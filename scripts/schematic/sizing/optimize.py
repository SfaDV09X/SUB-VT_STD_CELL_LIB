#!/usr/bin/env python3
# Multi-objective sizing on the GP surrogates from fit_gpr.py. Objectives: maximise worst-case
# NM, minimise delay, energy, leakage and area; constraints: feasible, NM >= floor, asymmetry
# <= limit. Compares Bayesian optimisation (MOBO with expected hypervolume improvement) against
# NSGA-II and random search over several seeds, with the same evaluation budget.
# --mode run    : run the comparison, write evaluated_designs.csv, hv_curves.csv, hv_comparison.png
# --mode verify : pick a spread of Pareto designs per method into verify_designs.csv for real simulation

import os
# One BLAS thread per process; parallelism comes from the process pool instead.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import pickle
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import qmc
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, Matern, WhiteKernel
from sklearn.preprocessing import StandardScaler
from pymoo.indicators.hv import HV

from spec import area_um2, W_LEVELS_N, W_LEVELS_P, snap_design, BASELINE, BOX_HI, BOX_LO, FEATURES, MAX_ASYM, MIN_NM_MV

warnings.filterwarnings("ignore")

# Objective vector (all minimised) and the hypervolume reference point in normalised units.
NAMES = list(FEATURES)
ND = len(NAMES)
LO = np.array(BOX_LO, float)
HI = np.array(BOX_HI, float)
OBJ = ["-NM_mV", "log10_tp_ns", "log10_E_fJ", "log10_leak_pW", "area_um2"]
NOBJ = len(OBJ)
REF = 1.1


# Clip to the design box and snap to the allowed width levels and 10 nm L steps.
def snap(x):
    a = np.asarray(x, float)
    flat = a.reshape(-1, a.shape[-1])
    out = np.array([snap_design(*np.clip(r, LO, HI)) for r in flat])
    return out.reshape(a.shape)


def area(x):
    return area_um2(x[..., 0], x[..., 1], x[..., 2], x[..., 3])


# Stands in for the simulator: returns objectives F, pass/fail, per-condition NM, asymmetries
# and constraint values G (<= 0 means satisfied) for one design.
class SurrogateOracle:
    def __init__(self, pkl, min_nm, max_asym):
        with open(pkl, "rb") as f:
            p = pickle.load(f)
        self.m, self.s = p["models"], p["scalers"]
        need = {"NM_mV", "tp", "energy", "leakage", "asym_tp", "asym_slew"}
        missing = need - set(self.m) - ({"NM_mV"} if p.get("nm_cond") else set())
        if missing:
            raise SystemExit(f"{pkl} lacks models for {sorted(missing)} (fewer than 8 feasible training rows). Simulate more designs first.")
        self.c, self.cs = p["classifier"], p["classifier_scaler"]
        self.nm = list((p.get("nm_cond") or {}).values())
        self.min_nm, self.max_asym = min_nm, max_asym

    def __call__(self, x):
        x = snap(x)[None, :]
        lx = np.log(x)
        v = {k: float(self.m[k].predict(self.s[k].transform(lx))[0]) for k in self.m}
        nmv = None
        if self.nm:
            nmv = np.array([float(g.predict(sc.transform(lx))[0]) for sc, g in self.nm])
            v["NM_mV"] = float(nmv.min())
        asy = np.array([v["asym_tp"], v["asym_slew"]])
        func = True if self.c is None else bool(self.c.predict_proba(self.cs.transform(lx))[0, 1] >= 0.5)
        ok = func and v["NM_mV"] >= self.min_nm and asy.max() <= self.max_asym
        F = np.array([-v["NM_mV"], v["tp"], v["energy"], v["leakage"], area(x[0])])
        G = np.array([0.0 if func else 1.0, (self.min_nm - v["NM_mV"]) / 10.0, (asy.max() - self.max_asym) * 10.0])
        return F, bool(ok), nmv, asy, G


# Counts evaluations against the budget and keeps every evaluated design.
class Recorder:
    def __init__(self, oracle, budget):
        self.o, self.budget = oracle, budget
        self.X, self.F, self.feas, self.C, self.A = [], [], [], [], []

    def full(self):
        return len(self.X) >= self.budget

    def eval(self, x):
        x = snap(x)
        F, ok, nmv, asy, G = self.o(x)
        self.X.append(x)
        self.F.append(F)
        self.feas.append(ok)
        self.C.append(nmv)
        self.A.append(asy)
        return F, ok, G


