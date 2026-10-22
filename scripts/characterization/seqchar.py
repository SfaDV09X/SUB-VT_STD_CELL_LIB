#!/usr/bin/env python3
"""Characterize one sequential cell (rising-edge DFF or active-high latch) with ngspice and write a Liberty file.
Why not lctime: lctime has no latch support, and its flip-flop code hard-codes ps/ns-scale timing (2 ns setup, 100 ps pulse,
100 ns max delay) which do not fit a 0.4 V sub-threshold cell (delays are microseconds).

usage: seqchar.py --kind dff|latch --cell NAME --net PEXC.spice --lef CELL.lef --models MODELS.lib --corner tt
                  --out OUT.lib [--jobs N] [--ngspice ngspice] [--workdir DIR] [--vdd 0.4] [--temp 27]
Cell ports (read from the .subckt line): CLK D Q QB VDD GND.
Definitions (all thresholds as in the combinational libs: delay 50%/50%, slew 30%/70%):
  C_FO1   = mean of the CLK and D input-pin capacitances (measured by charge integration of a fast ramp)
  s*      = fixed point of mean Q/QB transition at load C_FO1 with CLK slew s  (steady slew, as for the other cells)
  grid    = loads C_FO1*[0.5,1,2] (both Q and QB loaded), slews s*[0.5,1,2] (CLK, and D for constraints)
  clk->Q  : DFF CLK rising; latch CLK rising (opening edge)       latch D->Q: CLK high, D toggles
  setup/hold: DFF vs CLK rising; latch vs CLK falling (closing edge). Setup = smallest D->CLK 50%-50% time for which the
  output is correct with delay <= 1.10 x nominal; hold = smallest CLK->D 50%-50% time for which the old data is captured
  (DFF: also delay <= 1.10 x nominal). Constraint sims use zero external load, as lctime does."""
import argparse, os, re, subprocess, sys, tempfile, math
import numpy as np
from concurrent.futures import ProcessPoolExecutor

_trapz = getattr(np, 'trapezoid', None) or np.trapz
A = None  # parsed args (set in main, inherited by workers via fork)
PUSHOUT = 1.10


def ports(net, cell):
    for l in open(net):
        m = re.match(r"\s*\.subckt\s+" + re.escape(cell) + r"\s+(.*)", l, re.I)
        if m: return m.group(1).split()
    sys.exit("no .subckt %s in %s" % (cell, net))


def pwl(init, trans):
    """trans: list of (t50_ns, level 0/1, slew_ns 30-70). Linear ramp, 50% point at t50. Returns PWL string in seconds."""
    v = lambda x: x * A.vdd
    pts = [(0.0, v(init))]
    cur = init
    for t, lvl, s in sorted(trans):
        tr = s / 0.4
        pts.append((t - tr / 2, v(cur))); pts.append((t + tr / 2, v(lvl))); cur = lvl
    out = [pts[0]]
    for t, x in pts[1:]:
        assert t > out[-1][0], "overlapping edges: %s" % (pts,)
        out.append((t, x))
    return "PWL(" + " ".join("%.6gn %.6g" % (t, x) for t, x in out) + ")"


def simulate(clk, d, tstop_ns, load_pf, tag, tmax_ns=None):
    """clk, d = PWL strings. Returns dict t,clk,d,q,qb in ns / V."""
    P = ports(A.net, A.cell)
    pin = {"CLK": "clk", "D": "d", "Q": "q", "QB": "qb", "VDD": "vdd", "GND": "0"}
    inst = " ".join(pin[p] for p in P)
    tmax = tmax_ns or max(tstop_ns / 3000.0, 1.0)
    base = os.path.join(A.workdir, tag)
    cir = """* seqchar
.lib "%s" %s
.include "%s"
.temp %g
Vdd vdd 0 DC %g
Vclk clk 0 %s
Vd d 0 %s
X1 %s %s
Cq q 0 %gp
Cqb qb 0 %gp
.tran %gn %gn
.control
set filetype=ascii
run
wrdata %s.dat v(clk) v(d) v(q) v(qb)
quit
.endc
.end
""" % (A.models, A.corner, A.net, A.temp, A.vdd, clk, d, inst, A.cell, load_pf, load_pf, tmax, tstop_ns, base)
    open(base + ".sp", "w").write(cir)
    r = subprocess.run([A.ngspice, "-b", base + ".sp"], capture_output=True, text=True,
                       env=dict(os.environ, OMP_NUM_THREADS="1"))
    if not os.path.exists(base + ".dat"):
        sys.exit("ngspice failed for %s:\n%s" % (tag, (r.stdout + r.stderr)[-1500:]))
    x = np.loadtxt(base + ".dat")
    for e in (".sp", ".dat"): os.remove(base + e)
    return dict(t=x[:, 0] * 1e9, clk=x[:, 1], d=x[:, 3], q=x[:, 5], qb=x[:, 7])


