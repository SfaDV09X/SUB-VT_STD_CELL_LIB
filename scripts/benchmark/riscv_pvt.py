#!/usr/bin/env python3
# Timing, power and energy of every core and workload at all 15 X4 corners. The netlist and
# switching activity come from the tt 27 C run; only the Liberty file changes per corner.
# Writes <out>/pvt_x4.json and riscv_pvt_x4.csv.

import argparse, csv, glob, json, os, sys
# The library tables (libs.py, libtools.py) live with the synthesis scripts.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "synthesis"))
import libs
from riscv_sta import one


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--libdir", required=True)
    ap.add_argument("--cores", default="serv,femto,pico,dark")
    ap.add_argument("--sta", default="sta")
    A = ap.parse_args()
    A.lib = "x4"
    rows = []
    for f in sorted(glob.glob(os.path.join(A.libdir, "*", "subvt_sky130_*_0p40v_*.lib"))):
        corner = os.path.basename(os.path.dirname(f))
        for core in A.cores.split(","):
            for r in one(A, libs.SUBVT, f, core, "FO4_" + corner, 4.0):
                r["corner"] = corner
                rows.append(r)
                print("%-6s %-6s %-8s Fmax %10.1f Hz  hold %9.1f ns  P %.3e W  leakage %.3e W  E/cycle %.3e J  E/instr %.3e J" %
                      (corner, core, r["workload"], r["fmax_hz"], r["hold_slack_ns"], r["p_tot_w"], r["p_leak_w"],
                       r["e_cycle_j"], r["e_instr_j"]), flush=True)
    json.dump(rows, open(os.path.join(A.out, "pvt_x4.json"), "w"), indent=1)
    keys = ["corner", "core", "workload", "fmax_hz", "tcrit_ns", "hold_slack_ns", "cpi", "p_tot_w", "p_dyn_w", "p_leak_w",
            "e_cycle_j", "e_instr_j"]
    with open(os.path.join(A.out, "riscv_pvt_x4.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(keys)
        w.writerows([[r[k] for k in keys] for r in rows])


if __name__ == "__main__":
    main()