# Normalisation range for each objective, from the feasible training designs.
def make_norm(train_csv):
    d = pd.read_csv(train_csv)
    keep = (d.feasible == 1)
    for f, l, h in zip(NAMES, LO, HI):
        keep &= d[f].between(l - 1e-9, h + 1e-9)
    d = d[keep]
    F = np.c_[-d.NM_mV, np.log10(d.tp_ns), np.log10(d.E_fJ), np.log10(d.leak_pW), area_um2(d.Wn_um, d.Wp_um, d.Ln_um, d.Lp_um)]
    lo, hi = F.min(0), F.max(0)
    return lo, np.where(hi - lo < 1e-12, lo + 1.0, hi)


def normalise(F, lo, hi):
    return (np.asarray(F) - lo) / (hi - lo)


def hypervolume(Fn):
    Fn = np.asarray(Fn)
    Fn = Fn[np.all(Fn < REF, axis=1)] if len(Fn) else Fn
    if len(Fn) == 0:
        return 0.0
    return float(HV(ref_point=np.full(Fn.shape[1], REF))(Fn))


# Hypervolume of the passing designs after each evaluation.
def hv_curve(rec, lo, hi):
    out, pts = [], []
    for F, ok in zip(rec.F[:rec.budget], rec.feas[:rec.budget]):
        if ok:
            pts.append(normalise(F, lo, hi))
        out.append(hypervolume(np.array(pts)) if pts else 0.0)
    return np.array(out)


# Mask of Pareto-optimal rows (all objectives minimised).
def nondominated(F):
    F = np.asarray(F)
    keep = np.ones(len(F), bool)
    for i in range(len(F)):
        if np.any(np.all(F <= F[i], axis=1) & np.any(F < F[i], axis=1)):
            keep[i] = False
    return keep


# Sobol starting points, shared by all methods for a fair comparison.
def initial_design(n, seed):
    u = qmc.Sobol(ND, scramble=True, seed=seed).random(n)
    return snap(LO + u * (HI - LO))


def run_random(rec, X0, seed):
    rng = np.random.default_rng(seed + 1000)
    for x in X0:
        if not rec.full():
            rec.eval(x)
    while not rec.full():
        rec.eval(LO + rng.random(ND) * (HI - LO))


# NSGA-II from pymoo with the same start population and budget.
def run_nsga2(rec, X0, seed):
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem
    from pymoo.optimize import minimize
    from pymoo.termination import get_termination

    class P(Problem):
        def __init__(self):
            super().__init__(n_var=ND, n_obj=NOBJ, n_ieq_constr=3, xl=LO, xu=HI)

        def _evaluate(self, X, out, *a, **k):
            Fs, Gs = [], []
            for x in X:
                if rec.full():
                    Fs.append(np.full(NOBJ, 1e3))
                    Gs.append([1.0, 1.0, 1.0])
                    continue
                F, ok, G = rec.eval(x)
                Fs.append(F)
                Gs.append(list(G))
            out["F"], out["G"] = np.array(Fs), np.array(Gs)

    algo = NSGA2(pop_size=len(X0), n_offsprings=5, sampling=np.array(X0), eliminate_duplicates=True)
    minimize(P(), algo, get_termination("n_eval", rec.budget), seed=seed, verbose=False)
    rng = np.random.default_rng(seed)
    while not rec.full():
        rec.eval(LO + rng.random(ND) * (HI - LO))


def quick_gp():
    k = C(1.0, (1e-2, 1e2)) * Matern(np.ones(ND), (0.05, 50.0), nu=2.5) + WhiteKernel(1e-3, (1e-8, 1e-1))
    return GaussianProcessRegressor(k, normalize_y=True, n_restarts_optimizer=2, random_state=0)


# Small GPs refitted on what the optimiser has seen so far.
def fit_models(X, F, feas, NMC, ASY):
    X, F, feas = np.array(X), np.array(F), np.array(feas)
    NMC, ASY = np.array(NMC, float), np.array(ASY, float)
    LX = np.log(X)
    models = {}
    for j, use_all in ((1, False), (2, False), (3, True)):
        m = np.ones(len(X), bool) if use_all else feas
        if m.sum() < 4:
            return None
        sc = StandardScaler().fit(LX[m])
        models[j] = (sc, quick_gp().fit(sc.transform(LX[m]), F[m, j]))
    nm = []
    for k in range(NMC.shape[1]):
        m = np.isfinite(NMC[:, k])
        if m.sum() < 4:
            return None
        sc = StandardScaler().fit(LX[m])
        nm.append((sc, quick_gp().fit(sc.transform(LX[m]), NMC[m, k])))
    sc = StandardScaler().fit(LX)
    asy = [(sc, quick_gp().fit(sc.transform(LX), ASY[:, k])) for k in range(ASY.shape[1])]
    pf = None
    if 3 <= feas.sum() <= len(feas) - 3:
        k = C(1.0, (1e-2, 1e2)) * RBF(np.ones(ND), (0.05, 50.0))
        pf = (sc, GaussianProcessClassifier(k, random_state=0).fit(sc.transform(LX), feas.astype(int)))
    return models, nm, asy, pf


