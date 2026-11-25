#!/usr/bin/env python3
# Combine synth.py and sta.py results into synthesis/out/report: logic table (cell usage,
# equivalence, simulation), delay table, power table and the comparison with sky130_fd_sc_hd,
# as csv files plus one report.html.

import argparse, csv, html, json, os, sys
# The library tables (libs.py, libtools.py) live with the synthesis scripts.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "synthesis"))
import libs

FUNCS = ["inv1", "nand2", "nor2", "and2", "or2", "xor2", "xnor2", "aoi3", "oai3", "moai4", "maoi4"]


def fnum(x, f="%.4g"):
    return f % x


def table(head, rows):
    h = "<table border=1 cellspacing=0 cellpadding=4>\n<tr>%s</tr>\n" % "".join("<th>%s</th>" % html.escape(str(c)) for c in head)
    for r in rows:
        h += "<tr>%s</tr>\n" % "".join("<td align=center>%s</td>" % html.escape(str(c)) for c in r)
    return h + "</table>\n"


def write_csv(path, head, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--designs", default="rca8,counter8,demo")
    A = ap.parse_args()
    designs = A.designs.split(",")
    sta = {k: json.load(open(os.path.join(A.out, "sta_%s.json" % k))) for k in ("subvt", "hd") if os.path.isfile(os.path.join(A.out, "sta_%s.json" % k))}
    res = {(k, d): json.load(open(os.path.join(A.out, k, d, "result.json"))) for k in sta for d in designs}
    rep = os.path.join(A.out, "report")
    os.makedirs(rep, exist_ok=True)
    body = ["<html><head><title>Synthesis report</title></head><body>",
            "<h1>Synthesis and benchmark report</h1>",
            "<p>Sub-threshold library: subvt_sky130 X4, 0.4 V, 15 PVT corners. Reference: sky130_fd_sc_hd, tt 25 &deg;C, 1.8 V, "
            "restricted to the 13 equivalent cells. Delay = critical path with zero input/output delay, inverter-driven inputs and a "
            "4-inverter output load. Power at f = 1/T<sub>crit</sub> with switching activity from gate-level simulation. "
            "Energy per operation = total power &times; T<sub>crit</sub>.</p>"]

    head = ["library", "design", "cells", "area_um2", "library cells used", "equivalence", "gate-level sim"] + FUNCS + ["dff", "latch"]
    rows = []
    for k in sta:
        L = libs.LIBS[k]
        names = [L["cells"][f][0] for f in FUNCS] + [L["dff"][0], L["latch"][0]]
        for d in designs:
            R = res[(k, d)]
            r0 = next(x for x in sta[k] if x["design"] == d)
            rows.append([k, d, r0["cells"], fnum(r0["area"], "%.2f"), "%d/13" % r0["used"],
                         "PASS" if R["equiv"] else "FAIL", "PASS" if R["sim"] else "FAIL"] + [R["cells"][n] for n in names])
    write_csv(os.path.join(rep, "logic_table.csv"), head, rows)
    body += ["<h2>Logic table (cell usage)</h2>", table(head, rows)]

    head = ["library", "design", "corner", "Tcrit_ns", "fmax_Hz", "hold_slack_ns", "critical_start", "critical_end"]
    rows = [[x["lib"], x["design"], x["corner"], fnum(x["tcrit_ns"], "%.4f"), fnum(x["fmax_hz"]), fnum(x["hold_slack_ns"], "%.4f"), x["start"], x["end"]]
            for k in sta for x in sta[k]]
    write_csv(os.path.join(rep, "delay_table.csv"), head, rows)
    body += ["<h2>Delay table</h2>", table(head, rows)]

    head = ["library", "design", "corner", "P_internal_W", "P_switching_W", "P_leakage_W", "P_total_W", "E_dynamic_J", "E_leakage_J", "E_per_op_J"]
    rows = [[x["lib"], x["design"], x["corner"], fnum(x["p_int_w"]), fnum(x["p_sw_w"]), fnum(x["p_leak_w"]), fnum(x["p_tot_w"]),
             fnum(x["e_dyn_j"]), fnum(x["e_leak_j"]), fnum(x["e_op_j"])] for k in sta for x in sta[k]]
    write_csv(os.path.join(rep, "power_table.csv"), head, rows)
    body += ["<h2>Power table</h2>", table(head, rows)]

    if "hd" in sta and "subvt" in sta:
        head = ["design", "metric", "subvt 0.4 V tt 27 C", "hd 1.8 V tt 25 C", "subvt / hd"]
        rows = []
        for d in designs:
            s = next(x for x in sta["subvt"] if x["design"] == d and x["corner"] == "tt_27")
            h = next(x for x in sta["hd"] if x["design"] == d)
            for lab, key, f in (("area (um2)", "area", "%.2f"), ("cells", "cells", "%d"), ("critical delay (ns)", "tcrit_ns", "%.4g"),
                                ("fmax (Hz)", "fmax_hz", "%.4g"), ("total power at fmax (W)", "p_tot_w", "%.4g"),
                                ("leakage power (W)", "p_leak_w", "%.4g"), ("dynamic energy per op (J)", "e_dyn_j", "%.4g"),
                                ("energy per op (J)", "e_op_j", "%.4g")):
                rows.append([d, lab, f % s[key], f % h[key], "%.4g" % (s[key] / h[key]) if h[key] else "-"])
        write_csv(os.path.join(rep, "benchmark.csv"), head, rows)
        body += ["<h2>Benchmark against sky130_fd_sc_hd (1.8 V)</h2>", table(head, rows)]
    body.append("</body></html>")
    open(os.path.join(rep, "report.html"), "w").write("\n".join(body))
    print("wrote " + rep)


if __name__ == "__main__":
    main()
