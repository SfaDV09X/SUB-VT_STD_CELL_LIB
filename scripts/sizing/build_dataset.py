#!/usr/bin/env python3
import argparse
import glob
import os

import numpy as np
import pandas as pd

from spec import (area_um2, FANOUT, MAX_ASYM, MIN_NM_MV, NOMINAL, SWING, VDD_NOM, nm_col, parse_conds, tag)

KEY = ["Wn_um", "Wp_um", "Ln_um", "Lp_um"]
COND = ["corner", "temp_C", "VDD_V", "fanout", "load_F"]
SKIP = ("training_", "all_conditions", "cv_", "verify_designs", "evaluated_", "hv_", "feasibility_",
        "critical_check", "finalists_", "mc_summary")


def load_all(folder):
    frames = []
    for f in sorted(glob.glob(os.path.join(folder, "*.csv"))):
        name = os.path.basename(f)
        if name.startswith(SKIP):
            continue
        if os.path.getsize(f) == 0:
            print(f"  skip {name} (empty file)")
            continue
        d = pd.read_csv(f)
        if not {"Wn_um", "Wp_um", "Ln_um", "Lp_um", "status", "corner", "fanout", "VDD_V"} <= set(d.columns):
            continue
        d["source"] = name
        frames.append(d)
        print(f"  read {name:34s} {len(d):5d} rows")
    if not frames:
        raise SystemExit("No simulation CSV files found in " + folder)
    d = pd.concat(frames, ignore_index=True)
    key = ["Wn_um", "Wp_um", "Ln_um", "Lp_um", "corner", "temp_C", "VDD_V", "fanout"]
    n0 = len(d)
    d = d.drop_duplicates(key, keep="last").reset_index(drop=True)
    if len(d) < n0:
        print(f"  removed {n0 - len(d)} duplicate rows (same design and condition, e.g. after a resumed run)")
    return d


def derive(d):
    d["feasible_run"] = (d["status"] == "ok").astype(int)
    d["NM_mV"] = d["NM_min_V"] * 1e3
    d["NMH_mV"] = d["NMH_V"] * 1e3
    d["NML_mV"] = d["NML_V"] * 1e3
    d["Vm_mV"] = d["Vm_V"] * 1e3
    d["tp_ns"] = d["tp_max_s"] * 1e9
    d["tp_avg_ns"] = d["tp_avg_s"] * 1e9
    d["Edyn_fJ"] = d["dyn_energy_cycle_J"] * 1e15
    d["E_fJ"] = d["energy_op_J"] * 1e15
    d["PDP_fJ"] = d["pdp_J"] * 1e15
    d["EDP_fJns"] = d["edp_Js"] * 1e24
    leak_w = d["leakage_max_W"].fillna(d["leakage_avg_W"]) if "leakage_max_W" in d.columns else d["leakage_avg_W"]
    d["leak_pW"] = leak_w * 1e12
    d["area_um2"] = area_um2(d["Wn_um"], d["Wp_um"], d["Ln_um"], d["Lp_um"])
    d["swing_ok"] = ((d["vout_max_V"] >= (1 - SWING) * d["VDD_V"]) &
                     (d["vout_min_V"] <= SWING * d["VDD_V"])).astype(int)
    return d


def aggregate(d, conds, vdd, fanout, min_nm, max_asym):
    d = d[np.isclose(d["VDD_V"], vdd) & (d["fanout"] == fanout) & np.isclose(d["load_F"], 0.0)]
    out, incomplete, missing_count = [], 0, {}
    for key, g in d.groupby(KEY):
        have = {(r.corner, float(r.temp_C)): r for r in g.itertuples()}
        miss = [c for c in conds if c not in have]
        if miss:
            incomplete += 1
            for c in miss:
                missing_count[c] = missing_count.get(c, 0) + 1
            continue
        rs = [have[c] for c in conds]
        functional = all(r.status == "ok" and r.swing_ok == 1 for r in rs)
        nm = {c: r.NM_mV for c, r in zip(conds, rs) if np.isfinite(r.NM_mV)}
        nm_full = len(nm) == len(conds)
        row = dict(zip(KEY, key))
        row.update(
            area_um2=area_um2(*key),
            n_cond=len(conds),
            n_fail=sum(r.status != "ok" for r in rs),
            feasible=int(functional),
            NM_mV=min(nm.values()) if nm_full else np.nan,
            worst_NM_cond=tag(*min(nm, key=nm.get)) if nm_full else "",
            leak_pW=max((r.leak_pW for r in rs if np.isfinite(r.leak_pW)), default=np.nan),
        )
        if functional:
            tp = {c: r.tp_ns for c, r in zip(conds, rs)}
            row.update(tp_ns=max(tp.values()), worst_tp_cond=tag(*max(tp, key=tp.get)),
                       E_fJ=max(r.E_fJ for r in rs), Edyn_fJ=max(r.Edyn_fJ for r in rs),
                       PDP_fJ=max(r.PDP_fJ for r in rs), EDP_fJns=max(r.EDP_fJns for r in rs),
                       asym_tp_max=max(r.asym_tp for r in rs), asym_slew_max=max(r.asym_slew for r in rs))
        else:
            row.update(tp_ns=np.nan, worst_tp_cond="", E_fJ=np.nan, Edyn_fJ=np.nan, PDP_fJ=np.nan,
                       EDP_fJns=np.nan, asym_tp_max=np.nan, asym_slew_max=np.nan)
        nomr = have.get(NOMINAL)
        ok_nom = nomr is not None and nomr.status == "ok"
        row["asym_tp"] = nomr.asym_tp if ok_nom else np.nan
        row["asym_slew"] = nomr.asym_slew if ok_nom else np.nan
        row["Vm_dev_tt27"] = nomr.Vm_dev_norm if ok_nom else np.nan
        for c, r in zip(conds, rs):
            row[nm_col(*c)] = r.NM_mV
        row["meets_nm"] = int(nm_full and row["NM_mV"] >= min_nm)
        row["meets_asym"] = int(ok_nom and max(row["asym_tp"], row["asym_slew"]) <= max_asym)
        row["spec_pass"] = int(functional and row["meets_nm"] and row["meets_asym"])
        out.append(row)
    pvt = pd.DataFrame(out)
    print(f"\nPVT set: {len(conds)} conditions = " + ", ".join(tag(*c) for c in conds) + f" at {vdd:g} V, FO{fanout}")
    print(f"  designs simulated in ALL conditions: {len(pvt)}   (incomplete: {incomplete})")
    if len(pvt):
        print(f"  functional in every condition: {int(pvt.feasible.sum())}   failing somewhere: {int((1 - pvt.feasible).sum())}")
        print(f"  meet NM >= {min_nm:g} mV: {int(pvt.meets_nm.sum())}   meet asymmetry <= {max_asym:g} (tt@27): "
              f"{int(pvt.meets_asym.sum())}   meet everything: {int(pvt.spec_pass.sum())}")
    if incomplete and not len(pvt):
        print("  -> run subvt_dataset.py --mode sweep / --mode pvt first")
    if missing_count:
        top = sorted(missing_count.items(), key=lambda kv: -kv[1])[:5]
        print("  most often missing conditions:", ", ".join(f"{tag(*c)} x{n}" for c, n in top))
    return pvt