# Bayesian optimisation loop. Each step: refit the GPs, build candidates (Sobol points plus
# perturbations of the current Pareto designs), estimate the expected hypervolume gain of each
# by sampling the GPs and counting Monte Carlo points it would newly dominate, weight by the
# probability of being feasible, and evaluate the best one. If nothing improves, pick the most
# likely feasible candidate with a small bonus for uncertainty.
def run_mobo(rec, X0, seed, lo, hi, min_nm, max_asym, n_cand=300, n_samp=8, n_mc=30000):
    rng = np.random.default_rng(seed + 2000)
    for x in X0:
        if not rec.full():
            rec.eval(x)

    sob = qmc.Sobol(ND, scramble=True, seed=seed + 3000)
    P_unit = qmc.Sobol(NOBJ, scramble=True, seed=seed + 4000).random(n_mc)
    box_lo, box_hi = -0.3, REF
    P = box_lo + P_unit * (box_hi - box_lo)
    vol = (box_hi - box_lo) ** NOBJ

    while not rec.full():
        fit = fit_models(rec.X, rec.F, rec.feas, rec.C, rec.A)
        if fit is None:
            rec.eval(LO + rng.random(ND) * (HI - LO))
            continue
        models, nm, asy, pf = fit

        cand = LO + sob.random(n_cand) * (HI - LO)
        feas_idx = [i for i, f in enumerate(rec.feas) if f]
        if feas_idx:
            Ff = np.array([normalise(rec.F[i], lo, hi) for i in feas_idx])
            nd = np.array(feas_idx)[nondominated(Ff)]
            base = np.array([rec.X[i] for i in nd])
            loc = base[rng.integers(0, len(base), 100)] + rng.normal(0, 0.05, (100, ND)) * (HI - LO)
            flip = rng.random((100, 2)) < 0.3
            loc[:, 0] = np.where(flip[:, 0], rng.choice(W_LEVELS_N, 100), loc[:, 0])
            loc[:, 1] = np.where(flip[:, 1], rng.choice(W_LEVELS_P, 100), loc[:, 1])
            cand = np.vstack([cand, loc])
        cand = snap(cand)
        lc = np.log(cand)

        mu, sd = np.zeros((len(cand), NOBJ)), np.zeros((len(cand), NOBJ))
        for j, (sc, gp) in models.items():
            m_, s_ = gp.predict(sc.transform(lc), return_std=True)
            mu[:, j], sd[:, j] = m_, s_
        mu[:, 4] = area(cand)
        mn, sn = np.zeros((len(cand), len(nm))), np.zeros((len(cand), len(nm)))
        for k, (sc, gp) in enumerate(nm):
            mn[:, k], sn[:, k] = gp.predict(sc.transform(lc), return_std=True)
        ma, sa = np.zeros((len(cand), len(asy))), np.zeros((len(cand), len(asy)))
        for k, (sc, gp) in enumerate(asy):
            ma[:, k], sa[:, k] = gp.predict(sc.transform(lc), return_std=True)

        pts = [normalise(rec.F[i], lo, hi) for i in feas_idx]
        covered = np.zeros(len(P), bool)
        for f in pts:
            covered |= np.all(P >= f, axis=1)
        U = P[~covered]

        z = rng.standard_normal((n_samp, len(cand), NOBJ))
        Ys = mu[None] + sd[None] * z
        nm_s = mn[None] + sn[None] * rng.standard_normal((n_samp, len(cand), len(nm)))
        asy_s = ma[None] + sa[None] * rng.standard_normal((n_samp, len(cand), len(asy)))
        nm_min = nm_s.min(axis=2)
        Ys[:, :, 0] = -nm_min
        ok_s = (nm_min >= min_nm) & (asy_s.max(axis=2) <= max_asym)

        ehvi = np.zeros(len(cand))
        for c in range(len(cand)):
            Y = normalise(Ys[:, c, :], lo, hi)
            cnt = np.array([np.count_nonzero(np.all(U >= y, axis=1)) for y in Y])
            ehvi[c] = np.mean(cnt * ok_s[:, c]) / n_mc * vol
        if pf is not None:
            ehvi *= pf[1].predict_proba(pf[0].transform(lc))[:, 1]

        if ehvi.max() <= 0:
            p_ok = ok_s.mean(axis=0)
            expl = sd[:, 1:4].sum(1) + sn.sum(1)
            best = int(np.argmax(p_ok + 1e-3 * expl / max(expl.max(), 1e-12)))
        else:
            best = int(np.argmax(ehvi))
        rec.eval(cand[best])
        if len(rec.X) % 10 == 0:
            print(f"      MOBO seed {seed}: {len(rec.X)}/{rec.budget} evaluations", flush=True)


