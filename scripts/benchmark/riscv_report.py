#!/usr/bin/env python3
# Tables for the RISC-V benchmark from sta_x4.json and sta_hd.json: suite summary (totals over
# all workloads), energy per instruction and per cycle by workload with the X4 saving, and CPI.
# Writes riscv_results.md and riscv_results.csv in the output folder.

import argparse, csv, json, os

CORES = [("serv", "SERV"), ("femto", "FemtoRV32 Quark"), ("pico", "PicoRV32"), ("dark", "DarkRISCV")]
NAMES = {"x4": "X4, 0.40 V", "hd": "hd, 1.80 V"}
KEYS = ["core", "library", "workload", "cells", "flip_flops", "area_um2", "fmax_hz", "instructions", "cycles", "cpi",
        "instructions_per_s", "p_total_w", "p_dynamic_w", "p_leakage_w", "uw_per_mhz", "energy_per_cycle_j",
        "energy_per_instr_j", "energy_program_j"]


# Number with an SI prefix, e.g. 1.23 µJ.
def si(v, unit):
    for f, p in ((1e9, "G"), (1e6, "M"), (1e3, "k"), (1.0, ""), (1e-3, "m"), (1e-6, "µ"), (1e-9, "n"), (1e-12, "p"), (1e-15, "f")):
        if abs(v) >= f:
            return ("%.3g %s%s" % (v / f, p, unit)).strip()
    return "%.3g %s" % (v, unit)


# Suite totals: CPI = cycles / instructions, energy per instruction and per cycle from the total
# program energy, and the average power over the whole suite.
def suite(rows):
    e = sum(r["e_prog_j"] for r in rows)
    n = sum(r["instret"] for r in rows)
    c = sum(r["cycles"] for r in rows)
    return dict(cpi=c / n, epi=e / n, epc=e / c, ptot=e / (c / rows[0]["fmax_hz"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    rows = []
    for lib in ("x4", "hd"):
        p = os.path.join(A.out, "sta_%s.json" % lib)
        if os.path.exists(p):
            rows += json.load(open(p))
    wls = list(dict.fromkeys(r["workload"] for r in rows))
    R = {(r["lib"], r["core"], r["workload"]): r for r in rows}
    cores = [(c, n) for c, n in CORES if ("x4", c, wls[0]) in R and ("hd", c, wls[0]) in R]
    md = ["# RISC-V core benchmark: X4 vs sky130_fd_sc_hd at FO4", "",
          "Workloads: " + ", ".join("%s (%d instructions)" % (w, R[("x4", cores[0][0], w)]["instret"]) for w in wls) + ".",
          "Suite values are totals over all workloads: CPI = cycles / instructions, energy per instruction = energy / instructions, energy per cycle = energy / cycles.", "",
          "## Suite summary", "",
          "| Core | Library | Cells | Area (mm²) | Fmax | CPI | Instructions/s | Power at Fmax | Leakage | Energy/cycle | Energy/instr | Energy/instr vs hd |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c, name in cores:
        sx = suite([R[("x4", c, w)] for w in wls])
        sh = suite([R[("hd", c, w)] for w in wls])
        for lib, S in (("x4", sx), ("hd", sh)):
            r = R[(lib, c, wls[0])]
            leak = r["p_leak_w"]
            md.append("| %s | %s | %d | %.3f | %s | %.2f | %s | %s | %s | %s | %s | %s |" % (
                name, NAMES[lib], r["cells"], r["area_um2"] / 1e6, si(r["fmax_hz"], "Hz"), S["cpi"], si(r["fmax_hz"] / S["cpi"], ""),
                si(S["ptot"], "W"), si(leak, "W"), si(S["epc"], "J"), si(S["epi"], "J"),
                "%.1f× lower" % (sh["epi"] / sx["epi"]) if lib == "x4" else "reference"))
    for title, key in (("Energy per instruction", "e_instr_j"), ("Energy per cycle", "e_cycle_j")):
        md += ["", "## %s by workload" % title, "",
               "| Core | Library | " + " | ".join(wls) + " |", "|---|---|" + "---|" * len(wls)]
        for c, name in cores:
            for lib in ("x4", "hd"):
                md.append("| %s | %s | %s |" % (name, NAMES[lib], " | ".join(si(R[(lib, c, w)][key], "J") for w in wls)))
            md.append("| %s | X4 saving | %s |" % (name, " | ".join("%.1f×" % (R[("hd", c, w)][key] / R[("x4", c, w)][key]) for w in wls)))
    md += ["", "## CPI by workload", "", "| Core | " + " | ".join(wls) + " |", "|---|" + "---|" * len(wls)]
    for c, name in cores:
        md.append("| %s | %s |" % (name, " | ".join("%.2f" % R[("x4", c, w)]["cpi"] for w in wls)))
    with open(os.path.join(A.out, "riscv_results.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(KEYS)
        for r in rows:
            wr.writerow([r["core"], r["lib"], r["workload"], r["cells"], r["ff"], r["area_um2"], r["fmax_hz"], r["instret"],
                         r["cycles"], r["cpi"], r["ips"], r["p_tot_w"], r["p_dyn_w"], r["p_leak_w"], r["uw_per_mhz"],
                         r["e_cycle_j"], r["e_instr_j"], r["e_prog_j"]])
    open(os.path.join(A.out, "riscv_results.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
