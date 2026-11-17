#!/usr/bin/env python3
import argparse
import os

import pandas as pd

from spec import MAX_ASYM, MIN_NM_MV

KEY = ["Wn_um", "Wp_um", "Ln_um", "Lp_um"]


def main():
    ap = argparse.ArgumentParser(description="Explain why designs fail: status per corner, failures versus each variable, NM and asymmetry spread.")
    ap.add_argument("--dir", default=".")
    ap.add_argument("--file", default="all_conditions.csv")
    a = ap.parse_args()
    path = os.path.join(a.dir, a.file)
    if not os.path.exists(path):
        raise SystemExit(f"{path} not found - run build_dataset.py first")
    pd.set_option("display.width", 200)
    d = pd.read_csv(path)
    d["cond"] = d.corner + "@" + d.temp_C.astype(int).astype(str)
    d["ok"] = d.status == "ok"
    print("=== 1. status per condition")
    print(pd.crosstab(d.cond, d.status), "\n")

    print("=== 2. share of functional runs versus each variable, per condition (1.00 = always works)")
    for v in KEY:
        t = d.pivot_table(index=d[v].round(2), columns="cond", values="ok", aggfunc="mean")
        print(f"-- {v}")
        print(t.round(2), "\n")

    print(f"=== 3. noise margin (mV) per condition, functional runs only; floor {MIN_NM_MV:g} mV")
    ok = d[d.ok]
    print((ok.groupby("cond").NM_min_V.describe(percentiles=[0.1, 0.5, 0.9]) * 1e3).drop(columns="count").round(1), "\n")
    if "worst_arc" in d.columns:
        print("=== 3b. which arc sets the noise margin (count of runs)")
        print(pd.crosstab(ok.cond, ok.worst_arc), "\n")

    t = d[(d.corner == "tt") & (d.temp_C == 27) & d.ok]
    if len(t):
        print(f"=== 4. asymmetry at tt@27 (limit {MAX_ASYM:g})")
        print(t[["asym_tp", "asym_slew"]].describe(percentiles=[0.1, 0.5, 0.9]).T.round(3).drop(columns="count"), "\n")
        r = t.assign(ratio=(t.Wp_um / t.Wn_um).round(2))
        print("-- median slew asymmetry versus Wp/Wn")
        print(r.groupby("ratio").asym_slew.agg(["count", "median", "min"]).round(3), "\n")
        arcs = [c for c in t.columns if c.startswith("asym_slew_arc_")]
        if arcs:
            print("-- median slew asymmetry per arc")
            print(t[arcs].median().round(3), "\n")

    g = d.groupby(KEY)
    full = g.cond.nunique()
    n_cond = d.cond.nunique()
    func = g.ok.all()
    nm = g.NM_min_V.min() * 1e3
    print("=== 5. counts over designs with every condition")
    m = full == n_cond
    print(f"designs complete {m.sum()}, functional everywhere {(func & m).sum()}, "
          f"NM >= {MIN_NM_MV:g} mV {((nm >= MIN_NM_MV) & func & m).sum()}")
    if len(t):
        at = t.set_index(KEY)
        both = ((at.asym_tp <= MAX_ASYM) & (at.asym_slew <= MAX_ASYM)).reindex(func.index).fillna(False)
        print(f"asymmetry pass {(both & m).sum()}, everything {((nm >= MIN_NM_MV) & func & m & both).sum()}")
    print("\n=== 6. nearest misses (functional everywhere, sorted by worst-case NM)")
    cand = pd.DataFrame({"NM_wc_mV": nm, "functional": func})[func & m]
    if len(t):
        cand = cand.join(t.set_index(KEY)[["asym_tp", "asym_slew"]])
    print(cand.sort_values("NM_wc_mV", ascending=False).head(15).round(3))


if __name__ == "__main__":
    main()