def cross(t, v, level, rising, t0, t1):
    """first crossing of `level` with given direction in [t0,t1] (ns), linear interpolation, or None."""
    m = (t >= t0) & (t <= t1)
    tt, vv = t[m], v[m]
    s = (vv[:-1] - level) * (vv[1:] - level) < 0
    for i in np.nonzero(s)[0]:
        if (vv[i + 1] > vv[i]) == rising:
            return tt[i] + (level - vv[i]) * (tt[i + 1] - tt[i]) / (vv[i + 1] - vv[i])
    return None


def edge_meas(w, node, rising, t_ref, t0, t1):
    """(delay, slew) of node's transition in [t0,t1] relative to t_ref (ns); None if no full transition."""
    v = w[node]; V = A.vdd
    t50 = cross(w["t"], v, 0.5 * V, rising, t0, t1)
    t30 = cross(w["t"], v, (0.3 if rising else 0.7) * V, rising, t0, t1)
    t70 = cross(w["t"], v, (0.7 if rising else 0.3) * V, rising, t0, t1)
    if None in (t50, t30, t70): return None
    return t50 - t_ref, abs(t70 - t30)


# ---------------------------------------------------------------- input capacitance
def input_cap(pin):
    """Mean of rise/fall charge-integration capacitance (pF). Other input is held in the state where the pin is 'seen':
    D with the master/transparent phase open, CLK with D=0."""
    V = A.vdd; ramp = 10.0                          # ns, 0-100% ramp
    res = []
    for rising in (True, False):
        t0, T = 200.0, 600.0
        lv_a, lv_b = (0, 1) if rising else (1, 0)
        edge = "PWL(0 %g %gn %g %gn %g)" % (lv_a * V, t0, lv_a * V, t0 + ramp, lv_b * V)
        if pin == "D":
            open_lvl = 0 if A.kind == "dff" else 1
            other = "PWL(0 %g)" % (open_lvl * V)
            clk_s, d_s = other, edge
        else:
            clk_s, d_s = edge, "PWL(0 0)"
        P = ports(A.net, A.cell)
        pmap = {"CLK": "clk", "D": "d", "Q": "q", "QB": "qb", "VDD": "vdd", "GND": "0"}
        inst = " ".join(pmap[p] for p in P)
        base = os.path.join(A.workdir, "cap_%s_%d" % (pin, rising))
        src = "Vclk" if pin == "CLK" else "Vd"
        open(base + ".sp", "w").write("""* cap
.lib "%s" %s
.include "%s"
.temp %g
Vdd vdd 0 DC %g
Vclk clk 0 %s
Vd d 0 %s
X1 %s %s
.tran 0.5n %gn
.control
set filetype=ascii
run
wrdata %s.dat i(%s)
quit
.endc
.end
""" % (A.models, A.corner, A.net, A.temp, A.vdd, clk_s, d_s, inst, A.cell, T, base, src))
        subprocess.run([A.ngspice, "-b", base + ".sp"], capture_output=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
        x = np.loadtxt(base + ".dat"); t = x[:, 0] * 1e9; i = x[:, 1]
        for e in (".sp", ".dat"): os.remove(base + e)
        i0 = np.mean(i[(t > t0 - 80) & (t < t0 - 5)])                 # static current before the ramp (A, leakage)
        i1 = np.mean(i[(t > t0 + ramp + 80) & (t < t0 + ramp + 150)])   # static current after the ramp
        a, b = t0 - 5, t0 + ramp + 60                                    # integrate ramp + short settling
        q = _trapz(i[(t >= a) & (t <= b)] - np.interp(t[(t >= a) & (t <= b)], [a, b], [i0, i1]),
                         t[(t >= a) & (t <= b)]) * 1e-9
        res.append(abs(q) / V * 1e12)                                     # pF
    return float(np.mean(res))


# ---------------------------------------------------------------- stimuli
def clk_to_q(args):
    """Edge-triggered / opening-edge delays. args=(sc, load, H). Returns dict[(out,'rise'|'fall')] = (delay, slew)."""
    sc, load, H = args
    # CLK: pulses at H-2H, 3H-4H, 5H-6H ; D: 0, ->1 at 2.5H, ->0 at 4.5H
    clk = pwl(0, [(H, 1, sc), (2 * H, 0, sc), (3 * H, 1, sc), (4 * H, 0, sc), (5 * H, 1, sc), (6 * H, 0, sc)])
    d = pwl(0, [(2.5 * H, 1, sc), (4.5 * H, 0, sc)])
    w = simulate(clk, d, 7 * H, load, "cq_%g_%g" % (sc, load))
    r = {}
    for out, (r2, f3) in (("q", (True, False)), ("qb", (False, True))):
        m1 = edge_meas(w, out, r2, 3 * H, 3 * H, 4 * H)           # edge 2: Q rises, QB falls
        m2 = edge_meas(w, out, f3, 5 * H, 5 * H, 6 * H)           # edge 3: Q falls, QB rises
        if out == "q":
            r[("q", "rise")], r[("q", "fall")] = m1, m2
        else:
            r[("qb", "fall")], r[("qb", "rise")] = m1, m2
    return r


def d_to_q(args):
    """Latch transparent delays: CLK high from H; D rises at 3H, falls at 5H. args=(sd, load, H)."""
    sd, load, H = args
    clk = pwl(0, [(H, 1, sd)])
    d = pwl(0, [(3 * H, 1, sd), (5 * H, 0, sd)])
    w = simulate(clk, d, 7 * H, load, "dq_%g_%g" % (sd, load))
    r = {}
    r[("q", "rise")] = edge_meas(w, "q", True, 3 * H, 3 * H, 4 * H)
    r[("q", "fall")] = edge_meas(w, "q", False, 5 * H, 5 * H, 6 * H)
    r[("qb", "fall")] = edge_meas(w, "qb", False, 3 * H, 3 * H, 4 * H)
    r[("qb", "rise")] = edge_meas(w, "qb", True, 5 * H, 5 * H, 6 * H)
    return r


def setup_trial(sd, sc, rising_d, t_su, H):
    """True if captured correctly with delay <= PUSHOUT*nominal (nominal supplied by caller via closure), returns (ok, delay)."""
    new = 1 if rising_d else 0; old = 1 - new
    tc = 3 * H
    if A.kind == "dff":
        clk = pwl(0, [(H, 1, sc), (2 * H, 0, sc), (tc, 1, sc)])
        d = pwl(old, [(tc - t_su, new, sd)])
        end = 4.6 * H
        w = simulate(clk, d, end, 0.0, "su_%g" % abs(hash((sd, sc, rising_d, round(t_su, 4)))))
        meas = edge_meas(w, "q", bool(new), tc, tc - 0.2 * H, end)
        dly = None if meas is None else meas[0]
        ok = w["q"][-1] > 0.9 * A.vdd if new else w["q"][-1] < 0.1 * A.vdd
        return ok and dly is not None, dly
    else:  # latch: transparent until CLK falls at tc
        clk = pwl(0, [(H, 1, sc), (tc, 0, sc)])
        d = pwl(old, [(tc - t_su, new, sd)])
        end = 4.6 * H
        w = simulate(clk, d, end, 0.0, "su_%g" % abs(hash((sd, sc, rising_d, round(t_su, 4)))))
        tD = tc - t_su
        meas = edge_meas(w, "q", bool(new), tD, tD - 0.1 * H, end)
        dly = None if meas is None else meas[0]
        ok = w["q"][-1] > 0.9 * A.vdd if new else w["q"][-1] < 0.1 * A.vdd
        return ok and dly is not None, dly


def hold_trial(sd, sc, rising_d, t_h, H):
    """D value V=new is captured at the active clock edge; D flips to !V at t_edge + t_h. Returns (ok, delay)."""
    V = 1 if rising_d else 0; nV = 1 - V
    tc = 3 * H
    if A.kind == "dff":
        clk = pwl(0, [(H, 1, sc), (2 * H, 0, sc), (tc, 1, sc)])
        d = pwl(nV, [(2.5 * H, V, sd), (tc + t_h, nV, sd)])
        end = 4.6 * H
        w = simulate(clk, d, end, 0.0, "ho_%g" % abs(hash((sd, sc, rising_d, round(t_h, 4)))))
        meas = edge_meas(w, "q", bool(V), tc, tc - 0.2 * H, end)
        dly = None if meas is None else meas[0]
        ok = w["q"][-1] > 0.9 * A.vdd if V else w["q"][-1] < 0.1 * A.vdd
        return ok and dly is not None, dly
    else:
        clk = pwl(0, [(H, 1, sc), (tc, 0, sc)])
        d = pwl(nV, [(2 * H, V, sd), (tc + t_h, nV, sd)])
        end = 4.6 * H
        w = simulate(clk, d, end, 0.0, "ho_%g" % abs(hash((sd, sc, rising_d, round(t_h, 4)))))
        return (w["q"][-1] > 0.9 * A.vdd if V else w["q"][-1] < 0.1 * A.vdd), None


def bisect(trial, lo, hi, d_nom, H, iters=9):
    """smallest x in [lo,hi] with trial passing (pass at hi, fail at lo assumed, checked). Returns x or None if hi fails."""
    def passes(x):
        ok, dly = trial(x)
        return ok and (d_nom is None or dly <= PUSHOUT * d_nom)
    if not passes(hi):
        hi2 = hi * 2
        if hi2 < 0.4 * H and passes(hi2): hi = hi2
        else: return None
    if passes(lo):
        return lo                     # constraint is below the search window; clipped
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if passes(mid): hi = mid
        else: lo = mid
    return hi


def constraint(args):
    """args=(kind 'setup'|'hold', sd, sc, rising_d, H, d_ref). Returns time in ns."""
    k, sd, sc, rd, H, d_ref = args
    if k == "setup":
        tr = lambda x: setup_trial(sd, sc, rd, x, H)
        _, dnom = tr(0.5 * H)
        return bisect(tr, -1.5 * d_ref, 4 * d_ref, dnom, H)
    tr = lambda x: hold_trial(sd, sc, rd, x, H)
    ok, dnom = tr(0.5 * H)
    return bisect(tr, -2 * d_ref, 3 * d_ref, dnom if A.kind == "dff" else None, H)


# ---------------------------------------------------------------- liberty writer
def tab(rows):
    return ", \\\n".join('            "%s"' % ", ".join("%.6f" % v for v in r) for r in rows)


def fmt_idx(v): return ", ".join("%.6f" % x for x in v)


def main():
    global A
    p = argparse.ArgumentParser()
    p.add_argument("--kind", choices=["dff", "latch"], required=True)
    for k in ("cell", "net", "lef", "models", "corner", "out"): p.add_argument("--" + k, required=True)
    p.add_argument("--jobs", type=int, default=os.cpu_count()); p.add_argument("--ngspice", default="ngspice")
    p.add_argument("--workdir", default=None); p.add_argument("--vdd", type=float, default=0.4)
    p.add_argument("--temp", type=float, default=27.0)
    p.add_argument("--H", type=float, default=100000.0, help="half-period of the stimulus in ns (must exceed ~8x the largest delay)")
    A = p.parse_args()
    A.workdir = A.workdir or tempfile.mkdtemp(prefix="seq_")
    os.makedirs(A.workdir, exist_ok=True)
    import multiprocessing as mp
    pool = ProcessPoolExecutor(A.jobs, mp_context=mp.get_context('fork'))
    log = lambda s: print(s, flush=True)

    # 1) FO1 load from input caps
    cD, cC = pool.submit(input_cap, "D"), pool.submit(input_cap, "CLK")
    cD, cC = cD.result(), cC.result()
    C = 0.5 * (cD + cC)
    log("input caps: D=%.4f pF  CLK=%.4f pF  -> C_FO1 = %.4f pF" % (cD, cC, C))

    # 2) s* fixed point (clock slew -> mean output transition at C_FO1)
    H = A.H
    s = 500.0
    for it in range(10):
        r = clk_to_q((s, C, H))
        if any(v is None for v in r.values()): sys.exit("clk->Q did not complete; increase --H")
        s_new = float(np.mean([v[1] for v in r.values()]))
        log("  s* iteration %d: %.1f -> %.1f ns" % (it, s, s_new))
        if abs(s_new - s) < 0.01 * s: s = s_new; break
        s = s_new
    slews = s * np.array([0.5, 1, 2]); loads = C * np.array([0.5, 1, 2])
    log("grid: slews %s ns, loads %s pF" % (slews.round(1), loads.round(5)))

    # 3) delay tables (clock slew x load)
    jobs = {(i, j): pool.submit(clk_to_q, (slews[i], loads[j], H)) for i in range(3) for j in range(3)}
    cq = {k: f.result() for k, f in jobs.items()}
    arcs = [("q", "rise"), ("q", "fall"), ("qb", "rise"), ("qb", "fall")]
    for k, v in cq.items():
        if any(x is None for x in v.values()): sys.exit("missing transition at grid point %s" % (k,))
    dmax = max(v[0] for r in cq.values() for v in r.values())
    log("max clk->out delay on grid: %.0f ns (H=%.0f ns)" % (dmax, H))
    if H < 6 * dmax: sys.exit("H too small for the slowest delay; rerun with --H %d" % (8 * dmax))
    dq = None
    if A.kind == "latch":
        jobs = {(i, j): pool.submit(d_to_q, (slews[i], loads[j], H)) for i in range(3) for j in range(3)}
        dq = {k: f.result() for k, f in jobs.items()}
        if any(x is None for r in dq.values() for x in r.values()): sys.exit("missing D->Q transition")
    log("delay tables done")

    # 4) constraints (D slew x CLK slew), per D direction
    d_ref = cq[(1, 1)][("q", "rise")][0]
    cj = {}
    for kind in ("setup", "hold"):
        for rd in (True, False):
            for i in range(3):
                for j in range(3):
                    cj[(kind, rd, i, j)] = pool.submit(constraint, (kind, slews[i], slews[j], rd, H, d_ref))
    con = {k: f.result() for k, f in cj.items()}
    if any(v is None for v in con.values()): sys.exit("a constraint search failed (no passing point): %s" %
                                                       [k for k, v in con.items() if v is None])
    log("constraints done")

    # 5) write liberty
    m = re.search(r"SIZE\s+([\d.]+)\s+BY\s+([\d.]+)", open(A.lef).read())
    area = float(m.group(1)) * float(m.group(2))
    edge = "rising" if A.kind == "dff" else "falling"
    T = "delay_template_3x3"
    def delay_tbl(arc_get, which):
        # rows: loads (index_1), cols: slews (index_2), as lctime writes them
        return [[arc_get(i, j)[which] for i in range(3)] for j in range(3)]
    def timing_block(related, out, ttype, srcs, sense=None):
        s_ = ""
        for rf in ("rise", "fall"):
            pass
        return s_
    def block(related, ttype, src, out, sense):
        t = "      timing () {\n        related_pin : \"%s\";\n        timing_type : %s;\n" % (related, ttype)
        if sense: t += "        timing_sense : %s;\n" % sense
        for rf in ("rise", "fall"):
            for nm, w in (("cell_%s" % rf, 0), ("%s_transition" % rf, 1)):
                t += "        %s (%s) {\n          index_1 ( \\\n            \"%s\" \\\n          );\n          index_2 ( \\\n            \"%s\" \\\n          );\n          values ( \\\n%s \\\n          );\n        }\n" % (
                    nm, T, fmt_idx(loads), fmt_idx(slews),
                    tab(delay_tbl(lambda i, j: src[(i, j)][(out, rf)], w)))
        return t + "      }\n"
    def cons_block(ttype, key):
        t = "      timing () {\n        related_pin : \"CLK\";\n        timing_type : %s_%s;\n" % (key, edge)
        for rd, nm in ((True, "rise_constraint"), (False, "fall_constraint")):
            rows = [[con[(key, rd, i, j)] for j in range(3)] for i in range(3)]
            t += "        %s (constraint_template_3x3) {\n          index_1 ( \\\n            \"%s\" \\\n          );\n          index_2 ( \\\n            \"%s\" \\\n          );\n          values ( \\\n%s \\\n          );\n        }\n" % (
                nm, fmt_idx(slews), fmt_idx(slews), tab(rows))
        return t + "      }\n"
    clk_type = "rising_edge"
    seq = ("  ff (IQ, IQN) {\n      clocked_on : \"CLK\";\n      next_state : \"D\";\n    }\n" if A.kind == "dff" else
           "  latch (IQ, IQN) {\n      enable : \"CLK\";\n      data_in : \"D\";\n    }\n")
    dummy = fmt_idx([1000, 1001, 1002])
    lib = """library (subvt_sky130_%(c)s_0p40v_27c_%(cell)s) {
  delay_model : table_lookup;
  time_unit : "1ns";
  voltage_unit : "1V";
  current_unit : "1uA";
  pulling_resistance_unit : "1kohm";
  leakage_power_unit : "1nW";
  capacitive_load_unit (1, pf);
  nom_process : 1;
  nom_temperature : %(T)g;
  nom_voltage : %(V)g;
  input_threshold_pct_rise : 50;
  input_threshold_pct_fall : 50;
  output_threshold_pct_rise : 50;
  output_threshold_pct_fall : 50;
  slew_lower_threshold_pct_rise : 30;
  slew_upper_threshold_pct_rise : 70;
  slew_lower_threshold_pct_fall : 30;
  slew_upper_threshold_pct_fall : 70;
  slew_derate_from_library : 1.0;
  lu_table_template (delay_template_3x3) {
    variable_1 : total_output_net_capacitance;
    variable_2 : input_net_transition;
    index_1 ( \\
      "%(dm)s" \\
    );
    index_2 ( \\
      "%(dm)s" \\
    );
  }
  lu_table_template (constraint_template_3x3) {
    variable_1 : constrained_pin_transition;
    variable_2 : related_pin_transition;
    index_1 ( \\
      "%(dm)s" \\
    );
    index_2 ( \\
      "%(dm)s" \\
    );
  }
  cell (%(cell)s) {
    area : %(area).4f;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : VDD;
    }
    pg_pin (GND) {
      pg_type : primary_ground;
      voltage_name : GND;
    }
  %(seq)s    pin (CLK) {
      direction : input;
      clock : true;
      capacitance : %(cC).6f;
    }
    pin (D) {
      direction : input;
      capacitance : %(cD).6f;
%(dcons)s    }
""" % dict(c=A.corner, cell=A.cell, T=A.temp, V=A.vdd, dm=dummy, area=area, seq=seq, cC=cC, cD=cD,
           dcons=cons_block(None, "setup") + cons_block(None, "hold"))
    for out, fn in (("q", "IQ"), ("qb", "IQN")):
        lib += "    pin (%s) {\n      direction : output;\n      function : \"%s\";\n" % (out.upper(), fn)
        lib += block("CLK", "rising_edge", cq, out, None)
        if A.kind == "latch":
            lib += block("D", "combinational", dq, out, "positive_unate" if out == "q" else "negative_unate")
        lib += "    }\n"
    lib += "  }\n}\n"
    open(A.out, "w").write(lib)
    log("wrote %s" % A.out)


if __name__ == "__main__":
    main()
