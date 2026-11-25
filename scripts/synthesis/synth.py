#!/usr/bin/env python3
# Synthesise the benchmark designs with Yosys/ABC onto one library and check the result:
# formal equivalence with the RTL, gate-level simulation with the testbench, and switching
# activity from the VCD for power analysis. Results per design in <out>/<lib>/<design>/
# (netlist, stat.txt, result.json). Called by run_synth.sh.

import argparse, collections, os, re, subprocess, sys
import libs, models

# Per design: clock port, time per operation in ns of simulation (one clock period, or one
# input vector for the combinational rca8), and the VCD window to measure activity in.
DESIGNS = {
    "rca8": dict(clk=None, op=1.0, win=None),
    "counter8": dict(clk="clk", op=10.0, win=None),
    "demo": dict(clk="clk", op=100.0, win=(400.0, 400.0 + 20000 * 100.0)),
}
# Output pin names of both libraries, used to find the driver of each net.
OUTPINS = ("Y", "X", "Q", "QB", "Q_N")


def run(cmd, log):
    with open(log, "w") as f:
        r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    return r.returncode


def synth(A, L, design, out):
    top = design
    rtl = os.path.join(A.root, "rtl", design + ".v")
    lib = A.synlib[L["name"]]
    os.makedirs(os.path.join(out, "lib"), exist_ok=True)
    libs.techmaps(L, out)
    open(os.path.join(out, "map.script"), "w").write("strash\ndch -f\nmap\n")
    open(os.path.join(out, "map_area.script"), "w").write("strash\ndch -f\nmap -a\n")
    # demo.v has cov_<function> submodules that must each use one specific cell so every library
    # cell appears in the benchmark. Each gets a library with only that cell plus inverter and
    # NAND/NOR helpers made 1000x larger in area, so ABC picks the target cell.
    cov = re.findall(r"module cov_(\w+)", open(rtl).read())
    for c in cov:
        target = L["cells"][c][0]
        helpers = [L["cells"]["inv1"][0], L["cells"]["nor2" if c == "nand2" else "nand2"][0]]
        keep = [target] + [h for h in helpers if h != target]
        libs.subset(lib, os.path.join(out, "lib", "only_%s.lib" % c), keep, {h: 1000.0 for h in helpers if h != target})
    # Main flow: generic synthesis, flip-flops/latches onto the library, the forced cov_ blocks,
    # ABC on the rest, then flatten, give nets and cells short names and write the netlist.
    ys = ["read_verilog -sv %s" % rtl,
          "read_liberty -overwrite -setattr liberty_cell -lib %s" % lib,
          "hierarchy -check -top %s" % top,
          "synth -top %s -flatten" % top,
          "dfflegalize -cell $_DFF_P_ x -cell $_DLATCH_P_ x -cell $_DLATCH_N_ x",
          "techmap -map %s" % os.path.join(out, "latch_map.v"),
          "dfflibmap -liberty %s" % lib]
    for c in cov:
        ys.append("cd cov_%s" % c)
        if c == "inv1":
            ys.append("techmap -map %s" % os.path.join(out, "inv_map.v"))
        else:
            ys.append("abc -liberty %s -script %s" % (os.path.join(out, "lib", "only_%s.lib" % c), os.path.join(out, "map_area.script")))
        ys.append("cd ..")
    ys += ["cd %s" % top, "abc -liberty %s -script %s" % (lib, os.path.join(out, "map.script")), "cd ..",
           "setattr -mod -unset keep_hierarchy *", "flatten", "opt_clean -purge", "hierarchy -top %s" % top,
           "rename %s %s_gate" % (top, top),
           "rename -hide w:* i:* %d o:* %d", "rename -hide c:*",
           "rename -enumerate -pattern n% w:* i:* %d o:* %d", "rename -enumerate -pattern u% c:*",
           "check -assert",
           "tee -o %s stat -liberty %s" % (os.path.join(out, "stat.txt"), lib),
           "write_verilog -noattr -noexpr %s" % os.path.join(out, top + "_gate.v")]
    open(os.path.join(out, "synth.ys"), "w").write("\n".join(ys) + "\n")
    if run([A.yosys, "-q", "-s", os.path.join(out, "synth.ys")], os.path.join(out, "synth.log")):
        sys.exit("yosys synthesis failed for %s/%s, see %s/synth.log" % (L["name"], design, out))
    models.main(lib, os.path.join(out, "cells.v"), libs.cell_names(L))
    return os.path.join(out, top + "_gate.v")


