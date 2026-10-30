#!/usr/bin/env python3
import argparse, csv, itertools, os, re, subprocess, sys, tempfile
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from libtools import (cell_blocks, cell_info, sensitizing_states, when_expr, eval_function)

_trapz = getattr(np, "trapezoid", None) or np.trapz
VDD = 0.4
TEMP = 27
SEQ = {"dffx1": "dff", "dlx1": "latch"}
G = None


def ports(net, cell):
    for l in open(net):
        m = re.match(r"\s*\.subckt\s+" + re.escape(cell) + r"\s+(.*)", l, re.I)
        if m:
            return m.group(1).split()
    raise SystemExit("no .subckt %s in %s" % (cell, net))


def node(p):
    return "vdd" if p == "VDD" else "0" if p == "GND" else p.lower()


def header(net, cell):
    return ('.lib "%s" %s\n.include "%s"\n.temp %g\n.option abstol=1e-15 reltol=1e-4\nVSUP vdd 0 DC %g\n'
            % (G.models, G.corner, net, TEMP, VDD))


def instance(net, cell):
    return "X1 %s %s\n" % (" ".join(node(p) for p in ports(net, cell)), cell)


def pwl(points):
    return "PWL(" + " ".join("%.6gn %.6g" % p for p in points) + ")"


def steps_to_pwl(init, steps, ramp=100.0):
    pts = [(0.0, init * VDD)]
    cur = init
    for t, lvl in steps:
        pts += [(t, cur * VDD), (t + ramp, lvl * VDD)]
        cur = lvl
    return pwl(pts)


