#!/usr/bin/env python3
import argparse
import os
import pickle
import re
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, Matern, WhiteKernel
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler

from spec import BOX_HI, BOX_LO, FEATURES

warnings.filterwarnings("ignore")

TARGETS = {
    "NM_mV":     ("NM_mV",     lambda y: y,   "NM_min worst case (mV)",     "finite"),
    "tp":        ("tp_ns",     np.log10,      "log10 tp_max FO4 (ns)",      "feasible"),
    "energy":    ("E_fJ",      np.log10,      "log10 E_op (fJ)",            "feasible"),
    "leakage":   ("leak_pW",   np.log10,      "log10 leakage (pW)",         "finite"),
    "asym_tp":   ("asym_tp",   lambda y: y,   "tp asymmetry at tt@27",      "nominal"),
    "asym_slew": ("asym_slew", lambda y: y,   "slew asymmetry at tt@27",    "nominal"),
}


def make_X(df):
    return np.log(df[FEATURES].to_numpy(float))


def regressor():
    k = C(1.0, (1e-2, 1e2)) * Matern(length_scale=np.ones(len(FEATURES)),
                                     length_scale_bounds=(0.05, 50.0), nu=2.5) \
        + WhiteKernel(1e-3, (1e-8, 1e-1))
    return GaussianProcessRegressor(k, normalize_y=True, n_restarts_optimizer=8, random_state=0)


def classifier():
    k = C(1.0, (1e-2, 1e2)) * RBF(np.ones(len(FEATURES)), (0.05, 50.0))
    return GaussianProcessClassifier(k, n_restarts_optimizer=4, random_state=0)


def cv_regression(X, y, folds, seed):
    mu, sd = np.zeros(len(y)), np.zeros(len(y))
    for tr, te in KFold(min(folds, len(y)), shuffle=True, random_state=seed).split(X):
        sc = StandardScaler().fit(X[tr])
        m = regressor().fit(sc.transform(X[tr]), y[tr])
        mu[te], sd[te] = m.predict(sc.transform(X[te]), return_std=True)
    return mu, sd


def metrics(y, mu, sd):
    err = y - mu
    z = err / np.maximum(sd, 1e-12)
    return {
        "R2": 1 - np.sum(err ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-30),
        "RMSE": float(np.sqrt(np.mean(err ** 2))),
        "MAE": float(np.mean(np.abs(err))),
        "cover_1sigma": float(np.mean(np.abs(z) <= 1)),
        "cover_2sigma": float(np.mean(np.abs(z) <= 2)),
        "mean_sigma": float(np.mean(sd)),
    }