METHODS = {"MOBO": run_mobo, "NSGA-II": run_nsga2, "Random": run_random}


# One (method, seed) run in a worker process.
def job(args):
    method, seed, a = args
    oracle = SurrogateOracle(os.path.join(a.dir, a.models), a.min_nm, a.max_asym)
    lo, hi = make_norm(os.path.join(a.dir, a.train))
    rec = Recorder(oracle, a.budget)
    X0 = initial_design(a.n0, seed)
    t0 = time.time()
    if method == "MOBO":
        run_mobo(rec, X0, seed, lo, hi, a.min_nm, a.max_asym)
    else:
        METHODS[method](rec, X0, seed)
    return method, seed, hv_curve(rec, lo, hi), rec.X[:a.budget], rec.F[:a.budget], rec.feas[:a.budget], time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--train", default="training_pvt.csv")
    ap.add_argument("--models", default="gp_models_pvt.pkl")
    ap.add_argument("--mode", choices=["run", "verify"], default="run")
    ap.add_argument("--budget", type=int, default=70)
    ap.add_argument("--n0", type=int, default=25)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--methods", nargs="+", default=["MOBO", "NSGA-II", "Random"])
    ap.add_argument("--n-verify", type=int, default=10)
    ap.add_argument("--verify-methods", nargs="+", default=["MOBO", "NSGA-II", "Random"])
    ap.add_argument("--min-nm", type=float, default=MIN_NM_MV)
    ap.add_argument("--max-asym", type=float, default=MAX_ASYM)
    a = ap.parse_args()
    if a.mode == "verify":
        return verify(a)

    jobs = [(m, s, a) for s in range(a.seeds) for m in a.methods]
    print(f"{len(jobs)} runs ({a.methods} x {a.seeds} seeds), budget {a.budget}, initial {a.n0}, "
          f"NM floor {a.min_nm:g} mV, asymmetry limit {a.max_asym:g}")
    results = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(job, j) for j in jobs]
        for n, fu in enumerate(as_completed(futs), 1):
            r = fu.result()
            results.append(r)
            print(f"  [{n}/{len(jobs)}] {r[0]:8s} seed {r[1]}  final HV = {r[2][-1]:.4f}   ({r[6]:.0f}s)", flush=True)
    results.sort(key=lambda r: (r[1], a.methods.index(r[0])))

    curves = [{"method": m, "seed": s, "n_evals": i + 1, "hv": h} for m, s, hv, *_ in results for i, h in enumerate(hv)]
    pd.DataFrame(curves).to_csv(os.path.join(a.dir, "hv_curves.csv"), index=False)
    rows = []
    for m, s, hv, X, F, feas, _ in results:
        for i, (x, f, ok) in enumerate(zip(X, F, feas)):
            rows.append(dict(method=m, seed=s, order=i + 1, feasible=int(ok),
                             **dict(zip(NAMES, x)), **dict(zip(OBJ, f))))
    des = pd.DataFrame(rows)
    des["NM_mV"], des["tp_ns"] = -des["-NM_mV"], 10 ** des["log10_tp_ns"]
    des["E_fJ"], des["leak_pW"] = 10 ** des["log10_E_fJ"], 10 ** des["log10_leak_pW"]
    des.to_csv(os.path.join(a.dir, "evaluated_designs.csv"), index=False)

    cv = pd.DataFrame(curves)
    piv = cv.pivot_table(index="n_evals", columns="method", values="hv", aggfunc=["mean", "std"], dropna=False).fillna(0.0)
    final = cv[cv.n_evals == a.budget].groupby("method").hv.agg(["mean", "std"]).fillna(0.0)
    print(f"\nFinal hypervolume after {a.budget} evaluations (mean +- std over {a.seeds} seeds):")
    print(final.round(4).to_string())
    if "NSGA-II" in a.methods and "MOBO" in a.methods:
        target = final.loc["NSGA-II", "mean"]
        mob = piv["mean"]["MOBO"]
        hit = np.where(mob.values >= target)[0]
        if len(hit):
            print(f"\nMOBO reaches NSGA-II's final mean hypervolume after {int(mob.index[hit[0]])} evaluations "
                  f"(NSGA-II needs {a.budget}).")
        else:
            print("\nMOBO does not reach NSGA-II's final mean hypervolume within the budget.")

    # Best NM each method found under increasing delay budgets, with the baseline for reference.
    tr = pd.read_csv(os.path.join(a.dir, a.train))
    b = tr[np.isclose(tr.Wn_um, BASELINE[0]) & np.isclose(tr.Wp_um, BASELINE[1]) & np.isclose(tr.Ln_um, BASELINE[2]) & np.isclose(tr.Lp_um, BASELINE[3])]
    btxt = (f"baseline worst-case NM = {b.NM_mV.iloc[0]:.1f} mV" +
            (f", tp = {b.tp_ns.iloc[0]:.0f} ns" if np.isfinite(b.tp_ns.iloc[0]) else "")) if len(b) else "baseline not in training table"
    ok = des[des.feasible == 1]
    print(f"\nBest spec-passing worst-case noise margin by worst-case FO4 delay budget ({btxt}):")
    tmax = np.nanmax(ok.tp_ns) if len(ok) else 0
    for q in (0.25, 0.5, 0.75, 1.0):
        t_max = np.nanquantile(ok.tp_ns, q) if len(ok) else 0
        best = ok[ok.tp_ns <= t_max].groupby(["method", "seed"]).NM_mV.max().groupby("method").mean()
        print(f"  tp <= {t_max:10.0f} ns : " + "   ".join(f"{k} {v:.1f} mV" for k, v in best.items()))

    fig, ax = plt.subplots(figsize=(7.5, 5))
    for m in a.methods:
        mu, sd = piv["mean"][m].values, piv["std"][m].values
        x = piv.index.values
        ax.plot(x, mu, label=m)
        ax.fill_between(x, mu - sd, mu + sd, alpha=0.2)
    ax.axvline(a.n0, color="gray", ls=":", lw=1)
    ax.set_xlabel("number of simulations")
    ax.set_ylabel("hypervolume (normalised)")
    ax.set_title(f"MOBO vs NSGA-II vs random, worst-case PVT ({a.seeds} seeds)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(a.dir, "hv_comparison.png"), dpi=140)
    print(f"\nSaved hv_curves.csv, evaluated_designs.csv, hv_comparison.png in {a.dir}")


# Up to n_verify Pareto designs per method, spread evenly in NM, for full PVT/MC simulation.
def verify(a):
    d = pd.read_csv(os.path.join(a.dir, "evaluated_designs.csv"))
    parts = []
    for method in a.verify_methods:
        q = d[(d.method == method) & (d.feasible == 1)].drop_duplicates(NAMES)
        if q.empty:
            print(f"  {method}: no design passed the criteria")
            continue
        q = q[nondominated(q[OBJ].to_numpy())].sort_values("NM_mV", ascending=False)
        if len(q) > a.n_verify:
            q = q.iloc[np.unique(np.linspace(0, len(q) - 1, a.n_verify).round().astype(int))]
        parts.append(q.assign(method=method))
    if not parts:
        raise SystemExit("No design passed the criteria in evaluated_designs.csv")
    d = pd.concat(parts, ignore_index=True)
    out = pd.DataFrame({
        "method": d.method, "Wn_um": d.Wn_um, "Wp_um": d.Wp_um, "Ln_um": d.Ln_um, "Lp_um": d.Lp_um, "pred_NM_mV": d.NM_mV, "pred_tp_ns": d.tp_ns,
        "pred_E_fJ": d.E_fJ, "pred_leak_pW": d.leak_pW, "area_um2": d.area_um2})
    path = os.path.join(a.dir, "verify_designs.csv")
    out.to_csv(path, index=False)
    print(out.round(4).to_string(index=False))
    print(f"\n{len(out)} rows ({len(out.drop_duplicates(NAMES))} unique designs) written to {path}")


if __name__ == "__main__":
    main()
