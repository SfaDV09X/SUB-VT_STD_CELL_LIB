#!/usr/bin/env python3
# Synthesise one or more RISC-V cores onto a library and verify them on every workload:
# RTL and gate-level simulation must both pass the self-check, their store traces must match
# the instruction-set simulator (rv_iss.py) and each other cycle for cycle. The gate-level
# VCD gives the switching activity for power. Results in <out>/<lib>/<core>/result.json.

import argparse, json, os, re, subprocess, sys, time
import libs, models, rv_iss, rv_buffer
from synth import usage, drivers
from rv_vcd import activity as vcd_activity

# RTL files, clock port and include dirs of each core (wrappers in benchmarking/wrap).
CORES = {
    "serv": dict(files=["cores/serv/serv_*.v"], clk="clk", inc=[]),
    "femto": dict(files=["cores/femtorv32/femtorv32_quark.v"], clk="clk", inc=[]),
    "pico": dict(files=["cores/picorv32/picorv32.v"], clk="clk", inc=[]),
    "dark": dict(files=["cores/darkriscv/rtl/darkriscv.v"], clk="clk", inc=["cores/darkriscv/rtl"]),
}
# Simulation clock period (only used to turn VCD time into cycles), fanout limit for buffering,
# and the workload programs in benchmarking/prog.
PERIOD_NS = 10.0
MAX_FANOUT = 4
WORKLOADS = ["sortcrc", "gemm", "stencil", "kmp", "spmv"]


def run(cmd, log, cwd=None, timeout=None):
    with open(log, "w") as f:
        try:
            return subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=cwd, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            f.write("\nTIMEOUT after %d s\n" % timeout)
            return None


def sources(A, core):
    import glob
    fs = []
    for p in CORES[core]["files"]:
        fs += sorted(f for f in glob.glob(os.path.join(A.root, p)) if not f.endswith("serv_synth_wrapper.v"))
    return fs + [os.path.join(A.root, "wrap", "core_%s.v" % core)]


# Yosys/ABC flow as in synth.py, then rv_buffer.py splits every net with more than MAX_FANOUT
# loads using inverter pairs, and the buffered netlist is checked and counted again.
def synth(A, L, lib, core, out):
    top = "core_" + core
    libs.techmaps(L, out)
    open(os.path.join(out, "map.script"), "w").write("strash\ndch -f\nmap\n")
    inc = " ".join("-I%s" % os.path.join(A.root, d) for d in CORES[core]["inc"])
    ys = ["read_verilog -sv %s %s" % (inc, f) for f in sources(A, core)]
    ys += ["read_liberty -overwrite -setattr liberty_cell -lib %s" % lib,
           "hierarchy -check -top %s" % top,
           "synth -top %s -flatten" % top,
           "setattr -unset init w:*",
           "dfflegalize -cell $_DFF_P_ x -cell $_DLATCH_P_ x -cell $_DLATCH_N_ x",
           "techmap -map %s" % os.path.join(out, "latch_map.v"),
           "dfflibmap -liberty %s" % lib,
           "abc -liberty %s -script %s" % (lib, os.path.join(out, "map.script")),
           "opt_clean -purge",
           "rename %s %s_gate" % (top, top),
           "rename -hide w:* i:* %d o:* %d", "rename -hide c:*",
           "rename -enumerate -pattern n% w:* i:* %d o:* %d", "rename -enumerate -pattern u% c:*",
           "check -assert",
           "tee -o %s stat -liberty %s" % (os.path.join(out, "stat_unbuffered.txt"), lib),
           "write_verilog -noattr -noexpr %s" % os.path.join(out, top + "_unbuffered.v")]
    open(os.path.join(out, "synth.ys"), "w").write("\n".join(ys) + "\n")
    if run([A.yosys, "-q", "-s", os.path.join(out, "synth.ys")], os.path.join(out, "synth.log")):
        sys.exit("yosys synthesis failed for %s/%s, see %s/synth.log" % (L["name"], core, out))
    models.main(lib, os.path.join(out, "cells.v"), libs.cell_names(L))
    inv, ip, io = L["cells"]["inv1"]
    B = rv_buffer.buffer_netlist(os.path.join(out, top + "_unbuffered.v"), os.path.join(out, top + "_gate.v"),
                                 os.path.join(out, "cells.v"), inv, ip["a"], io, CORES[core]["clk"], MAX_FANOUT)
    ys = ["read_liberty -lib %s" % lib, "read_verilog %s" % os.path.join(out, top + "_gate.v"),
          "hierarchy -check -top %s_gate" % top, "check -assert",
          "tee -o %s stat -liberty %s" % (os.path.join(out, "stat.txt"), lib)]
    open(os.path.join(out, "stat.ys"), "w").write("\n".join(ys) + "\n")
    if run([A.yosys, "-q", "-s", os.path.join(out, "stat.ys")], os.path.join(out, "stat.log")):
        sys.exit("buffered netlist check failed for %s/%s, see %s/stat.log" % (L["name"], core, out))
    return os.path.join(out, top + "_gate.v"), B


# Testbench for the RTL or (with -DGATE) for the gate netlist plus behavioural cell models.
def compile_tb(A, core, out, gate):
    tb = os.path.join(A.root, "tb", "tb_%s.v" % core)
    vvp = os.path.join(out, "sim_%s.vvp" % ("gate" if gate else "rtl"))
    inc = ["-I" + os.path.join(A.root, d) for d in CORES[core]["inc"]]
    if gate:
        srcs = ["-DGATE", tb, os.path.join(out, "cells.v"), os.path.join(out, "core_%s_gate.v" % core)]
    else:
        srcs = [tb] + sources(A, core)
    log = os.path.join(out, "comp_%s.log" % ("gate" if gate else "rtl"))
    if run([A.iverilog, "-g2012", "-o", vvp] + inc + srcs, log):
        sys.exit("iverilog failed, see " + log)
    return vvp


