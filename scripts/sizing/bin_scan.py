#!/usr/bin/env python3
import argparse
import os
import shutil

import numpy as np

import subvt_dataset as m
from spec import FINGER_MAX

WP = [round(0.42 * k, 2) for k in range(1, 7)]
WN = [round(0.42 * k, 2) for k in range(2, 13)]
LG = [round(0.15 + 0.01 * k, 2) for k in range(0, 16)]


def dc_point(wn, wp, ln, lp, corner, temp, vdd):
    rd = os.path.join(m.RUNS_DIR, f"binscan_{os.getpid()}")
    shutil.rmtree(rd, ignore_errors=True)
    os.makedirs(rd)
    name, ports, block = m.load_subckt(m.CELL_NETLIST)
    b = m.set_widths(block, wn, wp, ln, lp)
    try:
        with open(os.path.join(rd, "tb_vec.cir"), "w") as f:
            f.write(m.build_vec_tb(b, name, ports, corner, vdd, temp))
        m.run_ngspice(rd, "tb_vec.cir", f"vec_{len(m.vectors()) - 1}.txt")
        vec = m.read_vectors(rd, vdd)
        dc, ok, _ = m.dc_cell(b, name, ports, corner, vdd, temp, 4, 0.0, rd)
    except RuntimeError:
        return None
    dc["leak_pW"] = max(x[1] for x in vec.values()) * 1e12
    dc["func_ok"] = m.function_ok(vec, vdd)
    return dc


def reversals(y):
    d = np.sign(np.diff(np.asarray(y, float)))
    d = d[d != 0]
    return int(np.sum(d[1:] != d[:-1]))


def scan(label, var, grid, base, corner, vdd):
    print(f"\n{label}")
    print(f"{var:>6s}  Vm_mV  NM_mV  leak_pW")
    leaks = []
    for w in grid:
        d = dict(base)
        d[var] = w
        dc = dc_point(d["Wn"], d["Wp"], d["Ln"], d["Lp"], corner, temp, vdd)
        if dc is None:
            print(f"{w:6.2f}  model/ngspice error")
            continue
        leaks.append(dc["leak_pW"])
        print(f"{w:6.2f}  {dc.get('Vm_V', np.nan) * 1e3:5.1f}  {dc.get('NM_min_V', np.nan) * 1e3:5.1f}  {dc['leak_pW']:7.3f}" + ("" if dc["func_ok"] else "  WRONG FUNCTION"))
    print(f"leakage direction reversals along {var}: {reversals(leaks)} (a smooth device model gives 0)")


def main():
    global temp
    ap = argparse.ArgumentParser()
    ap.add_argument("--corner", default="tt")
    ap.add_argument("--temp", type=float, default=27.0)
    ap.add_argument("--vdd", type=float, default=m.VDD_NOM)
    ap.add_argument("--wn", type=float, default=2.52)
    ap.add_argument("--wp", type=float, default=0.84)
    ap.add_argument("--ln", type=float, default=0.15)
    ap.add_argument("--lp", type=float, default=0.18)
    ap.add_argument("--vars", nargs="+", default=["Wp", "Wn", "Lp", "Ln"])
    a = ap.parse_args()
    temp = a.temp
    print("Netlist:", m.CELL_NETLIST)
    print("Models :", m.MODEL_LIB)
    base = {"Wn": a.wn, "Wp": a.wp, "Ln": a.ln, "Lp": a.lp}
    tg = f"{a.corner}@{a.temp:g}C"
    print(f"base: Wn={a.wn:g} Wp={a.wp:g} Ln={a.ln:g} Lp={a.lp:g}; fingers capped at {FINGER_MAX:g} um")
    grids = {"Wp": WP, "Wn": WN, "Lp": LG, "Ln": LG}
    for v in a.vars:
        scan(f"{v} scan, {tg}", v, grids[v], base, a.corner, a.vdd)


if __name__ == "__main__":
    main()
