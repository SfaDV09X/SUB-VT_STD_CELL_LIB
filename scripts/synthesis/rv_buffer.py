#!/usr/bin/env python3
# Fanout buffering for the synthesised cores. ABC's own buffering needs a buffer cell and
# the library has none, so every net with more than nmax loads is split here with a tree of
# inverter pairs (two inversions keep the logic value). The clock is left alone (ideal clock).

import collections, re


# Input pin names of every cell, from the behavioural models in cells.v.
def cell_inputs(cells_v):
    ins = {}
    for m in re.finditer(r"module\s+(\w+)\s*\(.*?\);\s*input\s+([^;]+);", open(cells_v).read(), re.S):
        ins[m.group(1)] = set(p.strip() for p in m.group(2).split(","))
    return ins


# Group the sinks nmax at a time, each group driven by an inverter (second level); those
# inverters are driven nmax at a time by first-level inverters, and so on until the source
# drives at most nmax pins. Returns (sink, driving net) pairs.
def fanout_tree(src, sinks, nmax, new_inv):
    if len(sinks) <= nmax:
        return [(s, src) for s in sinks]
    groups = [sinks[i:i + nmax] for i in range(0, len(sinks), nmax)]
    conn = []
    second = []
    for g in groups:
        pin, out = new_inv(None)
        second.append(pin)
        conn += [(s, out) for s in g]
    firsts = [second[i:i + nmax] for i in range(0, len(second), nmax)]
    first_pins = []
    for g in firsts:
        pin, out = new_inv(None)
        first_pins.append(pin)
        conn += [(s, out) for s in g]
    return conn + fanout_tree(src, first_pins, nmax, new_inv)


# Rewrite the netlist with the new inverters and wires; returns how many were inserted.
def buffer_netlist(src, dst, cells_v, inv, inv_in, inv_out, clock, nmax):
    text = open(src).read()
    ins = cell_inputs(cells_v)
    inst_re = re.compile(r"^(\s*)(\w+)\s+(u\d+)\s*\((.*?)\);\s*$", re.M | re.S)
    insts = []
    for m in inst_re.finditer(text):
        pins = re.findall(r"\.(\w+)\(([^()]*)\)", m.group(4))
        insts.append((m.start(), m.end(), m.group(2), m.group(3), pins))
    # Every non-clock net and the (instance, pin) pairs it drives.
    sinks = collections.defaultdict(list)
    for k, (_, _, cell, name, pins) in enumerate(insts):
        for p, n in pins:
            n = n.strip()
            if p in ins[cell] and n and n != clock and "'" not in n:
                sinks[n].append((k, p))
    new_wires = []
    new_cells = []
    counter = [0]
    base = max(int(i[3][1:]) for i in insts) + 1

    def new_inv(_):
        i = counter[0]
        counter[0] += 1
        a = "nb%d_a" % i
        y = "nb%d_y" % i
        new_wires.extend([a, y])
        new_cells.append("  %s u%d (\n    .%s(%s),\n    .%s(%s)\n  );\n" % (inv, base + i, inv_in, a, inv_out, y))
        return ("new", i), y

    remap = {}
    alias = {}
    for net, sk in sinks.items():
        if len(sk) <= nmax:
            continue
        for (s, drv) in fanout_tree(net, sk, nmax, new_inv):
            if s[0] == "new":
                alias[s[1]] = drv
            else:
                remap[s] = drv
    out = []
    last = 0
    for k, (st, en, cell, name, pins) in enumerate(insts):
        out.append(text[last:st])
        body = ",\n".join("    .%s(%s)" % (p, remap.get((k, p), n.strip())) for p, n in pins)
        out.append("  %s %s (\n%s\n  );" % (cell, name, body))
        last = en
    tail = text[last:]
    out.append(tail)
    res = "".join(out)
    # Inverters driving other new inverters are wired to their driver net directly.
    for i, drv in alias.items():
        new_cells[i] = new_cells[i].replace(".%s(nb%d_a)" % (inv_in, i), ".%s(%s)" % (inv_in, drv))
        new_wires.remove("nb%d_a" % i)
    decl = "".join("  wire %s;\n" % w for w in new_wires)
    res = re.sub(r"\n(\s*)endmodule\s*$", "\n" + "".join(new_cells) + "endmodule\n", res)
    res = res.replace(");\n", ");\n" + decl, 1)
    open(dst, "w").write(res)
    return dict(inserted=counter[0], nets_fixed=sum(1 for v in sinks.values() if len(v) > nmax),
                max_fanout_before=max(len(v) for v in sinks.values()))