# Run one workload: +hex program, +expect result, optional +vcd. Returns pass flag, cycle
# count, result word and the store trace (cycle, address, data, byte mask).
def simulate(A, vvp, out, tag, hexfile, expect, vcd=None):
    args = [A.vvp, "-n", vvp, "+hex=" + hexfile, "+expect=%08x" % expect]
    if vcd:
        args.append("+vcd=" + vcd)
    log = os.path.join(out, "sim_%s.log" % tag)
    run(args, log)
    t = open(log).read()
    cyc = re.search(r"CYCLES (\d+)", t)
    res = re.search(r"RESULT (\w+)", t)
    trace = re.findall(r"(?m)^W (\d+) (\S+) (\S+) (\S+)$", t)
    return bool(re.search(r"(?m)^PASS", t)), int(cyc.group(1)) if cyc else None, res.group(1) if res else None, trace


# Store trace with the bytes that were not written replaced by "--", for comparison.
def masked(trace):
    out = []
    for c, a, d, m in trace:
        out.append((c, a, m, "".join(d[6 - 2 * k:8 - 2 * k] if m[3 - k] == "1" else "--" for k in range(3, -1, -1))))
    return out


# Stores of the simulation must equal the ISS stores in order, address, mask and data.
def store_check(trace, ref):
    if len(trace) != len(ref["stores"]):
        return False
    for (_, a, d, m), (ra, rm, rd) in zip(trace, ref["stores"]):
        if "x" in a.lower() or "x" in m.lower() or int(a, 16) & ~3 != ra or int(m, 2) != rm:
            return False
        for k in range(4):
            if rm >> k & 1:
                byte = d[6 - 2 * k:8 - 2 * k]
                if "x" in byte.lower() or "z" in byte.lower() or int(byte, 16) != (rd >> (8 * k)) & 0xFF:
                    return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lib", required=True, choices=["x4", "hd"])
    ap.add_argument("--synlib", required=True)
    ap.add_argument("--cores", default="serv,femto,pico,dark")
    ap.add_argument("--workloads", default=",".join(WORKLOADS))
    ap.add_argument("--yosys", default="yosys")
    ap.add_argument("--iverilog", default="iverilog")
    ap.add_argument("--vvp", default="vvp")
    A = ap.parse_args()
    L = {"x4": libs.SUBVT, "hd": libs.HD}[A.lib]
    wls = A.workloads.split(",")
    hexes = {w: os.path.join(A.root, "prog", w + ".hex") for w in wls}
    # Golden result, store list and instruction count of every workload from the ISS.
    refs = {w: rv_iss.run(hexes[w]) for w in wls}
    for core in A.cores.split(","):
        out = os.path.join(A.out, A.lib, core)
        os.makedirs(out, exist_ok=True)
        t0 = time.time()
        vvp_rtl = compile_tb(A, core, out, False)
        net, B = synth(A, L, A.synlib, core, out)
        cnt = usage(L, net)
        vvp_gate = compile_tb(A, core, out, True)
        R = dict(core=core, lib=A.lib, cells=cnt, buffering=B, max_fanout=MAX_FANOUT, clk=CORES[core]["clk"],
                 drivers=drivers(L, net), workloads={})
        for w in wls:
            ref = refs[w]
            vcd = os.path.join(out, "gate_%s.vcd" % w)
            ok_rtl, cyc_rtl, _, tr_rtl = simulate(A, vvp_rtl, out, "rtl_" + w, hexes[w], ref["result"])
            ok, cyc, res, tr = simulate(A, vvp_gate, out, "gate_" + w, hexes[w], ref["result"], vcd)
            iss_ok = store_check(tr_rtl, ref) and store_check(tr, ref)
            lockstep = masked(tr) == masked(tr_rtl) and cyc == cyc_rtl
            act, ops = vcd_activity(vcd, PERIOD_NS) if os.path.exists(vcd) else ({}, 0)
            if os.path.exists(vcd):
                os.remove(vcd)
            R["workloads"][w] = dict(result=res, expect="%08x" % ref["result"], instret=ref["instret"], cycles_rtl=cyc_rtl,
                                     cycles=cyc, cpi=cyc / ref["instret"] if cyc else None, stores=len(tr), iss_match=iss_ok,
                                     lockstep=lockstep, sim_rtl=ok_rtl, sim_gate=ok, ops=ops, activity=act)
            print("%-3s %-6s %-8s cells %6d  rtl %s  gate %s  stores %4d vs ISS %s  RTL/gate lockstep %s  cycles %8s  CPI %6.2f  %5.0f s" %
                  (A.lib, core, w, sum(cnt.values()), "PASS" if ok_rtl else "FAIL", "PASS" if ok else "FAIL", len(tr),
                   "PASS" if iss_ok else "FAIL", "PASS" if lockstep else "FAIL", cyc, cyc / ref["instret"] if cyc else 0,
                   time.time() - t0), flush=True)
            if not (ok_rtl and ok and iss_ok and lockstep):
                sys.exit("verification failed for %s/%s/%s" % (A.lib, core, w))
        json.dump(R, open(os.path.join(out, "result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
