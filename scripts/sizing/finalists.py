#!/usr/bin/env python3
import argparse
import os

import numpy as np
import pandas as pd

from spec import (area_um2, FANOUT, MAX_ASYM, MC_SIGMA_K, MIN_NM_MV, NOMINAL, VDD_NM_FRAC, VDD_NOM, VDD_TOL, parse_conds, tag)

KEY = ["Wn_um", "Wp_um", "Ln_um", "Lp_um"]


def hv_report(a, raw, out):
    tp = os.path.join(a.dir, "training_pvt.csv")
    if not os.path.exists(tp) or "NM_wc_mV" not in out:
        return
    from pymoo.indicators.hv import HV
    tr = pd.read_csv(tp)
    tr = tr[tr.feasible == 1]
    if len(tr) < 2 or "method" not in raw:
        return
    f = np.c_[-tr.NM_mV, np.log10(tr.tp_ns), np.log10(tr.E_fJ), np.log10(tr.leak_pW), area_um2(tr.Wn_um, tr.Wp_um, tr.Ln_um, tr.Lp_um)]
    lo, hi = f.min(0), f.max(0)
    hi = np.where(hi - lo < 1e-12, lo + 1.0, hi)
    o = out.copy()
    o["pass_all_core"] = ((o.get("pass_nm", 0) == 1) & (o.get("pass_asym", 0) == 1)).astype(int)
    print("\nhypervolume of the SPICE-verified designs per method (normalised with the training ranges, ref 1.1):")
    for method, g in raw.groupby("method"):
        m = g[KEY].drop_duplicates().merge(o, on=KEY, how="left")
        m = m[(m.pass_all_core == 1) & m.NM_wc_mV.notna()]
        if m.empty:
            print(f"  {method:8s}: no verified design passes the criteria")
            continue
        F = np.c_[-m.NM_wc_mV, np.log10(m.tp_wc_ns), np.log10(m.E_op_wc_fJ), np.log10(m.leak_wc_pW),
                  area_um2(m.Wn_um, m.Wp_um, m.Ln_um, m.Lp_um)]
        Fn = (F - lo) / (hi - lo)
        Fn = Fn[np.all(Fn < 1.1, axis=1)]
        v = float(HV(ref_point=np.full(5, 1.1))(Fn)) if len(Fn) else 0.0
        print(f"  {method:8s}: {len(m)} passing designs, SPICE hypervolume = {v:.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--designs", default="verify_designs.csv")
    ap.add_argument("--mc", default="mc_samples.csv")
    ap.add_argument("--min-nm", type=float, default=MIN_NM_MV)
    ap.add_argument("--max-asym", type=float, default=MAX_ASYM)
    ap.add_argument("--fanout", type=int, default=FANOUT)
    ap.add_argument("--vdd-check", action="store_true", help="also require the VDD -10 %% / +10 %% checks")
    a = ap.parse_args()

    ac = pd.read_csv(os.path.join(a.dir, "all_conditions.csv"))
    ac = ac[(ac["fanout"] == a.fanout) & np.isclose(ac["load_F"], 0.0)].copy()
    ac["temp_C"] = ac["temp_C"].astype(float)
    raw = pd.read_csv(os.path.join(a.dir, a.designs))
    for c in KEY:
        raw[c] = raw[c].round(4)
    des = raw[KEY].drop_duplicates()
    full = parse_conds(["full15"])
    vlo, vhi = round(VDD_NOM * (1 - VDD_TOL), 4), round(VDD_NOM * (1 + VDD_TOL), 4)

    mc = None
    mp = os.path.join(a.dir, a.mc)
    if os.path.exists(mp):
        mc = pd.read_csv(mp)
        mc = mc[mc["status"].isin(["ok", "no_gain"])].copy()
        mc["NM_mV"] = mc["NM_min_V"] * 1e3
        for c in KEY:
            mc[c] = mc[c].round(4)

    rows = []
    for wn, wp, ln, lp in des[KEY].itertuples(index=False):
        g = ac[np.isclose(ac.Wn_um, wn) & np.isclose(ac.Wp_um, wp) & np.isclose(ac.Ln_um, ln) & np.isclose(ac.Lp_um, lp)]
        r = {"Wn_um": wn, "Wp_um": wp, "Ln_um": ln, "Lp_um": lp}
        nom = g[np.isclose(g.VDD_V, VDD_NOM)]
        have = {(x.corner, x.temp_C): x for x in nom.itertuples()}
        n_ok = sum(1 for c in full if c in have and have[c].status == "ok")
        r["pvt_ok"] = f"{n_ok}/{len(full)}"
        if n_ok == len(full):
            rs = [have[c] for c in full]
            nmv = [x.NM_mV for x in rs]
            r["NM_wc_mV"] = min(nmv)
            r["NM_wc_at"] = tag(*full[int(np.argmin(nmv))])
            tpv = [x.tp_ns for x in rs]
            r["tp_wc_ns"] = max(tpv)
            r["tp_wc_at"] = tag(*full[int(np.argmax(tpv))])
            r["E_op_wc_fJ"] = max(x.E_fJ for x in rs)
            r["PDP_wc_fJ"] = max(x.PDP_fJ for x in rs)
            r["EDP_wc_fJns"] = max(x.EDP_fJns for x in rs)
            r["leak_wc_pW"] = max(x.leak_pW for x in rs)
            r["tp_tt27_ns"] = have[NOMINAL].tp_ns
            r["E_op_tt27_fJ"] = have[NOMINAL].E_fJ
            r["PDP_tt27_fJ"] = have[NOMINAL].PDP_fJ
            r["asym_tp_tt27"] = have[NOMINAL].asym_tp
            r["asym_slew_tt27"] = have[NOMINAL].asym_slew
            r["Vm_dev_tt27"] = have[NOMINAL].Vm_dev_norm
            r["pass_nm"] = int(r["NM_wc_mV"] >= a.min_nm)
            r["pass_asym"] = int(max(r["asym_tp_tt27"], r["asym_slew_tt27"]) <= a.max_asym)
        for tagv, v in (("lo", vlo), ("hi", vhi)):
            gv = g[np.isclose(g.VDD_V, v)]
            if len(gv):
                allok = bool((gv.status == "ok").all())
                r[f"n_vdd_{tagv}"] = len(gv)
                r[f"NM_vdd_{tagv}_mV"] = float(gv.NM_mV.min()) if allok else np.nan
                r[f"pass_vdd_{tagv}"] = int(allok and gv.NM_mV.min() >= VDD_NM_FRAC * v * 1e3)
                r[f"tp_vdd_{tagv}_ns"] = float(gv.tp_ns.max()) if allok else np.nan
        if mc is not None:
            gm = mc[np.isclose(mc.Wn_um, wn) & np.isclose(mc.Wp_um, wp) & np.isclose(mc.Ln_um, ln) & np.isclose(mc.Lp_um, lp)]
            if len(gm):
                worst = None
                for (c, t, v), q in gm.groupby(["corner", "temp_C", "VDD_V"]):
                    nm = q["NM_mV"].fillna(-1e3).to_numpy()
                    mean, sd = float(nm.mean()), float(nm.std(ddof=1)) if len(nm) > 1 else 0.0
                    lower = mean - MC_SIGMA_K * sd
                    if worst is None or lower < worst[0]:
                        worst = (lower, mean, sd, float(nm.min()), float((nm >= a.min_nm).mean()), len(nm), tag(c, t))
                r["mc_n"] = worst[5]
                r["mc_worst_at"] = worst[6]
                r["mc_NM_mean_mV"], r["mc_NM_sigma_mV"], r["mc_NM_min_mV"] = worst[1], worst[2], worst[3]
                r["mc_NM_mean_minus_k_sigma_mV"] = worst[0]
                r["mc_yield_at_floor"] = worst[4]
                r["pass_mc"] = int(worst[0] >= 0.0)
        pr = raw[np.isclose(raw.Wn_um, wn) & np.isclose(raw.Wp_um, wp) & np.isclose(raw.Ln_um, ln) & np.isclose(raw.Lp_um, lp)]
        if "pred_NM_mV" in pr and "NM_wc_mV" in r:
            r["pred_NM_mV"] = float(pr.pred_NM_mV.iloc[0])
            r["err_NM_mV"] = r["pred_NM_mV"] - r["NM_wc_mV"]
            r["err_tp_pct"] = 100 * (float(pr.pred_tp_ns.iloc[0]) - r["tp_wc_ns"]) / r["tp_wc_ns"]
            r["err_E_pct"] = 100 * (float(pr.pred_E_fJ.iloc[0]) - r["E_op_wc_fJ"]) / r["E_op_wc_fJ"]
            r["err_leak_pct"] = 100 * (float(pr.pred_leak_pW.iloc[0]) - r["leak_wc_pW"]) / r["leak_wc_pW"]
        need = ["pass_nm", "pass_asym", "pass_mc"] + (["pass_vdd_lo", "pass_vdd_hi"] if a.vdd_check else [])
        r["checks_done"] = sum(k in r for k in need)
        r["all_pass"] = int(all(r.get(k) == 1 for k in need))
        rows.append(r)

    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(a.dir, "finalists_report.csv"), index=False)
    show = [c for c in ["Wn_um", "Wp_um", "Ln_um", "Lp_um", "pvt_ok", "NM_wc_mV", "NM_wc_at", "tp_wc_ns", "E_op_wc_fJ", "PDP_wc_fJ",
                        "leak_wc_pW", "asym_tp_tt27", "asym_slew_tt27", "NM_vdd_lo_mV", "NM_vdd_hi_mV",
                        "mc_NM_mean_mV", "mc_NM_sigma_mV", "mc_NM_mean_minus_k_sigma_mV", "checks_done", "all_pass"] if c in out]
    print(out[show].round(3).to_string(index=False))
    ecols = [c for c in ("err_NM_mV", "err_tp_pct", "err_E_pct", "err_leak_pct") if c in out]
    if ecols:
        print("\nsurrogate error (predicted minus simulated, worst case over 15 PVT):")
        print(out[ecols].describe().loc[["mean", "min", "max"]].round(2).to_string())
    if "method" in raw:
        hv_report(a, raw, out)
    print(f"\ncriteria: NM_wc >= {a.min_nm:g} mV over 15 PVT at {VDD_NOM:g} V; asymmetry <= {a.max_asym:g} at {tag(*NOMINAL)}; "
          + (f"NM >= {VDD_NM_FRAC * 100:.0f}% VDD at {vlo:g}/{vhi:g} V; " if a.vdd_check else "")
          + f"MC mean - {MC_SIGMA_K:g} sigma >= 0 mV (all at {VDD_NOM:g} V)")
    print(f"{int(out.all_pass.sum())} of {len(out)} finalists pass all checks (15-PVT NM, asymmetry, mismatch" + (", VDD -10 %, VDD +10 %" if a.vdd_check else "") + ")")
    print(f"Saved {os.path.join(a.dir, 'finalists_report.csv')}")


if __name__ == "__main__":
    main()