def select_rows(df, col, use):
    ok = np.isfinite(df[col])
    if use == "feasible":
        return df[(df.feasible == 1) & ok]
    return df[ok]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--train", default="training_pvt.csv")
    ap.add_argument("--tag", default="pvt")
    ap.add_argument("--in-box", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    out = a.out or a.dir
    os.makedirs(out, exist_ok=True)

    sfx = f"_{a.tag}" if a.tag else ""
    df = pd.read_csv(os.path.join(a.dir, a.train))
    if a.in_box:
        keep = np.ones(len(df), bool)
        for f, l, h in zip(FEATURES, BOX_LO, BOX_HI):
            keep &= df[f].between(l - 1e-9, h + 1e-9).to_numpy()
        print(f"--in-box: keeping {int(keep.sum())} of {len(df)} designs inside the box")
        df = df[keep].reset_index(drop=True)
    print(f"{len(df)} training designs, {int(df.feasible.sum())} feasible\n")

    rows, oof = [], {}
    models, scalers = {}, {}
    print(f"{a.folds}-fold cross-validation (hyper-parameters re-fitted in each fold)")
    for name, (col, tf, label, use) in TARGETS.items():
        d = select_rows(df, col, use)
        if len(d) < 8:
            print(f"  {name:9s} skipped: only {len(d)} rows")
            continue
        X, y = make_X(d), tf(d[col].to_numpy(float))
        mu, sd = cv_regression(X, y, a.folds, a.seed)
        m = metrics(y, mu, sd)
        m.update(target=name, n=len(y), y_std=float(y.std()))
        rows.append(m)
        oof[name] = (y, mu, sd, label)
        sc = StandardScaler().fit(X)
        models[name] = regressor().fit(sc.transform(X), y)
        scalers[name] = sc
        print(f"  {name:9s} n={len(y):3d}  R2={m['R2']:.3f}  RMSE={m['RMSE']:.3f} "
              f"(target std {y.std():.3f})  1sigma={m['cover_1sigma']:.2f}  2sigma={m['cover_2sigma']:.2f}")

    X = make_X(df)
    yc = df["feasible"].to_numpy(int)
    clf, scc = None, None
    if 0 < yc.sum() < len(yc) and min(yc.sum(), len(yc) - yc.sum()) >= 2:
        pc = np.zeros(len(yc))
        for tr, te in StratifiedKFold(min(a.folds, int(min(yc.sum(), len(yc) - yc.sum()))),
                                      shuffle=True, random_state=a.seed).split(X, yc):
            sc = StandardScaler().fit(X[tr])
            g = classifier().fit(sc.transform(X[tr]), yc[tr])
            pc[te] = g.predict_proba(sc.transform(X[te]))[:, 1]
        pred = (pc >= 0.5).astype(int)
        print(f"\n  feasibility classifier: accuracy={np.mean(pred == yc):.3f} "
              f"(majority baseline {max(yc.mean(), 1 - yc.mean()):.3f}), "
              f"false-feasible={int(np.sum((pred == 1) & (yc == 0)))}, "
              f"false-infeasible={int(np.sum((pred == 0) & (yc == 1)))}")
        scc = StandardScaler().fit(X)
        clf = classifier().fit(scc.transform(X), yc)
    else:
        print("\n  feasibility classifier skipped: only one class present")

    cond_cols = [c for c in df.columns if re.fullmatch(r"NM_(tt|ss|ff|sf|fs)_-?\d+(?:\.\d+)?C", c)]
    nm_cond = {}
    if cond_cols:
        Xa = make_X(df)
        n_, nc = len(df), len(cond_cols)
        omu, osd = np.full((n_, nc), np.nan), np.full((n_, nc), np.nan)
        for tr, te in KFold(min(a.folds, n_), shuffle=True, random_state=a.seed).split(Xa):
            for j, c in enumerate(cond_cols):
                yv = df[c].to_numpy(float)
                m = np.isfinite(yv[tr])
                if m.sum() < 8:
                    continue
                sc = StandardScaler().fit(Xa[tr][m])
                g = regressor().fit(sc.transform(Xa[tr][m]), yv[tr][m])
                omu[te, j], osd[te, j] = g.predict(sc.transform(Xa[te]), return_std=True)
        print("\nper-condition noise-margin GPs (cross-validated):")
        for j, c in enumerate(cond_cols):
            yv = df[c].to_numpy(float)
            m = np.isfinite(yv) & np.isfinite(omu[:, j])
            if m.sum() < 3:
                continue
            mm = metrics(yv[m], omu[m, j], osd[m, j])
            mm.update(target=c, n=int(m.sum()), y_std=float(yv[m].std()))
            rows.append(mm)
            print(f"  {c:14s} n={int(m.sum()):3d}  R2={mm['R2']:.3f}  RMSE={mm['RMSE']:.2f} mV")
            fin = np.isfinite(yv)
            if fin.sum() >= 8:
                sc = StandardScaler().fit(Xa[fin])
                nm_cond[c] = (sc, regressor().fit(sc.transform(Xa[fin]), yv[fin]))

        full = np.isfinite(df[cond_cols].to_numpy(float)).all(axis=1) & np.isfinite(df["NM_mV"].to_numpy(float))
        full &= np.isfinite(omu).all(axis=1)
        if full.sum() >= 3:
            yw = df.loc[full, "NM_mV"].to_numpy(float)
            draws = omu[full][None] + osd[full][None] * np.random.default_rng(0).standard_normal((300, int(full.sum()), nc))
            pw, sw = draws.min(axis=2).mean(0), draws.min(axis=2).std(0)
            mw = metrics(yw, pw, sw)
            mw.update(target="NM_worst", n=int(full.sum()), y_std=float(yw.std()))
            rows.append(mw)
            oof["NM_worst"] = (yw, pw, sw, "worst-case NM_min (mV)")
            print(f"\n  worst-case NM, min of per-condition GPs (n={int(full.sum())}): "
                  f"R2={mw['R2']:.3f}  RMSE={mw['RMSE']:.2f} mV  1sigma={mw['cover_1sigma']:.2f}")

    pd.DataFrame(rows).to_csv(os.path.join(out, f"cv_metrics{sfx}.csv"), index=False)

    fig, axs = plt.subplots((len(oof) + 1) // 2, 2, figsize=(10, 4.5 * ((len(oof) + 1) // 2)), squeeze=False)
    for ax in axs.ravel()[len(oof):]:
        ax.axis("off")
    for ax, (name, (y, mu, sd, label)) in zip(axs.ravel(), oof.items()):
        ax.errorbar(y, mu, yerr=2 * sd, fmt="o", ms=3, alpha=0.6, elinewidth=0.6)
        lo, hi = min(y.min(), mu.min()), max(y.max(), mu.max())
        ax.plot([lo, hi], [lo, hi], "k--", lw=1)
        r2 = [r for r in rows if r["target"] == name][0]["R2"]
        ax.set_title(f"{name}   CV R2 = {r2:.3f}")
        ax.set_xlabel("simulated: " + label)
        ax.set_ylabel("predicted (out-of-fold)")
    fig.tight_layout()
    fig.savefig(os.path.join(out, f"cv_gpr{sfx}.png"), dpi=130)

    with open(os.path.join(out, f"gp_models{sfx}.pkl"), "wb") as f:
        pickle.dump({"features": FEATURES, "targets": {k: v[2] for k, v in TARGETS.items()},
                     "models": models, "scalers": scalers, "classifier": clf,
                     "classifier_scaler": scc, "nm_cond": nm_cond}, f)
    print(f"\nSaved cv_metrics{sfx}.csv, cv_gpr{sfx}.png, gp_models{sfx}.pkl in {out}")


if __name__ == "__main__":
    main()
