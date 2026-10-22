#!/usr/bin/env python3
"""Derive the per-cell FO1 5x5 grid from a probe .lib of that cell (one corner).
usage: make_grids.py <probe.lib> <cell>
FO1 load  C = mean of the cell's input-pin capacitances (pF)   -> LOADS = C*[0.5, 1, 2, 4, 8]
s*        = fixed point of s -> mean over all arcs/edges of transition(load=C, slew=s)
            (steady-state slew of a chain of this cell, each stage loaded by one input pin)
SLEWS     = s* * [0.25, 0.5, 1, 2, 4]   (ns, 30%-70% slew)
STEP      = lctime time step: 1e5 steps must cover the worst-case window
            (input ramp + delay + output transition at the largest grid point), x3 margin, rounded up to 1-2-5.
Prints shell-sourceable lines."""
import sys, math
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from liberty.parser import parse_liberty

lib = parse_liberty(open(sys.argv[1]).read())
name = sys.argv[2]
cell = next(c for c in lib.get_groups("cell") if str(c.args[0]) == name)
pins = list(cell.get_groups("pin"))
caps = [float(p["capacitance"]) for p in pins if str(p["direction"]) == "input"]
cin = float(np.mean(caps))
out = next(p for p in pins if str(p["direction"]) == "output")


def rows(x):
    return np.array([[float(v) for v in str(r).strip().strip('"').split(",")] for r in x])


def interp(g):
    return RegularGridInterpolator((rows(g["index_1"])[0], rows(g["index_2"])[0]), rows(g["values"]),
                                   bounds_error=False, fill_value=None)


trans, delay = [], []
for t in out.get_groups("timing"):
    for n in ("rise_transition", "fall_transition"):
        for g in t.get_groups(n): trans.append(interp(g))
    for n in ("cell_rise", "cell_fall"):
        for g in t.get_groups(n): delay.append(interp(g))
if not trans or not delay: sys.exit("no timing tables in %s" % sys.argv[1])

s = 500.0
for _ in range(200):
    s_new = float(np.mean([f([[cin, s]])[0] for f in trans]))
    if abs(s_new - s) < 1e-6 * max(s, 1e-12): break
    s = s_new
loads = cin * np.array([0.5, 1, 2, 4, 8]); slews = s * np.array([0.25, 0.5, 1, 2, 4])
pt = [[loads[-1], slews[-1]]]
window = slews[-1] / 0.4 + max(f(pt)[0] for f in delay) + max(f(pt)[0] for f in trans)   # ns
need = 3 * window * 1e-9 / 1e5
e = 10 ** math.floor(math.log10(need))
step = next(m * e for m in (1, 2, 5, 10) if m * e >= need)
fmt = lambda v: ", ".join("%.6g" % x for x in v)
print("# %s: C_FO1(mean of %d input pins %s pF) = %.6g pF ; s* = %.6g ns ; window = %.4g ns" %
      (name, len(caps), ["%.4g" % c for c in caps], cin, s, window))
print('SLEWS="%s"' % fmt(slews))
print('LOADS="%s"' % fmt(loads))
print('STEP="%.0e"' % step)
