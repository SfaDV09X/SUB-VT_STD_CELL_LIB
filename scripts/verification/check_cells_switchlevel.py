#!/usr/bin/env python3
"""Switch-level truth-table check: transistor netlists (cells/<c>/<c>.spice) vs Liberty functions.
Static CMOS only (combinational cells). For every input vector, iterate node values to a fixed point:
a node is driven 1 if a conducting path to VDD exists, 0 if a conducting path to GND exists.
PASS requires: every output is driven (never floating), never contended (VDD and GND paths both),
and equals the Liberty function.
usage: check_cells_switchlevel.py <lib> <dir with <CELL>/spice/<cell>.spice, <cell>/<cell>.spice or <cell>.spice>"""
import re, sys, itertools, os

lib, sdir = sys.argv[1], sys.argv[2]
txt = open(lib).read()
funcs = {}
for m in re.finditer(r'cell\s*\(\s*(\w+)\s*\)\s*\{', txt):
    name, i, depth = m.group(1), m.end(), 1
    while depth:
        depth += (txt[i] == '{') - (txt[i] == '}'); i += 1
    body = txt[m.end():i-1]
    if re.search(r'\b(latch|ff)\s*\(', body):
        continue                                  # sequential: not checked here
    ins  = re.findall(r'pin\s*\(\s*(\w+)\s*\)\s*\{\s*direction : input', body)
    out  = re.search(r'pin\s*\(\s*(\w+)\s*\)\s*\{\s*direction : output;\s*function : "([^"]+)"', body)
    funcs[name] = (ins, out.group(1), out.group(2).replace('!', '~').replace('+', '|'))

def parse(path):
    subckt = None; fets = []
    for ln in open(path):
        t = ln.split()
        if not t or t[0].startswith(('*', '*.')): continue
        if t[0].lower() == '.subckt': subckt = t[1]; ports = t[2:]
        elif t[0].upper().startswith('X'):
            d, g, s, b = t[1:5]; model = t[5]
            fets.append(('n' if 'nfet' in model else 'p', d, g, s))
    return ports, fets

bad = 0
for name, (ins, outp, expr) in sorted(funcs.items()):
    f = os.path.join(sdir, name, name + '.spice')          # <dir>/<cell>/<cell>.spice (repo layout)
    f = f if os.path.exists(f) else os.path.join(sdir, name.upper(), 'spice', name + '.spice')   # repo layout: cells/<CELL>/spice/<cell>.spice
    f = f if os.path.exists(f) else os.path.join(sdir, name + '.spice')
    ports, fets = parse(f)
    assert set(ins) <= set(ports) and outp in ports, (name, ports)
    internal = {n for f in fets for n in f[1:]} - {'VDD', 'GND'} - set(ins)
    ok = True
    for vec in itertools.product([0, 1], repeat=len(ins)):
        env = dict(zip(ins, vec))
        val = {n: None for n in internal}       # None = unknown/undriven
        for _ in range(20):                      # settle through internal inverters
            def lvl(n):
                if n == 'VDD': return 1
                if n == 'GND': return 0
                return env[n] if n in env else val[n]
            # conducting edges
            edges = []
            for k, d, g, s in fets:
                gv = lvl(g)
                if gv is None: continue
                if (k == 'n' and gv == 1) or (k == 'p' and gv == 0): edges.append((d, s))
            def reach(src):
                seen = {src}; st = [src]
                while st:
                    x = st.pop()
                    for a, b in edges:
                        for u, v in ((a, b), (b, a)):
                            if u == x and v not in seen: seen.add(v); st.append(v)
                return seen
            up, dn = reach('VDD'), reach('GND')
            new = {}
            for n in internal:
                if n in up and n in dn: new[n] = 'X'
                elif n in up: new[n] = 1
                elif n in dn: new[n] = 0
                else: new[n] = val[n]            # floating: keep (flagged below if it is the output)
            if new == val: break
            val = new
        got = val[outp]
        want = eval(expr, {}, dict(env)) & 1
        if got != want:
            ok = False
            print("  %s %s -> got %s expected %d" % (name, dict(env), got, want))
    print("%-8s %s  (%d vectors, %d transistors)" % (name, "PASS" if ok else "FAIL", 2**len(ins), len(fets)))
    bad += not ok
print("RESULT:", "ALL PASS" if not bad else "%d FAIL" % bad)
sys.exit(bad)
