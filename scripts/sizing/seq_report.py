#!/usr/bin/env python3
import argparse

import numpy as np
import pandas as pd

KEYS = ["Win_um", "Lin_um", "Wfb_um", "Lfb_um", "kclk", "kout", "kqb"]


def summarise(d, min_snm, max_asym):
    d = d.copy()
    d["cond"] = d.corner + "@" + d.temp_C.astype(float).astype(int).astype(str)
    rows = []
    for key, g in d.groupby(KEYS):
        r = dict(zip(KEYS, key))
        r["n_cond"] = g.cond.nunique()
        r["all_ok"] = bool((g.status == "ok").all())
        r["snm_wc_mV"] = g.snm_mV.min()
        r["snm_wc_at"] = g.loc[g.snm_mV.idxmin(), "cond"] if g.snm_mV.notna().any() else ""
        full = "tcq_max_s" in g and g.tcq_max_s.notna().any()
        if full:
            ok = g[g.status == "ok"]
            r["tcq_wc_us"] = ok.tcq_max_s.max() * 1e6 if len(ok) else np.nan
            r["tcq_wc_at"] = ok.loc[ok.tcq_max_s.idxmax(), "cond"] if len(ok) else ""
            r["E_wc_fJ"] = ok.energy_cycle_J.max() * 1e15 if len(ok) else np.nan
            r["leak_wc_pW"] = ok.leak_W.max() * 1e12 if len(ok) else np.nan
            t = g[(g.corner == "tt") & (g.temp_C.astype(float) == 27.0)]
            r["asym_tcq_tt27"] = float(t.asym_tcq.iloc[0]) if len(t) and t.asym_tcq.notna().iloc[0] else np.nan
            r["asym_slew_tt27"] = float(t.asym_slew.iloc[0]) if len(t) and t.asym_slew.notna().iloc[0] else np.nan
            r["failed_at"] = " ".join(g[g.status != "ok"].cond)
            r["pass"] = bool(r["all_ok"] and r["snm_wc_mV"] >= min_snm
                             and r["asym_tcq_tt27"] <= max_asym and r["asym_slew_tt27"] <= max_asym)
        else:
            r["pass"] = bool(r["all_ok"] and r["snm_wc_mV"] >= min_snm)
        rows.append(r)
    return pd.DataFrame(rows)


def mc_summary(m, k):
    out = []
    for key, g in m.groupby(KEYS):
        r = dict(zip(KEYS, key))
        worst = None
        for c, gc in g.groupby(["corner", "temp_C"]):
            v = gc.snm_mV.dropna()
            if len(v) < 2:
                continue
            marg = v.mean() - k * v.std(ddof=1)
            if worst is None or marg < worst[0]:
                worst = (marg, v.mean(), v.std(ddof=1), f"{c[0]}@{float(c[1]):g}")
        if worst:
            r.update(mc_mean_mV=worst[1], mc_sigma_mV=worst[2], mc_margin_mV=worst[0], mc_at=worst[3])
        out.append(r)
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser(description="Summarise sequential-cell runs per design.")
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--mc", default=None)
    ap.add_argument("--min-snm", type=float, default=40.0)
    ap.add_argument("--max-asym", type=float, default=0.25)
    ap.add_argument("--k", type=float, default=3.0)
    ap.add_argument("--out", default="seq_summary.csv")
    ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()
    d = pd.concat([pd.read_csv(f) for f in a.csv], ignore_index=True)
    d = d.drop_duplicates(KEYS + ["corner", "temp_C", "mode"], keep="last")
    s = summarise(d, a.min_snm, a.max_asym)
    if a.mc:
        s = s.merge(mc_summary(pd.read_csv(a.mc), a.k), on=KEYS, how="left")
        s["pass"] = s["pass"] & (s.mc_margin_mV >= 0)
    s.to_csv(a.out, index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    print(f"{len(s)} designs, {int(s['pass'].sum())} pass (SNM >= {a.min_snm:g} mV"
          + (f", asymmetry <= {a.max_asym:g}" if "asym_tcq_tt27" in s else "") + (", MC mean - k sigma >= 0" if a.mc else "") + ")")
    order = "E_wc_fJ" if "E_wc_fJ" in s else "snm_wc_mV"
    asc = order == "E_wc_fJ"
    print(s.sort_values(["pass", order], ascending=[False, asc]).head(a.top).round(3).to_string(index=False))
    print(f"Saved {a.out}")


if __name__ == "__main__":
    main()
