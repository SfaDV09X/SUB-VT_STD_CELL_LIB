#!/usr/bin/env python3
# OpenSTA timing and power of the synthesised cores (uses the setup from sta.py): Fmax from
# the critical path with FO4 output loads, then power at Fmax for each workload with its own
# switching activity. Energy per cycle = P / Fmax, energy per instruction = that x CPI.
# Writes <out>/sta_<lib>.json. Called by run_riscv_benchmark.sh; riscv_pvt.py reuses it for the other corners.

import argparse, json, os, re, sys
# The library tables (libs.py, libtools.py) live with the synthesis scripts.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "synthesis"))
import libs
from sta import header, sta, inv_cap

# Output load as a multiple of the library inverter input cap.
LOADS = {"x4": [("FO4", 4.0)], "hd": [("FO4", 4.0)]}


class Args:
    pass


# Input port bit names of the netlist (to tell port activity from internal nets).
def ports(net):
    names = set()
    for hi, lo, n in re.findall(r"^\s*input\s+(?:\[(\d+):(\d+)\]\s*)?(\w+)\s*;", open(net).read(), re.M):
        if hi:
            for i in range(min(int(hi), int(lo)), max(int(hi), int(lo)) + 1):
                names.add("%s[%d]" % (n, i))
        else:
            names.add(n)
    return names


# All workloads of one core at one corner and load.
def one(A, L, lib, core, tag, k):
    d = os.path.join(A.out, A.lib, core)
    R = json.load(open(os.path.join(d, "result.json")))
    top = "core_" + core
    net = os.path.join(d, top + "_gate.v")
    load = k * inv_cap(lib, L)
    S = Args()
    S.sta = A.sta
    # Same two-pass search as sta.py, starting from a period well above the expected delay.
    period = 1.0e9 if A.lib != "hd" else 1.0e3
    for _ in range(2):
        h = header(L, lib, net, "core_" + core, R["clk"], period, load)
        o = sta(S, h + ["report_checks -path_delay max -format full_clock_expanded -digits 4",
                        "puts \"WNS_MAX [sta::format_time [sta::worst_slack_cmd max] 6]\"",
                        "puts \"WNS_MIN [sta::format_time [sta::worst_slack_cmd min] 6]\""],
                os.path.join(d, "sta_%s.log" % tag))
        wmax = float(re.search(r"WNS_MAX\s+(\S+)", o).group(1))
        wmin = float(re.search(r"WNS_MIN\s+(\S+)", o).group(1))
        tcrit = period - wmax
        period = 2.0 * tcrit
    sp = re.search(r"Startpoint: (\S+)", o)
    ep = re.search(r"Endpoint: (\S+)", o)
    h = header(L, lib, net, top, R["clk"], tcrit, load)
    pn = ports(net)
    st = open(os.path.join(d, "stat.txt")).read()
    fmax = 1e9 / tcrit
    rows = []
    for w, W in R["workloads"].items():
        act = []
        for bit, (a, duty) in W["activity"].items():
            a = max(a, 1e-12)
            duty = min(max(duty, 1e-6), 1 - 1e-6)
            if bit in pn:
                act.append("set_power_activity -input_ports [get_ports {%s}] -activity %.9g -duty %.6g" % (bit, a, duty))
            elif bit in R["drivers"]:
                act.append("set_power_activity -pins [get_pins {%s}] -activity %.9g -duty %.6g" % (R["drivers"][bit], a, duty))
        o2 = sta(S, h + act + ["report_power -digits 6"], os.path.join(d, "power_%s_%s.log" % (tag, w)))
        m = re.search(r"(?m)^\s*Total\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)", o2)
        pint, psw, pleak, ptot = [float(x) for x in m.groups()]
        rows.append(dict(lib=A.lib, core=core, workload=w, load=tag, load_pf=load, cells=sum(R["cells"].values()),
                         ff=R["cells"][L["dff"][0]], area_um2=float(re.search(r"Chip area[^:]*:\s*([\d.]+)", st).group(1)),
                         tcrit_ns=tcrit, fmax_hz=fmax, hold_slack_ns=wmin, start=sp.group(1) if sp else "",
                         end=ep.group(1) if ep else "", cycles=W["cycles"], instret=W["instret"], cpi=W["cpi"],
                         ips=fmax / W["cpi"], p_int_w=pint, p_sw_w=psw, p_dyn_w=pint + psw, p_leak_w=pleak, p_tot_w=ptot,
                         uw_per_mhz=ptot / (fmax / 1e6) * 1e6, e_cycle_j=ptot / fmax, e_instr_j=ptot / fmax * W["cpi"],
                         e_prog_j=ptot / fmax * W["cycles"]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--lib", required=True, choices=["x4", "hd"])
    ap.add_argument("--stalib", required=True)
    ap.add_argument("--cores", default="serv,femto,pico,dark")
    ap.add_argument("--sta", default="sta")
    A = ap.parse_args()
    L = {"x4": libs.SUBVT, "hd": libs.HD}[A.lib]
    rows = []
    for core in A.cores.split(","):
        for tag, k in LOADS[A.lib]:
            for r in one(A, L, A.stalib, core, tag, k):
                rows.append(r)
                print("%-3s %-6s %-8s %s  Tcrit %12.3f ns  Fmax %11.4g Hz  hold %9.3f ns  P %.4e W  E/cycle %.4e J  E/instr %.4e J" %
                      (A.lib, core, r["workload"], tag, r["tcrit_ns"], r["fmax_hz"], r["hold_slack_ns"], r["p_tot_w"],
                       r["e_cycle_j"], r["e_instr_j"]), flush=True)
    json.dump(rows, open(os.path.join(A.out, "sta_%s.json" % A.lib), "w"), indent=1)


if __name__ == "__main__":
    main()