def run_ng(base):
    try:
        r = subprocess.run([G.ngspice, "-b", base + ".sp"], capture_output=True, text=True,
                           env=dict(os.environ, OMP_NUM_THREADS="1"), timeout=G.timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT after %g s" % G.timeout
    return r.stdout + r.stderr


def avg(t, v, a, b):
    m = (t >= a) & (t <= b)
    tt = t[m]
    if len(tt) < 2:
        raise ValueError("no samples in [%g,%g]" % (a, b))
    return _trapz(v[m], tt) / (tt[-1] - tt[0])


def cross(t, v, level, rising, a, b):
    m = (t >= a) & (t <= b)
    tt, vv = t[m], v[m]
    s = (vv[:-1] - level) * (vv[1:] - level) < 0
    for i in np.nonzero(s)[0]:
        if (vv[i + 1] > vv[i]) == rising:
            return tt[i] + (level - vv[i]) * (tt[i + 1] - tt[i]) / (vv[i + 1] - vv[i])
    return None


def power_task(a):
    cell, net, pin, state, i, j, load_pf, ramp, Tp, out = a
    tag = "p_%s_%s_%s_%d_%d" % (cell, pin, "".join(str(v) for v in state.values()) or "x", i, j)
    base = os.path.join(G.work, tag)
    P = ports(net, cell)
    src = ""
    for p in P:
        if p in ("VDD", "GND", out):
            continue
        if p == pin:
            src += "V_%s %s 0 %s\n" % (p, node(p), pwl([(0, 0), (Tp, 0), (Tp + ramp, VDD), (2 * Tp, VDD),
                                                       (2 * Tp + ramp, 0), (3 * Tp, 0)]))
        else:
            src += "V_%s %s 0 DC %g\n" % (p, node(p), state[p] * VDD)
    tmax = min(Tp / 1500.0, ramp / 10.0)
    open(base + ".sp", "w").write(
        "* power %s\n%s%s%sCL %s 0 %gp\n.tran %gn %gn\n.control\nset filetype=ascii\nrun\n"
        "wrdata %s.dat v(%s) i(VSUP)\nquit\n.endc\n.end\n"
        % (tag, header(net, cell), instance(net, cell), src, node(out), load_pf, tmax, 3 * Tp, base, node(out)))
    log = run_ng(base)
    if not os.path.exists(base + ".dat"):
        return [dict(error="ngspice failed: " + log[-400:], tag=tag)]
    x = np.loadtxt(base + ".dat")
    os.remove(base + ".dat")
    t = x[:, 0] * 1e9
    vy = x[:, 1]
    isup = -x[:, 3]
    rows = []
    for k, in_edge in ((1, "rise"), (2, "fall")):
        te, tend = k * Tp, (k + 1) * Tp
        vb = avg(t, vy, te - 0.1 * Tp, te)
        va = avg(t, vy, tend - 0.1 * Tp, tend)
        ib = avg(t, isup, te - 0.1 * Tp, te)
        ia = avg(t, isup, tend - 0.1 * Tp, tend)
        i_early = avg(t, isup, tend - 0.2 * Tp, tend - 0.1 * Tp)
        out_rise = va > vb
        rail = VDD if out_rise else 0.0
        tx = cross(t, vy, 0.5 * VDD, out_rise, te, tend)
        row = dict(cell=cell, pin=pin, when=when_expr(state), in_edge=in_edge,
                   out_edge="rise" if out_rise else "fall", i=i, j=j, load_pF=load_pf, ramp_ns=ramp)
        if tx is None:
            row["error"] = "output did not cross 50 %"
            rows.append(row)
            continue
        m = (t >= te) & (t <= tend)
        ibase = np.where(t[m] < tx, ib, ia)
        e_sup = VDD * _trapz(isup[m] - ibase, t[m] * 1e-9)
        e_load = load_pf * 1e-12 * VDD * (va - vb) if out_rise else 0.0
        row.update(Esup_fJ=e_sup * 1e15, Eload_fJ=e_load * 1e15, Eint_fJ=(e_sup - e_load) * 1e15,
                   Vy_err_V=abs(va - rail), drift_fJ=abs(ia - i_early) * VDD * 0.1 * Tp * 1e-9 * 1e15)
        rows.append(row)
    return rows


def power_jobs(lib_text, cells, repo, only_point=None):
    jobs = []
    cb = cell_blocks(lib_text)
    for name in cells:
        if name in SEQ:
            continue
        s, e = cb[name]
        info = cell_info(lib_text[s:e])
        out = info["outputs"][0]
        assert len(info["outputs"]) == 1, name
        fn = info["function"][out]
        loads = ramps = None
        for key, tabs in info["tables"].items():
            for (i1, i2, v) in tabs:
                if loads is None:
                    loads, ramps = i1, i2
                assert i1 == loads and i2 == ramps, "grid differs inside " + name
        net = os.path.join(repo, "cells", name.upper(), "spice", name + ".spice")
        for pin in info["inputs"]:
            states = sensitizing_states(fn, pin, info["inputs"])
            if not states:
                raise SystemExit("%s: pin %s never controls the output" % (name, pin))
            for st in states:
                for ii, jj in itertools.product(range(len(loads)), range(len(ramps))):
                    if only_point and (ii, jj) != only_point:
                        continue
                    dmax = max(v[ii][jj] for tabs in info["tables"].values() for (_, _, v) in tabs)
                    Tp = max(2000.0, 10.0 * 2 * dmax + 2 * ramps[jj])
                    jobs.append((name, net, pin, st, ii, jj, loads[ii], ramps[jj], Tp, out))
    return jobs


def leak_comb_task(a):
    cell, net, state, out = a
    tag = "l_%s_%s" % (cell, "".join(str(v) for v in state.values()))
    base = os.path.join(G.work, tag)
    src = "".join("V_%s %s 0 DC %g\n" % (p, node(p), v * VDD) for p, v in state.items())
    open(base + ".sp", "w").write("* leak %s\n%s%s%s.control\nop\nprint i(VSUP)\nquit\n.endc\n.end\n"
                                  % (tag, header(net, cell), instance(net, cell), src))
    log = run_ng(base)
    m = re.search(r"i\(vsup\)\s*=\s*([-+0-9.eE]+)", log, re.I)
    method = "op"
    if m:
        I = -float(m.group(1))
    else:
        open(base + ".sp", "w").write(
            "* leak %s\n%s%s%s.tran 100n 200u\n.control\nset filetype=ascii\nrun\nwrdata %s.dat i(VSUP)\nquit\n.endc\n.end\n"
            % (tag, header(net, cell), instance(net, cell), src, base))
        run_ng(base)
        if not os.path.exists(base + ".dat"):
            return dict(cell=cell, when=when_expr(state), error="ngspice failed: " + log[-300:])
        x = np.loadtxt(base + ".dat")
        I = -avg(x[:, 0], x[:, 1], 0.9 * x[-1, 0], x[-1, 0])
        method = "tran"
    return dict(cell=cell, when=when_expr(state), I_A=I, P_nW=I * VDD * 1e9, method=method)


def leak_seq_task(a):
    cell, net, kind, clk, d, q = a
    tag = "l_%s_%d%d%d" % (cell, clk, d, q)
    base = os.path.join(G.work, tag)
    T = 100000.0
    if kind == "dff":
        if clk == 0:
            ck = steps_to_pwl(0, [(T, 1), (2 * T, 0)]); dd = steps_to_pwl(q, [(3 * T, d)]) if d != q else steps_to_pwl(q, [])
            end = 4 * T
        else:
            ck = steps_to_pwl(0, [(T, 1)]); dd = steps_to_pwl(q, [(2 * T, d)]) if d != q else steps_to_pwl(q, [])
            end = 3 * T
    else:
        if clk == 1:
            if d != q:
                return dict(cell=cell, when=when_expr({"CLK": clk, "D": d, "Q": q}), error="unreachable (transparent)")
            ck = steps_to_pwl(1, []); dd = steps_to_pwl(d, []); end = 2 * T
        else:
            ck = steps_to_pwl(1, [(T, 0)]); dd = steps_to_pwl(q, [(2 * T, d)]) if d != q else steps_to_pwl(q, [])
            end = 3 * T
    P = ports(net, cell)
    inst = "X1 %s %s\n" % (" ".join(node(p) for p in P), cell)
    open(base + ".sp", "w").write(
        "* leak %s\n%sV_CLK clk 0 %s\nV_D d 0 %s\n%s.tran 50n %gn\n.control\nset filetype=ascii\nrun\n"
        "wrdata %s.dat v(q) v(qb) i(VSUP)\nquit\n.endc\n.end\n" % (tag, header(net, cell), ck, dd, inst, end, base))
    log = run_ng(base)
    w = when_expr({"CLK": clk, "D": d, "Q": q})
    if not os.path.exists(base + ".dat"):
        return dict(cell=cell, when=w, error="ngspice failed: " + log[-300:])
    x = np.loadtxt(base + ".dat")
    os.remove(base + ".dat")
    t = x[:, 0] * 1e9
    vq, vqb, isup = x[:, 1], x[:, 3], -x[:, 5]
    qe = avg(t, vq, end - 0.1 * T, end)
    qbe = avg(t, vqb, end - 0.1 * T, end)
    ok = (qe > 0.9 * VDD if q else qe < 0.1 * VDD) and (qbe < 0.1 * VDD if q else qbe > 0.9 * VDD)
    I = avg(t, isup, end - 0.1 * T, end)
    I_prev = avg(t, isup, end - 0.2 * T, end - 0.1 * T)
    row = dict(cell=cell, when=w, I_A=I, P_nW=I * VDD * 1e9, method="tran")
    if not ok:
        row["error"] = "state not reached (Q=%.3f V, QB=%.3f V)" % (qe, qbe)
    elif abs(I - I_prev) > 0.02 * abs(I) + 1e-15:
        row["error"] = "current not settled (%.4g vs %.4g A)" % (I, I_prev)
    return row


def leak_jobs(lib_text, cells, repo):
    comb, seq = [], []
    cb = cell_blocks(lib_text)
    for name in cells:
        net = os.path.join(repo, "cells", name.upper(), "spice", name + ".spice")
        if name in SEQ:
            for clk, d, q in itertools.product((0, 1), repeat=3):
                seq.append((name, net, SEQ[name], clk, d, q))
        else:
            s, e = cb[name]
            info = cell_info(lib_text[s:e])
            for bits in itertools.product((0, 1), repeat=len(info["inputs"])):
                comb.append((name, net, dict(zip(info["inputs"], bits)), info["outputs"][0]))
    return comb, seq


SEQ_PROG = {
    "dff": [("CLK", 1), ("CLK", 0), ("D", 1), ("CLK", 1), ("CLK", 0), ("CLK", 1), ("D", 0), ("D", 1), ("CLK", 0),
            ("D", 0), ("D", 1), ("D", 0), ("CLK", 1), ("D", 1), ("D", 0), ("CLK", 0), ("D", 1), ("D", 0),
            # events 19-24: CLK falls with D != Q (D changed while CLK high). Used only for the CLK fall pin energy.
            ("CLK", 1), ("D", 1), ("CLK", 0), ("CLK", 1), ("D", 0), ("CLK", 0)],
    "latch": [("CLK", 1), ("D", 1), ("CLK", 0), ("D", 0), ("CLK", 1), ("CLK", 0), ("D", 1), ("CLK", 1), ("D", 0),
              ("CLK", 0), ("D", 1), ("D", 0), ("D", 1), ("CLK", 1), ("CLK", 0), ("D", 0), ("D", 1), ("CLK", 1)],
}


def seq_ideal(kind, c, d, q, sig, lvl):
    if sig == "CLK":
        c2 = lvl
        if lvl == 1 and c == 0:
            q = d
        return c2, d, q
    d2 = lvl
    if kind == "latch" and c == 1:
        q = d2
    return c, d2, q


def seq_program(kind, H, ramp):
    clk, dd, ev = [(1 * H, 1), (2 * H, 0)], [], []
    c, d, q = seq_ideal(kind, 0, 0, 0, "CLK", 1)
    c, d, q = seq_ideal(kind, c, d, q, "CLK", 0)
    assert (c, d, q) == (0, 0, 0)
    for n, (sig, lvl) in enumerate(SEQ_PROG[kind], 1):
        te = (n + 2) * H
        ev.append(dict(n=n, te=te, sig=sig, lvl=lvl, c=c, d=d, q=q))
        (clk if sig == "CLK" else dd).append((te, lvl))
        c, d, q = seq_ideal(kind, c, d, q, sig, lvl)
    return clk, dd, ev, (len(ev) + 3) * H


def seq_analyse(t, vq, vqb, isup, kind, events, H, ramp, cq, cqb):
    rows = []
    for e in events:
        te = e["te"]
        pre, post, early = (te - 0.1 * H, te), (te + 0.9 * H, te + H), (te + 0.8 * H, te + 0.9 * H)
        row = dict(n=e["n"], sig=e["sig"], edge="rise" if e["lvl"] else "fall", c=e["c"], d=e["d"])
        vq_b, vq_a = avg(t, vq, *pre), avg(t, vq, *post)
        vb_b, vb_a = avg(t, vqb, *pre), avg(t, vqb, *post)
        qb_, qa_ = int(vq_b > 0.5 * VDD), int(vq_a > 0.5 * VDD)
        row.update(q_before=qb_, q_after=qa_)
        c2, d2, q2 = seq_ideal(kind, e["c"], e["d"], e["q"], e["sig"], e["lvl"])
        ok_lvl = (abs(vq_b - qb_ * VDD) < 0.1 * VDD and abs(vq_a - qa_ * VDD) < 0.1 * VDD and
                  abs(vb_b - (1 - qb_) * VDD) < 0.1 * VDD and abs(vb_a - (1 - qa_) * VDD) < 0.1 * VDD)
        if not ok_lvl:
            row["error"] = "Q/QB not complementary at rails (Q %.3f->%.3f V, QB %.3f->%.3f V)" % (vq_b, vq_a, vb_b, vb_a)
            rows.append(row)
            continue
        if qb_ != e["q"] or qa_ != q2:
            row["error"] = "unexpected state: Q %d->%d, expected %d->%d" % (qb_, qa_, e["q"], q2)
            rows.append(row)
            continue
        toggled = qb_ != qa_
        ib, ia = avg(t, isup, *pre), avg(t, isup, *post)
        i_early = avg(t, isup, *early)
        if toggled:
            tx = cross(t, vq, 0.5 * VDD, bool(qa_), te, te + H)
            if tx is None:
                row["error"] = "Q did not cross 50 %"
                rows.append(row)
                continue
        else:
            tx = te + 0.5 * ramp
        m = (t >= te) & (t <= te + H)
        ibase = np.where(t[m] < tx, ib, ia)
        e_sup = VDD * _trapz(isup[m] - ibase, t[m] * 1e-9)
        e_load = 0.0
        if toggled:
            if vq_a > vq_b:
                e_load += cq * 1e-12 * VDD * (vq_a - vq_b)
            if vb_a > vb_b:
                e_load += cqb * 1e-12 * VDD * (vb_a - vb_b)
        row.update(Esup_fJ=e_sup * 1e15, Eload_fJ=e_load * 1e15, Eint_fJ=(e_sup - e_load) * 1e15,
                   Vq_err_V=max(abs(vq_a - qa_ * VDD), abs(vb_a - (1 - qa_) * VDD)),
                   drift_fJ=abs(ia - i_early) * VDD * 0.1 * H * 1e-9 * 1e15)
        rows.append(row)
    return rows


def seq_power_task(a):
    cell, net, kind, jj, ramp, H, cq, cqb = a
    tag = "sp_%s_%d_%g_%g" % (cell, jj, cq, cqb)
    base = os.path.join(G.work, tag)
    clk_s, d_s, events, tend = seq_program(kind, H, ramp)
    loads = ("Cq q 0 %gp\n" % cq if cq else "") + ("Cqb qb 0 %gp\n" % cqb if cqb else "")
    tmax = min(H / 1500.0, ramp / 10.0)
    open(base + ".sp", "w").write(
        "* seq power %s\n%sV_CLK clk 0 %s\nV_D d 0 %s\n%s%s.tran %gn %gn\n.control\nset filetype=ascii\nrun\n"
        "wrdata %s.dat v(q) v(qb) i(VSUP)\nquit\n.endc\n.end\n"
        % (tag, header(net, cell), steps_to_pwl(0, clk_s, ramp), steps_to_pwl(0, d_s, ramp), instance(net, cell),
           loads, tmax, tend, base))
    log = run_ng(base)
    base_row = dict(cell=cell, jj=jj, ramp_ns=ramp, cq_pF=cq, cqb_pF=cqb)
    if not os.path.exists(base + ".dat"):
        return [dict(base_row, error="ngspice failed: " + log[-400:])]
    x = np.loadtxt(base + ".dat")
    os.remove(base + ".dat")
    rows = seq_analyse(x[:, 0] * 1e9, x[:, 1], x[:, 3], -x[:, 5], kind, events, H, ramp, cq, cqb)
    return [dict(base_row, **r) for r in rows]


def seq_power_jobs(lib_text, cells, repo):
    jobs = []
    cb = cell_blocks(lib_text)
    for name in cells:
        if name not in SEQ:
            continue
        s, e = cb[name]
        info = cell_info(lib_text[s:e])
        grid = None
        for key, tabs in info["tables"].items():
            for (i1, i2, v) in tabs:
                if grid is None:
                    grid = (i1, i2)
                assert (i1, i2) == grid, "grid differs inside " + name
        loads, slews = grid
        dmax = max(v for tabs in info["tables"].values() for (_, _, vals) in tabs for row in vals for v in row)
        ramps = [sl / 0.4 for sl in slews]
        H = max(5000.0, 20.0 * dmax + 8.0 * max(ramps))
        net = os.path.join(repo, "cells", name.upper(), "spice", name + ".spice")
        for jj, ramp in enumerate(ramps):
            cfg = [(0.0, 0.0)] + [(L, 0.0) for L in loads] + [(0.0, L) for L in loads]
            for cq, cqb in cfg:
                jobs.append((name, net, SEQ[name], jj, ramp, H, cq, cqb))
    return jobs


def main():
    global G
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--models", default=os.path.join(os.environ.get("PDK_ROOT", ""), os.environ.get("PDK", ""),
                                                    "libs.tech/ngspice/sky130.lib.spice"))
    p.add_argument("--corner", default="tt")
    p.add_argument("--ngspice", default="ngspice")
    p.add_argument("--jobs", type=int, default=os.cpu_count())
    p.add_argument("--timeout", type=float, default=900.0, help="seconds allowed per ngspice run")
    p.add_argument("--quick", action="store_true", help="INV1X1 FO1 point only (power) + INV1X1 leakage")
    p.add_argument("--cells", default=None, help="comma list of lower-case cell names (default: all 13)")
    G = p.parse_args()
    if not os.path.isfile(G.models):
        sys.exit("model file not found: " + G.models)
    os.makedirs(G.out, exist_ok=True)
    G.work = tempfile.mkdtemp(prefix="meas_", dir=G.out)
    lib_text = open(os.path.join(G.repo, "lib", "subvt_sky130_tt_0p40v_27c.lib")).read()
    all_cells = list(cell_blocks(lib_text))
    cells = G.cells.split(",") if G.cells else all_cells
    if G.quick:
        cells = ["inv1x1"]
    unknown = [c for c in cells if c not in all_cells]
    if unknown:
        sys.exit("cells not in lib: %s" % unknown)
    pool = ProcessPoolExecutor(G.jobs, mp_context=mp.get_context("fork"))
    errors = []

    comb, seq = leak_jobs(lib_text, cells, G.repo)
    lres = list(pool.map(leak_comb_task, comb)) + list(pool.map(leak_seq_task, seq))
    with open(os.path.join(G.out, "leakage.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, ["cell", "when", "I_A", "P_nW", "method", "error"])
        w.writeheader()
        for r in lres:
            w.writerow(r)
            if r.get("error"):
                errors.append("leak %s %s: %s" % (r["cell"], r["when"], r["error"]))
    print("leakage: %d states, %d problems" % (len(lres), sum(1 for r in lres if r.get("error"))), flush=True)

    jobs = power_jobs(lib_text, cells, G.repo, only_point=(1, 2) if G.quick else None)
    print("power: %d simulations" % len(jobs), flush=True)
    rows = []
    for n, res in enumerate(pool.map(power_task, jobs, chunksize=4), 1):
        rows += res
        if n % 10 == 0 or n == len(jobs):
            print("  %d / %d" % (n, len(jobs)), flush=True)
    cols = ["cell", "pin", "when", "in_edge", "out_edge", "i", "j", "load_pF", "ramp_ns", "Esup_fJ", "Eload_fJ",
            "Eint_fJ", "Vy_err_V", "drift_fJ", "error"]
    with open(os.path.join(G.out, "power.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
            if r.get("error"):
                errors.append("power %s %s %s: %s" % (r.get("cell"), r.get("pin"), r.get("when"), r["error"]))
            elif r["Vy_err_V"] > 0.02 * VDD:
                errors.append("power %s %s %s %s i=%d j=%d: output not settled (%.3g V)" %
                              (r["cell"], r["pin"], r["when"], r["in_edge"], r["i"], r["j"], r["Vy_err_V"]))
            elif r["drift_fJ"] > 0.005:
                errors.append("power %s %s %s %s i=%d j=%d: supply current still drifting (%.4f fJ)" %
                              (r["cell"], r["pin"], r["when"], r["in_edge"], r["i"], r["j"], r["drift_fJ"]))

    sjobs = seq_power_jobs(lib_text, cells, G.repo)
    if sjobs:
        print("sequential power: %d simulations" % len(sjobs), flush=True)
        srows = []
        for n, res in enumerate(pool.map(seq_power_task, sjobs), 1):
            srows += res
            print("  %d / %d" % (n, len(sjobs)), flush=True)
        scols = ["cell", "jj", "ramp_ns", "cq_pF", "cqb_pF", "n", "sig", "edge", "c", "d", "q_before", "q_after",
                 "Esup_fJ", "Eload_fJ", "Eint_fJ", "Vq_err_V", "drift_fJ", "error"]
        with open(os.path.join(G.out, "seq_power.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, scols, extrasaction="ignore")
            w.writeheader()
            for r in srows:
                w.writerow(r)
                tagr = "seqpower %s jj=%s cq=%s cqb=%s n=%s" % (r.get("cell"), r.get("jj"), r.get("cq_pF"), r.get("cqb_pF"), r.get("n"))
                if r.get("error"):
                    errors.append("%s: %s" % (tagr, r["error"]))
                elif r["Vq_err_V"] > 0.02 * VDD:
                    errors.append("%s: output not settled (%.3g V)" % (tagr, r["Vq_err_V"]))
                elif r["drift_fJ"] > 0.005:
                    errors.append("%s: supply current still drifting (%.4f fJ)" % (tagr, r["drift_fJ"]))

    if G.quick:
        print("\nINV1X1 FO1 point (load %.6g pF, ramp %.6g ns)" % (rows[0]["load_pF"], rows[0]["ramp_ns"]))
        print("expected from the exp1/power-check runs: A rising: supply -0.03..-0.05 fJ; A falling: supply 0.68..0.69 fJ, C*V^2 = 0.355 fJ")
        for r in rows:
            print("  input %s -> output %s: supply %.4f fJ, load %.4f fJ, internal %.4f fJ" %
                  (r["in_edge"], r["out_edge"], r["Esup_fJ"], r["Eload_fJ"], r["Eint_fJ"]))
        for r in lres:
            print("  leakage %-6s %.4g A  (%.4g nW)" % (r["when"], r["I_A"], r["P_nW"]))
        print("expected leakage from the earlier check: 5.18e-13 A (A=0), 3.40e-12 A (A=1)")
    with open(os.path.join(G.out, "measure.log"), "w") as f:
        f.write("\n".join(errors) + ("\n" if errors else ""))
    print("\n%d warnings/errors (see %s)" % (len(errors), os.path.join(G.out, "measure.log")))
    for e in errors[:20]:
        print("  " + e)
    sys.exit(1 if any("unreachable" not in e for e in errors) else 0)


if __name__ == "__main__":
    main()
