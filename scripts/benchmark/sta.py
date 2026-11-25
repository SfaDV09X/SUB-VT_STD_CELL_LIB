#!/usr/bin/env python3
# OpenSTA timing and power of the synthesised benchmark designs, per corner. Critical path
# with zero I/O delay, inputs driven by the library inverter and outputs loaded with 4
# inverter inputs; power at f = 1/Tcrit with the activity from gate-level simulation.
# Writes <out>/sta_<lib>.json for report.py. Called by run_benchmark.sh.

import argparse, json, os, re, subprocess, sys
# The library tables (libs.py, libtools.py) live with the synthesis scripts.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "synthesis"))
import libs

# Which Liberty file to use per library and corner; the hd reference only has tt 25 C.
LIBFILE = {
    "subvt": lambda A, p, t: os.path.join(A.libdir, "%s_%dc" % (p, t), "subvt_sky130_%s_0p40v_%dc.lib" % (p, t)),
    "hd": lambda A, p, t: A.hdlib,
}
CORNERS = {"subvt": libs.CORNERS, "hd": [("tt", 25)]}


# Input cap of the library inverter (FO4 load = 4x this).
def inv_cap(lib, L):
    t = open(lib).read()
    s, e = libs.cell_map(t)[L["cells"]["inv1"][0]]
    b = t[s:e]
    m = re.search(r'pin\s*\(\s*"?%s"?\s*\)\s*\{(.*?)\}' % L["cells"]["inv1"][1]["a"], b, re.S)
    return float(re.search(r"\bcapacitance\s*:\s*([0-9.eE+-]+)", m.group(1)).group(1))


# SDC part of the OpenSTA script.
def header(L, lib, net, top, clk, period, load):
    inv, ip, io = L["cells"]["inv1"]
    s = ["read_liberty %s" % lib, "read_verilog %s" % net, "link_design %s_gate" % top]
    if clk:
        s.append("create_clock -name clk -period %.6f [get_ports %s]" % (period, clk))
        s.append("set ins [lsearch -all -inline -not -exact [all_inputs] [get_ports %s]]" % clk)
        s.append("set_input_delay 0 -clock clk $ins")
    else:
        s.append("create_clock -name vclk -period %.6f" % period)
        s.append("set ins [all_inputs]")
        s.append("set_input_delay 0 -clock vclk $ins")
    s.append("set_output_delay 0 -clock %s [all_outputs]" % ("clk" if clk else "vclk"))
    s.append("set_driving_cell -lib_cell %s -pin %s $ins" % (inv, io))
    s.append("set_load %.6g [all_outputs]" % load)
    return s


def sta(A, tcl, log):
    open(log.replace(".log", ".tcl"), "w").write("\n".join(tcl) + "\n")
    r = subprocess.run([A.sta, "-no_splash", "-exit", log.replace(".log", ".tcl")], capture_output=True, text=True)
    open(log, "w").write(r.stdout + r.stderr)
    if r.returncode != 0 or "Error" in r.stdout + r.stderr:
        sys.exit("OpenSTA failed, see " + log)
    return r.stdout


def one(A, L, design, p, t):
    d = os.path.join(A.out, L["name"], design)
    R = json.load(open(os.path.join(d, "result.json")))
    lib = LIBFILE[L["name"]](A, p, t)
    net = os.path.join(d, design + "_gate.v")
    load = 4.0 * inv_cap(lib, L)
    tag = "%s_%d" % (p, t)
    # First pass with a huge period to read the critical path, second pass with 2x that delay
    # to get the hold slack and paths at a realistic clock; Tcrit is taken from the last pass.
    period = 1.0e8
    for _ in range(2):
        h = header(L, lib, net, design, R["clk"], period, load)
        o = sta(A, h + ["report_checks -path_delay max -format full_clock_expanded -digits 4 -fields {slew cap input_pins}",
                        "report_checks -path_delay min -digits 4",
                        "puts \"WNS_MAX [sta::format_time [sta::worst_slack_cmd max] 6]\"",
                        "puts \"WNS_MIN [sta::format_time [sta::worst_slack_cmd min] 6]\""],
                os.path.join(d, "sta_%s.log" % tag))
        wmax = float(re.search(r"WNS_MAX\s+(\S+)", o).group(1))
        wmin = float(re.search(r"WNS_MIN\s+(\S+)", o).group(1))
        tcrit = period - wmax
        period = 2.0 * tcrit
    sp = re.search(r"Startpoint: (\S+)", o)
    ep = re.search(r"Endpoint: (\S+)", o)
    h = header(L, lib, net, design, R["clk"], tcrit, load)
    act = []
    ports = set(re.findall(r"^\s*input\s+(?:\[(\d+):(\d+)\]\s*)?(\w+)\s*;", open(net).read(), re.M))
    pnames = set()
    for hi, lo, n in ports:
        if hi:
            for i in range(min(int(hi), int(lo)), max(int(hi), int(lo)) + 1):
                pnames.add("%s[%d]" % (n, i))
        else:
            pnames.add(n)
    # Per-bit activity from simulation, on input ports or on the driving cell pin.
    for bit, (a, duty) in R["activity"].items():
        a = max(a, 1e-12)
        duty = min(max(duty, 1e-6), 1 - 1e-6)
        if bit in pnames:
            act.append("set_power_activity -input_ports [get_ports {%s}] -activity %.9g -duty %.6g" % (bit, a, duty))
        elif bit in R["drivers"]:
            act.append("set_power_activity -pins [get_pins {%s}] -activity %.9g -duty %.6g" % (R["drivers"][bit], a, duty))
    o2 = sta(A, h + act + ["report_power -digits 6"],
             os.path.join(d, "power_%s.log" % tag))
    m = re.search(r"(?m)^\s*Total\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)", o2)
    pint, psw, pleak, ptot = [float(x) for x in m.groups()]
    return dict(lib=L["name"], design=design, corner=tag, area=float(re.search(r"Chip area[^:]*:\s*([\d.]+)", open(os.path.join(d, "stat.txt")).read()).group(1)),
                cells=sum(R["cells"].values()), used=sum(1 for v in R["cells"].values() if v), load_pf=load,
                tcrit_ns=tcrit, fmax_hz=1e9 / tcrit, hold_slack_ns=wmin, start=sp.group(1) if sp else "", end=ep.group(1) if ep else "",
                p_int_w=pint, p_sw_w=psw, p_leak_w=pleak, p_tot_w=ptot,
                e_dyn_j=(pint + psw) * tcrit * 1e-9, e_leak_j=pleak * tcrit * 1e-9, e_op_j=ptot * tcrit * 1e-9, ops_sim=R["ops"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--libdir", default="")
    ap.add_argument("--hdlib", default="")
    ap.add_argument("--lib", required=True, choices=list(libs.LIBS))
    ap.add_argument("--designs", default="rca8,counter8,demo")
    ap.add_argument("--sta", default="sta")
    A = ap.parse_args()
    L = libs.LIBS[A.lib]
    rows = []
    for design in A.designs.split(","):
        for p, t in CORNERS[A.lib]:
            r = one(A, L, design, p, t)
            rows.append(r)
            print("%-6s %-9s %-6s Tcrit %12.3f ns  hold %10.3f ns  P %.4e W  E/op %.4e J" %
                  (A.lib, design, r["corner"], r["tcrit_ns"], r["hold_slack_ns"], r["p_tot_w"], r["e_op_j"]), flush=True)
    json.dump(rows, open(os.path.join(A.out, "sta_%s.json" % A.lib), "w"), indent=1)


if __name__ == "__main__":
    main()
