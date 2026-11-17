#!/usr/bin/env python3
import argparse
import os

import numpy as np
import pandas as pd

from spec import (FANOUT, MAX_ASYM, MIN_NM_MV, NOMINAL, SWING, VDD_NOM, parse_conds, tag)

KEY = ["Wn_um", "Wp_um", "Ln_um", "Lp_um"]
NEEDED = ["NM_min_V", "NMH_V", "NML_V", "Vm_V", "tp_max_s", "energy_op_J", "leakage_avg_W", "asym_tp", "asym_slew"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--vdd", type=float, default=VDD_NOM)
    ap.add_argument("--fanout", type=int, default=FANOUT)
    ap.add_argument("--swing", type=float, default=SWING)
    ap.add_argument("--min-nm", type=float, default=MIN_NM_MV)
    ap.add_argument("--max-asym", type=float, default=MAX_ASYM)
    ap.add_argument("--conds", nargs="+", default=["critical"])
    a = ap.parse_args()

    path = os.path.join(a.dir, "all_conditions.csv")
    if not os.path.exists(path):
        raise SystemExit(f"{path} not found - run: python3 build_dataset.py --dir {a.dir}")
    d = pd.read_csv(path)
    d = d[np.isclose(d["VDD_V"], a.vdd) & (d["fanout"] == a.fanout) & np.isclose(d["load_F"], 0.0)].copy()
    d["temp_C"] = d["temp_C"].astype(float)
    d["cond"] = [tag(c, t) for c, t in zip(d["corner"], d["temp_C"])]
    req = [tag(*c) for c in parse_conds(a.conds)]

    d["f_status"] = d["status"] == "ok"
    d["f_swing"] = (d["vout_max_V"] >= (1 - a.swing) * a.vdd) & (d["vout_min_V"] <= a.swing * a.vdd)
    d["f_nm"] = (d["NMH_V"] * 1e3 >= a.min_nm) & (d["NML_V"] * 1e3 >= a.min_nm)
    d["f_data"] = np.isfinite(d[NEEDED]).all(axis=1)
    d["feasible"] = d[["f_status", "f_swing", "f_nm", "f_data"]].all(axis=1)
    nom = tag(*NOMINAL)
    d["f_asym"] = (d["asym_tp"] <= a.max_asym) & (d["asym_slew"] <= a.max_asym)

    print(f"{len(d)} simulations, {d.groupby(KEY).ngroups} unique designs, {d['cond'].nunique()} conditions, "
          f"NM floor {a.min_nm:g} mV, asymmetry limit {a.max_asym:g} (applied at {nom})\n")

    print("=== 1. Feasibility per corner / temperature (functional + NM floor) ===")
    rows = []
    for c in req:
        g = d[d["cond"] == c]
        if g.empty:
            rows.append(dict(condition=c, designs=0))
            continue
        ok = g[g.feasible]
        rows.append(dict(
            condition=c, designs=len(g), feasible=len(ok), pct=f"{100 * len(ok) / len(g):.0f}%",
            no_switch=int((g.status == "no_switch").sum()), no_gain=int((g.status == "no_gain").sum()),
            sim_fail=int((g.status == "sim_fail").sum()),
            bad_swing=int((g.f_status & ~g.f_swing).sum()),
            bad_NM=int((g.f_status & g.f_swing & ~g.f_nm).sum()),
            medianNM_mV=round(float(np.median(ok.NM_min_V)) * 1e3, 1) if len(ok) else np.nan,
            minNM_mV=round(float(ok.NM_min_V.min()) * 1e3, 1) if len(ok) else np.nan,
        ))
    t1 = pd.DataFrame(rows)
    for col in ["designs", "feasible", "no_switch", "no_gain", "sim_fail", "bad_swing", "bad_NM"]:
        if col in t1:
            t1[col] = t1[col].astype("Int64")
    print(t1.astype(object).where(t1.notna(), "-").to_string(index=False))

    print("\n=== 2. Feasibility per design ===")
    out = []
    for key, g in d.groupby(KEY):
        have = set(g["cond"])
        bad = sorted(g.loc[~g.feasible & g["cond"].isin(req), "cond"])
        cov = [c for c in req if c in have]
        nomrow = g[g["cond"] == nom]
        asym_ok = bool(len(nomrow) and nomrow["f_asym"].iloc[0])
        complete = len(cov) == len(req)
        out.append(dict(zip(KEY, key), conditions_simulated=len(cov), conditions_required=len(req),
                        complete=complete, n_infeasible=len(bad), infeasible_in=",".join(bad),
                        feasible_everywhere=complete and not bad, asym_ok_tt27=asym_ok,
                        spec_pass=complete and not bad and asym_ok,
                        worst_NM_mV=round(float(g.loc[g["cond"].isin(req), "NM_min_V"].min()) * 1e3, 1)))
    des = pd.DataFrame(out)
    comp = des[des.complete]
    print(f"designs simulated in all {len(req)} conditions : {len(comp)} of {len(des)}")
    print(f"  functional with NM >= floor in EVERY condition : {int(comp.feasible_everywhere.sum())}")
    print(f"  ... and asymmetry <= limit at {nom}            : {int(comp.spec_pass.sum())}")
    part = des[~des.complete]
    if len(part):
        print(f"designs with only some conditions simulated: {len(part)}")

    print("\n=== 3. Why simulations fail ===")
    bad = d[~d.feasible]
    if bad.empty:
        print("no infeasible simulations")
    else:
        why = pd.Series({
            "status != ok (no_switch / no_gain / sim_fail)": int((~bad.f_status).sum()),
            "output swing too small": int((bad.f_status & ~bad.f_swing).sum()),
            "noise margin below floor": int((bad.f_status & bad.f_swing & ~bad.f_nm).sum()),
            "missing / non-finite metric": int((bad.f_status & bad.f_swing & bad.f_nm & ~bad.f_data).sum()),
        })
        print(why.to_string())
        print("\nfailing simulations by condition:")
        print(bad["cond"].value_counts().to_string())
        for col in ("Wp_um", "Wn_um", "Lp_um", "Ln_um"):
            r = d.groupby(col).feasible.agg(["size", "sum"])
            r["fail_%"] = (100 * (1 - r["sum"] / r["size"])).round(0)
            print(f"\nfailure rate by {col}:")
            print(r.rename(columns={"size": "sims", "sum": "feasible"}).to_string())

    print("\n=== 4. Data sanity ===")
    okd = d[d.f_status]
    print(f"status ok rows with NaN in a needed metric : {int((~okd.f_data).sum())}")
    print(f"non-positive energy / leakage              : {int(((okd.energy_op_J <= 0) | (okd.leakage_avg_W <= 0)).sum())}")
    print(f"NM < 0 (inconsistent VTC)                  : {int((okd.NM_min_V < 0).sum())}")
    print(f"Vm outside 25-75% of VDD                   : "
          f"{int(((okd.Vm_V < 0.25 * a.vdd) | (okd.Vm_V > 0.75 * a.vdd)).sum())}")
    print(f"duplicate (design, condition) rows         : {int(d.duplicated(KEY + ['corner', 'temp_C']).sum())}")

    d.drop(columns=["f_data"]).assign(f_data=d["f_data"]).to_csv(os.path.join(a.dir, "feasibility_by_condition.csv"), index=False)
    des.to_csv(os.path.join(a.dir, "feasibility_by_design.csv"), index=False)
    print("\nSaved feasibility_by_condition.csv and feasibility_by_design.csv")

    print("\n=== Verdict ===")
    if len(comp) == 0:
        print("No design has been simulated in every required condition yet.")
    else:
        n_f = int(comp.spec_pass.sum())
        print(f"{n_f} designs pass every criterion ({100 * n_f / len(comp):.0f}% of {len(comp)} complete designs).")
        if n_f < 15:
            print("Fewer than 15 passing designs: the surrogate will be weak. Simulate more designs or "
                  "revisit the NM floor / asymmetry limit / design box.")


if __name__ == "__main__":
    main()
