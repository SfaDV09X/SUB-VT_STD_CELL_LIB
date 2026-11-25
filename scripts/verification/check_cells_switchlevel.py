#!/usr/bin/env python3
# Switch-level check of every combinational cell: for each input vector, find which
# nodes are pulled to VDD or GND through the conducting transistors and compare the
# output with the Liberty function. Latches and flip-flops are skipped.
# Usage: check_cells_switchlevel.py <liberty file> <cells dir>

import re, sys, itertools, os

lib, sdir = sys.argv[1], sys.argv[2]
txt = open(lib).read()
# Collect input pins, the output pin and its function for each cell in the Liberty file.
# The function is rewritten to Python syntax (! -> ~, + -> |) so it can be eval'd.
funcs = {}
for m in re.finditer(r'cell\s*\(\s*(\w+)\s*\)\s*\{', txt):
    name, i, depth = m.group(1), m.end(), 1
    while depth:
        depth += (txt[i] == '{') - (txt[i] == '}'); i += 1
    body = txt[m.end():i-1]
    if re.search(r'\b(latch|ff)\s*\(', body):
        continue
    ins  = re.findall(r'pin\s*\(\s*(\w+)\s*\)\s*\{\s*direction : input', body)
    out  = re.search(r'pin\s*\(\s*(\w+)\s*\)\s*\{\s*direction : output;[^{}]*?function : "([^"]+)"', body)
    funcs[name] = (ins, out.group(1), out.group(2).replace('!', '~').replace('+', '|'))

# Ports of the .subckt and every transistor as (type, drain, gate, source).
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
    # Netlist can be in a few places depending on the folder layout; try each.
    f = os.path.join(sdir, name, name + '.spice')
    f = f if os.path.exists(f) else os.path.join(sdir, name.upper(), 'spice', name + '.spice')
    f = f if os.path.exists(f) else os.path.join(sdir, name + '.spice')
    ports, fets = parse(f)
    assert set(ins) <= set(ports) and outp in ports, (name, ports)
    internal = {n for f in fets for n in f[1:]} - {'VDD', 'GND'} - set(ins)
    ok = True
    # Iterate the node values until they settle: a transistor conducts when its gate is
    # known and on, a node is 1/0 if it reaches VDD/GND, 'X' if it reaches both (fight).
    for vec in itertools.product([0, 1], repeat=len(ins)):
        env = dict(zip(ins, vec))
        val = {n: None for n in internal}
        for _ in range(20):
            def lvl(n):
                if n == 'VDD': return 1
                if n == 'GND': return 0
                return env[n] if n in env else val[n]
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
                else: new[n] = val[n]
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
# Exit code = number of failing cells, so this can be used in scripts.
sys.exit(bad)