# Cell usage count; stops if the netlist contains anything that is not a library cell.
def usage(L, net):
    names = libs.cell_names(L)
    used = collections.Counter(re.findall(r"^\s*(\w+)\s+u\d+\s*\(", open(net).read(), re.M))
    foreign = sorted(set(used) - set(names))
    if foreign:
        sys.exit("non-library cells in %s: %s" % (net, foreign))
    return {n: used.get(n, 0) for n in names}


# Yosys equivalence check of the RTL against the gate netlist (sequential, induction depth 2).
def equiv(A, design, out):
    top = design
    ys = """read_verilog -sv %(rtl)s
setattr -mod -unset keep_hierarchy *
prep -top %(top)s -flatten
design -stash gold
read_verilog %(cells)s
read_verilog %(net)s
prep -top %(top)s_gate -flatten
design -stash gate
design -copy-from gold -as gold %(top)s
design -copy-from gate -as gate %(top)s_gate
async2sync
equiv_make gold gate equiv
hierarchy -top equiv
equiv_simple -seq 2
equiv_induct -seq 2
tee -o %(st)s equiv_status
equiv_status -assert
""" % dict(rtl=os.path.join(A.root, "rtl", design + ".v"), top=top, cells=os.path.join(out, "cells.v"),
           net=os.path.join(out, top + "_gate.v"), st=os.path.join(out, "equiv_status.txt"))
    open(os.path.join(out, "equiv.ys"), "w").write(ys)
    return run([A.yosys, "-q", "-s", os.path.join(out, "equiv.ys")], os.path.join(out, "equiv.log")) == 0


# Run the testbench against the gate netlist (PASS line expected) and dump the VCD,
# only inside the measurement window when one is set.
def simulate(A, design, out):
    D = DESIGNS[design]
    tb = "tb_" + design
    win = D["win"]
    dump = "module dump_ctl;\ninitial begin\n  $dumpfile(\"%s\");\n  $dumpvars(1, %s.gate);\n" % (os.path.join(out, "gate.vcd"), tb)
    if win:
        dump += "  $dumpoff;\n  #%g $dumpon;\n  #%g $dumpoff;\n" % (win[0], win[1] - win[0])
    dump += "end\nendmodule\n"
    open(os.path.join(out, "dump_ctl.v"), "w").write(dump)
    vvp = os.path.join(out, "sim.vvp")
    if run([A.iverilog, "-g2005", "-o", vvp, os.path.join(A.root, "tb", tb + ".v"), os.path.join(A.root, "rtl", design + ".v"),
            os.path.join(out, "cells.v"), os.path.join(out, design + "_gate.v"), os.path.join(out, "dump_ctl.v")],
           os.path.join(out, "iverilog.log")):
        sys.exit("iverilog failed for %s, see %s/iverilog.log" % (design, out))
    run([A.vvp, "-n", vvp], os.path.join(out, "sim.log"))
    log = open(os.path.join(out, "sim.log")).read()
    return bool(re.search(r"(?m)^PASS", log)), log