def critical_check(d, vdd, fanout):
    from spec import CRITICAL
    full = parse_conds(["full15"])
    d = d[np.isclose(d["VDD_V"], vdd) & (d["fanout"] == fanout) & np.isclose(d["load_F"], 0.0)]
    rows = []
    for key, g in d.groupby(KEY):
        have = {(r.corner, float(r.temp_C)): r for r in g.itertuples()}
        if not all(c in have for c in full) or not all(have[c].status == "ok" for c in full):
            continue
        rf = [have[c] for c in full]
        rc = [have[c] for c in CRITICAL]
        rows.append(dict(
            zip(KEY, key),
            NM_full=min(r.NM_mV for r in rf), NM_crit=min(r.NM_mV for r in rc),
            tp_full=max(r.tp_ns for r in rf), tp_crit=max(r.tp_ns for r in rc),
            E_full=max(r.E_fJ for r in rf), E_crit=max(r.E_fJ for r in rc),
            leak_full=max(r.leak_pW for r in rf), leak_crit=max(r.leak_pW for r in rc),
            NM_cond=tag(*full[int(np.argmin([r.NM_mV for r in rf]))]),
            tp_cond=tag(*full[int(np.argmax([r.tp_ns for r in rf]))])))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--vdd", type=float, default=VDD_NOM)
    ap.add_argument("--fanout", type=int, default=FANOUT)
    ap.add_argument("--conds", nargs="+", default=["critical"])
    ap.add_argument("--min-nm", type=float, default=MIN_NM_MV)
    ap.add_argument("--max-asym", type=float, default=MAX_ASYM)
    a = ap.parse_args()

    d = load_all(a.dir)
    for c in KEY:
        d[c] = d[c].round(4)
    d["temp_C"] = d["temp_C"].astype(float)
    d["_ok"] = (d["status"] == "ok").astype(int)
    d = d.sort_values("_ok", ascending=False)
    n0 = len(d)
    d = d.drop_duplicates(KEY + COND, keep="first").drop(columns="_ok")
    print(f"\n{n0} rows -> {len(d)} unique (design, condition) rows")
    d = derive(d)

    out_dir = a.out or a.dir
    os.makedirs(out_dir, exist_ok=True)
    d.to_csv(os.path.join(out_dir, "all_conditions.csv"), index=False)

    conds = parse_conds(a.conds)
    pvt = aggregate(d, conds, a.vdd, a.fanout, a.min_nm, a.max_asym)
    out_p = os.path.join(out_dir, "training_pvt.csv")
    pvt.to_csv(out_p, index=False)

    chk = critical_check(d, a.vdd, a.fanout)
    if len(chk):
        chk.to_csv(os.path.join(out_dir, "critical_check.csv"), index=False)
        print(f"\nCritical-set validation on {len(chk)} designs simulated OK at all 15 conditions:")
        for k, lab in (("NM", "worst NM"), ("tp", "worst tp"), ("E", "worst E_op"), ("leak", "worst leakage")):
            e = (chk[f"{k}_crit"] - chk[f"{k}_full"]) / chk[f"{k}_full"].abs().clip(lower=1e-12) * 100
            if k == "NM":
                e = chk["NM_crit"] - chk["NM_full"]
                print(f"  {lab:14s}: critical-set minus full-15, max |diff| = {e.abs().max():.3f} mV, "
                      f"designs with a different worst condition: {int((e.abs() > 1e-9).sum())}")
            else:
                print(f"  {lab:14s}: critical-set vs full-15, max |error| = {e.abs().max():.3f} %")
    print(f"\nSaved:\n  {os.path.join(out_dir, 'all_conditions.csv')}\n  {out_p}")


if __name__ == "__main__":
    main()