# Toggles per operation and fraction of time at 1 for every bit in the VCD, counted only
# while dumping is on. These feed set_power_activity in sta.py.
def vcd_activity(path, op, win):
    ids, vals, tog, high, last = {}, {}, collections.Counter(), collections.Counter(), {}
    t = 0.0
    scale = 1.0
    t0, t1 = None, None
    on = True
    with open(path) as f:
        hdr = True
        for line in f:
            s = line.strip()
            if hdr:
                if s.startswith("$timescale"):
                    m = re.search(r"(\d+)\s*(s|ms|us|ns|ps|fs)", s + next(f, ""))
                    scale = float(m.group(1)) * {"s": 1e9, "ms": 1e6, "us": 1e3, "ns": 1.0, "ps": 1e-3, "fs": 1e-6}[m.group(2)]
                elif s.startswith("$var"):
                    p = s.split()
                    w, code, name = int(p[2]), p[3], p[4]
                    rng = p[5] if len(p) > 6 and p[5].startswith("[") else None
                    if w == 1:
                        bits = [name + (rng if rng else "")]
                    else:
                        hi, lo = [int(x) for x in rng.strip("[]").split(":")]
                        step = -1 if hi >= lo else 1
                        bits = ["%s[%d]" % (name, i) for i in range(hi, lo + step, step)]
                    ids[code] = bits
                elif s.startswith("$enddefinitions"):
                    hdr = False
                continue
            if not s:
                continue
            c = s[0]
            if c == "#":
                tn = float(s[1:]) * scale
                for b, v in vals.items():
                    if v == "1" and on and t0 is not None:
                        high[b] += tn - t
                t = tn
                continue
            if s.startswith("$dumpoff"):
                on = False
                t1 = t
                continue
            if s.startswith("$dumpon"):
                on = True
                t0 = t
                continue
            if s.startswith("$"):
                continue
            if c in "01xzXZ":
                code, bv = s[1:], c
                pairs = [(ids[code][0], bv)] if code in ids else []
            elif c in "bB":
                v, code = s[1:].split()
                bits = ids.get(code, [])
                v = v.rjust(len(bits), "0")
                pairs = list(zip(bits, v))
            else:
                continue
            if t0 is None:
                t0 = t
            for b, bv in pairs:
                old = vals.get(b)
                if on and old in ("0", "1") and bv in ("0", "1") and old != bv:
                    tog[b] += 1
                vals[b] = bv
    if t1 is None or t1 < t0:
        t1 = t
    dur = t1 - t0
    ops = dur / op
    if ops <= 0:
        sys.exit("no simulated operations in " + path)
    return {b: (tog[b] / ops, min(1.0, high[b] / dur)) for b in set(list(tog) + list(high) + list(vals))}, ops


# Net -> driving cell pin, so activity can be attached to the right pin in OpenSTA.
def drivers(L, net):
    txt = open(net).read()
    out = {}
    for m in re.finditer(r"^\s*(\w+)\s+(u\d+)\s*\((.*?)\);", txt, re.M | re.S):
        for pin, n in re.findall(r"\.(\w+)\(([^()]*)\)", m.group(3)):
            n = n.strip()
            if pin in OUTPINS and n:
                out[n.replace(" ", "")] = "%s/%s" % (m.group(2), pin)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lib", required=True, choices=list(libs.LIBS))
    ap.add_argument("--synlib", required=True)
    ap.add_argument("--designs", default="rca8,counter8,demo")
    ap.add_argument("--yosys", default="yosys")
    ap.add_argument("--iverilog", default="iverilog")
    ap.add_argument("--vvp", default="vvp")
    A = ap.parse_args()
    L = libs.LIBS[A.lib]
    A.synlib = {A.lib: A.synlib}
    import json
    for d in A.designs.split(","):
        out = os.path.join(A.out, A.lib, d)
        os.makedirs(out, exist_ok=True)
        net = synth(A, L, d, out)
        cnt = usage(L, net)
        eq = equiv(A, d, out)
        ok, log = simulate(A, d, out)
        act, ops = vcd_activity(os.path.join(out, "gate.vcd"), DESIGNS[d]["op"], DESIGNS[d]["win"])
        drv = drivers(L, net)
        json.dump(dict(design=d, lib=A.lib, cells=cnt, equiv=eq, sim=ok, ops=ops,
                       activity={k: v for k, v in act.items()}, drivers=drv, clk=DESIGNS[d]["clk"]),
                  open(os.path.join(out, "result.json"), "w"), indent=1)
        print("%-6s %-9s cells %4d  used %2d/13  equiv %s  sim %s  ops %d" %
              (A.lib, d, sum(cnt.values()), sum(1 for v in cnt.values() if v), "PASS" if eq else "FAIL", "PASS" if ok else "FAIL", ops))
        if not (eq and ok):
            sys.exit("verification failed for %s/%s" % (A.lib, d))


if __name__ == "__main__":
    main()
