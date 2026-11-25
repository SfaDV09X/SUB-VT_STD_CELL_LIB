#!/usr/bin/env python3
# Sizing simulations for the sequential cells DLX4 and DFFX4 (cell chosen with SUBVT_SEQ_CELL).
# Devices are grouped into roles (clock inverter, input and feedback transmission gates,
# internal/QB/Q inverters); a design is the 7 numbers in KEYS. For each design and PVT
# condition it measures the hold SNM of every storage loop and, in full mode, clock-to-Q
# delay, slews, energy per cycle and leakage; setup/hold times in setup-hold mode.
# Netlist handling and ngspice runs are shared with subvt_dataset.py.

import argparse
import csv
import os
import shutil
import sys
import time
from multiprocessing import Pool

import numpy as np

# subvt_dataset needs some cell selected at import; only its helpers are used here.
os.environ.setdefault("SUBVT_CELL", "inv1x4")
os.environ["SUBVT_CELL"] = "inv1x4"
import subvt_dataset as sd
from spec import split_fingers, AVT_N, AVT_P, VDD_NOM, FANOUT

# Reference inverter (Wn, Wp, Ln, Lp) from the INV1X4 sizing; drivers and inverter roles scale it.
INV_SIZED = tuple(float(x) for x in os.environ.get("SUBVT_INV_SIZED", "0.84,1.68,0.29,0.21").split(","))
# Search space: allowed widths, inverter multiples, L ranges, and the default design.
W_LEVELS = (0.42, 0.84, 1.68, 2.52)
K_LEVELS = (1, 2, 3)
LIN_BOX = (0.15, 0.30)
LFB_BOX = (0.15, 0.50)
KEYS = ["Win_um", "Lin_um", "Wfb_um", "Lfb_um", "kclk", "kout", "kqb"]
DEFAULT = {"Win_um": 0.84, "Lin_um": 0.15, "Wfb_um": 0.42, "Lfb_um": 0.30, "kclk": 1, "kout": 1, "kqb": 1}
# Clock period to start with (doubled up to 3 times if the cell does not switch), clock and
# data edge time, settle band (10 % of VDD) for a valid output, and DC sweep step.
PERIOD = 40e-6
PERIOD_RETRIES = 3
EDGE = 50e-9
SETTLE = 0.1
DC_STEP = 0.002

# Per cell: netlist, capturing clock edge, which devices form each role, and the storage
# loops (node broken for the SNM test, clock level that holds it, feedback devices).
SEQ = {
    "dlx4": {
        "netlist": "cells/DLX4/spice/dlx4.spice",
        "capture": "fall",
        "load_clk": "inverted",
        "roles": {
            "clk_inv": {"n": ["XM4"], "p": ["XM3"]},
            "tg_in": {"n": ["XM2"], "p": ["XM1"]},
            "tg_fb": {"n": ["XM10"], "p": ["XM7"]},
            "inv_int": {"n": [], "p": []},
            "inv_qb": {"n": ["XM8"], "p": ["XM9"]},
            "inv_out": {"n": ["XM6"], "p": ["XM5"]},
        },
        "loops": [
            {"name": "latch", "hold_clk": 0, "in": "net1", "mid": "QB", "fb": ["XM7", "XM10"]},
        ],
    },
    "dffx4": {
        "netlist": "cells/DFFX4/spice/dffx4.spice",
        "capture": "rise",
        "load_clk": "same",
        "roles": {
            "clk_inv": {"n": ["XM4"], "p": ["XM3"]},
            "tg_in": {"n": ["XM2", "XM5"], "p": ["XM1", "XM18"]},
            "tg_fb": {"n": ["XM16", "XM14"], "p": ["XM15", "XM13"]},
            "inv_int": {"n": ["XM8", "XM6"], "p": ["XM7", "XM17"]},
            "inv_qb": {"n": ["XM10"], "p": ["XM9"]},
            "inv_out": {"n": ["XM12"], "p": ["XM11"]},
        },
        "loops": [
            {"name": "master", "hold_clk": 1, "in": "net1", "mid": "net3", "fb": ["XM15", "XM16"]},
            {"name": "slave", "hold_clk": 0, "in": "net4", "mid": "QB", "fb": ["XM13", "XM14"]},
        ],
    },
}

CELL_NAME = os.environ.get("SUBVT_SEQ_CELL", "dlx4").lower()
if CELL_NAME not in SEQ:
    raise SystemExit(f"SUBVT_SEQ_CELL='{CELL_NAME}' unknown (dlx4 | dffx4)")
CELL = SEQ[CELL_NAME]
NETLIST = os.path.join(sd.BASE_DIR, CELL["netlist"])
if not os.path.isfile(NETLIST):
    raise SystemExit(f"netlist not found: {NETLIST}")
OUT_DIR = os.environ.get("SUBVT_OUT_DIR") or os.path.join(sd.BASE_DIR, "sizing_work", "sim")
RUNS = os.path.join(OUT_DIR, "seq_runs")

# Columns written to the output csv.
FIELDS = (["cell"] + KEYS + ["corner", "temp_C", "VDD_V", "mode", "sample", "status", "snm_mV"]
          + [f"snm_{lp['name']}_mV" for lp in CELL["loops"]]
          + ["period_s", "tcq_rise_s", "tcq_fall_s", "tcq_max_s", "trise_s", "tfall_s", "asym_tcq", "asym_slew",
             "energy_cycle_J", "leak_W", "setup_rise_s", "setup_fall_s", "hold_rise_s", "hold_fall_s", "setup_s", "hold_s",
             "runtime_s", "error"])


# Normalise a design row read from csv (rounded floats, integer multiples).
def norm(d):
    return {"Win_um": round(float(d["Win_um"]), 4), "Lin_um": round(float(d["Lin_um"]), 4),
            "Wfb_um": round(float(d["Wfb_um"]), 4), "Lfb_um": round(float(d["Lfb_um"]), 4),
            "kclk": int(round(float(d["kclk"]))), "kout": int(round(float(d["kout"]))),
            "kqb": int(round(float(d.get("kqb", 1))))}


# (W, L) of the nmos and pmos in each role; transmission gate pmos is twice the nmos width.
def role_sizes(d):
    wn, wp, ln, lp = INV_SIZED
    return {
        "clk_inv": ((d["kclk"] * wn, ln), (d["kclk"] * wp, lp)),
        "tg_in": ((d["Win_um"], d["Lin_um"]), (2 * d["Win_um"], d["Lin_um"])),
        "tg_fb": ((d["Wfb_um"], d["Lfb_um"]), (2 * d["Wfb_um"], d["Lfb_um"])),
        "inv_int": ((wn, ln), (wp, lp)),
        "inv_qb": ((d["kqb"] * wn, ln), (d["kqb"] * wp, lp)),
        "inv_out": ((d["kout"] * wn, ln), (d["kout"] * wp, lp)),
    }


def device_sizes(d):
    out = {}
    for role, (n, p) in role_sizes(d).items():
        for dev in CELL["roles"][role]["n"]:
            out[dev] = n
        for dev in CELL["roles"][role]["p"]:
            out[dev] = p
    return out


# Rewrite the netlist with the role sizes, splitting wide devices into fingers.
def size_block(block, d):
    sizes = device_sizes(d)
    out, used = [], set()
    for line in block:
        k = sd.device_kind(line)
        if k is None:
            out.append(line)
            continue
        toks = line.split()
        dev = toks[0].upper()
        if dev not in sizes:
            raise RuntimeError(f"device {dev} has no role")
        used.add(dev)
        w, length = sizes[dev]
        for i, (wf, nf) in enumerate(split_fingers(round(w, 4))):
            t = list(toks)
            t[0] = f"{toks[0]}_f{i}"
            s = " ".join(t)
            s = sd.W_RE.sub(lambda m: f"W={wf * nf:g}", s)
            s = sd.L_RE.sub(lambda m: f"L={length:g}", s)
            s = sd.NF_RE.sub(f"nf={nf}", s) if sd.NF_RE.search(s) else s + f" nf={nf}"
            s = sd.GEOM_RE.sub("", s).rstrip() + " " + sd.geometry_params(wf * nf, nf)
            out.append(s)
    missing = set(sizes) - used
    if missing:
        raise RuntimeError(f"roles name devices not in the netlist: {sorted(missing)}")
    return out


def rename(block, new):
    out = []
    for line in block:
        if line.strip().lower().startswith(".subckt"):
            t = line.split()
            t[1] = new
            out.append(" ".join(t))
        else:
            out.append(line)
    return out


# Open a storage loop: the feedback gate's connection to the loop input goes to a new port
# FBX, so the two halves of the loop can be swept separately for the butterfly curve.
def break_loop(block, loop, extra_ports):
    out = []
    fb = {x.upper() for x in loop["fb"]}
    for line in block:
        low = line.strip().lower()
        if low.startswith(".subckt"):
            out.append(line + " " + " ".join(extra_ports))
            continue
        k = sd.device_kind(line)
        if k is not None and sd.BASE_RE.sub("", line.split()[0]).upper() in fb:
            t = line.split()
            for i in (1, 3):
                if t[i].lower() == loop["in"].lower():
                    t[i] = "FBX"
            out.append(" ".join(t))
            continue
        out.append(line)
    return out


def inst(ports, name, sub, conn):
    return f"{name} " + " ".join(conn[p.upper()] for p in ports) + f" {sub}"


# Reference inverter used as clock/data driver and as load.
def driver_inv():
    wn, wp, ln, lp = INV_SIZED
    lines = [".subckt drvinv A Y VDD GND"]
    for tag, kind, w, length, drain_src in (("n", "nfet", wn, ln, "Y A GND GND"), ("p", "pfet", wp, lp, "Y A VDD VDD")):
        for i, (wf, nf) in enumerate(split_fingers(w)):
            lines.append(f"XD{tag}{i} {drain_src} sky130_fd_pr__{kind}_01v8 L={length:g} W={wf * nf:g} nf={nf} "
                         + sd.geometry_params(wf * nf, nf))
    lines.append(".ends")
    return lines


# Load on Q and QB: FANOUT copies of the reference inverter ("inv") or of the cell itself.
LOAD_KIND = os.environ.get("SUBVT_SEQ_LOAD", "cell").lower()


def loads(ports, name, node, prefix, clk, n):
    out = []
    if LOAD_KIND == "inv":
        for i in range(n):
            out.append(inst(["A", "Y", "VDD", "GND"], f"X{prefix}{i}", "drvinv",
                            {"A": node, "Y": f"{prefix}y{i}", "VDD": "vddx", "GND": "0"}))
        return out
    for i in range(n):
        conn = {"D": node, "CLK": clk, "VDD": "vddx", "GND": "0", "Q": f"{prefix}q{i}", "QB": f"{prefix}qb{i}"}
        out.append(inst(ports, f"X{prefix}{i}", name, conn))
    return out


def header(blocks, corner, temp):
    s = sd.header(blocks[0], corner, temp)
    for b in blocks[1:]:
        s += "\n".join(b) + "\n"
    return s


def run(run_dir, tb, text, out):
    with open(os.path.join(run_dir, tb), "w") as f:
        f.write(text)
    sd.run_ngspice(run_dir, tb, out)
    return np.loadtxt(os.path.join(run_dir, out))


# Hold SNM of one loop: sweep the loop input and read the middle node, then sweep the middle
# node and read the feedback node, and take the largest square between the two curves.
def snm_loop(base_block, load_blk, name, ports, loop, corner, temp, vdd, run_dir):
    extra = [n for n in (loop["in"], loop["mid"]) if n.upper() not in [p.upper() for p in ports]] + ["FBX"]
    sub = f"{name}_snm"
    blk = break_loop(rename(base_block, sub), loop, extra)
    clk = vdd if loop["hold_clk"] else 0.0

    def conn_map():
        m = {"D": "nd", "CLK": "nclk", "VDD": "vddd", "GND": "0", "Q": "nq", "QB": "nqb", "FBX": "nfbx"}
        for n in extra:
            if n != "FBX":
                m[n.upper()] = "n_" + n.lower()
        return m

    m = conn_map()
    node_in = m.get(loop["in"].upper())
    node_mid = m.get(loop["mid"].upper())
    dut_ports = ports + extra
    tops = [inst(dut_ports, "XDUT", sub, m)]
    common = (f"Vddd vddd 0 DC {vdd:g}\nVddx vddx 0 DC {vdd:g}\nVclk nclk 0 DC {clk:g}\nVd nd 0 DC 0\n"
              + "\n".join(tops) + "\n")
    curves = []
    for force, read, tag in ((node_in, node_mid, "a"), (node_mid, "nfbx", "b")):
        tb = (header([load_blk, blk], corner, temp) + common + f"Vsw {force} 0 DC 0\n"
              + f".control\nset wr_singlescale\ndc Vsw 0 {vdd:g} {DC_STEP:g}\nwrdata snm_{tag}.txt v({read})\n.endc\n.end\n")
        d = run(run_dir, f"tb_snm_{tag}.cir", tb, f"snm_{tag}.txt")
        curves.append((d[:, 0], d[:, 1]))
    return butterfly(curves[0], curves[1], vdd)


# Seevinck-style SNM: largest square that fits in each lobe of the butterfly plot,
# result is the smaller of the two lobes.
def butterfly(a, b, vdd):
    xa, ya = a
    yb, xb = b
    order = np.argsort(yb)
    yb, xb = yb[order], xb[order]
    pos, neg = 0.0, 0.0
    for x1, y1 in zip(xa, ya):
        t = np.linspace(-y1, vdd - y1, 801)
        h = np.interp(y1 + t, yb, xb) - (x1 + t)
        s = np.where(np.sign(h[:-1]) != np.sign(h[1:]))[0]
        for i in s:
            r = t[i] - h[i] * (t[i + 1] - t[i]) / (h[i + 1] - h[i])
            if r > 0:
                pos = max(pos, r)
            elif r < 0:
                neg = max(neg, -r)
    return min(pos, neg)


_trapz = getattr(np, "trapezoid", None) or np.trapz


# Interpolated times where v crosses `level` in the given direction.
def crossings(t, v, level, rising):
    s = v - level
    idx = np.where((s[:-1] < 0) & (s[1:] >= 0))[0] if rising else np.where((s[:-1] > 0) & (s[1:] <= 0))[0]
    return t[idx] + (-s[idx]) * (t[idx + 1] - t[idx]) / (s[idx + 1] - s[idx])


def first_after(arr, t0, t1):
    a = arr[(arr > t0) & (arr < t1)]
    return float(a[0]) if len(a) else None


# Transient test: buffered clock and data, data toggles every other cycle, FO4 loads on Q
# and QB. Fails (None) if any captured or held value is wrong; otherwise measures tcq and
# slews on the last two edges, energy over one period and leakage just before the edges.
def tran(base_block, name, ports, corner, temp, vdd, period, ncyc, run_dir):
    T = period
    tops = [inst(["A", "Y", "VDD", "GND"], "XC1", "drvinv", {"A": "ck0", "Y": "ck1", "VDD": "vddx", "GND": "0"}),
            inst(["A", "Y", "VDD", "GND"], "XC2", "drvinv", {"A": "ck1", "Y": "nclkd", "VDD": "vddx", "GND": "0"}),
            inst(["A", "Y", "VDD", "GND"], "XD1", "drvinv", {"A": "d0", "Y": "d1", "VDD": "vddx", "GND": "0"}),
            inst(["A", "Y", "VDD", "GND"], "XD2", "drvinv", {"A": "d1", "Y": "nd", "VDD": "vddx", "GND": "0"}),
            inst(ports, "XDUT", name, {"D": "nd", "CLK": "nclkd", "VDD": "vddd", "GND": "0", "Q": "nq", "QB": "nqb"})]
    lck = "ck0b" if CELL["load_clk"] == "inverted" else "ck0"
    tops += loads(ports, name, "nq", "LQ", lck, FANOUT)
    tops += loads(ports, name, "nqb", "LB", lck, FANOUT)
    tb = (header([base_block, driver_inv()], corner, temp)
          + f"Vddd vddd 0 DC {vdd:g}\nVddx vddx 0 DC {vdd:g}\n"
          + f"Vck ck0 0 PULSE(0 {vdd:g} {T / 2:g} {EDGE:g} {EDGE:g} {T / 2 - EDGE:g} {T:g})\n"
          + f"Vckb ck0b 0 PULSE({vdd:g} 0 {T / 2:g} {EDGE:g} {EDGE:g} {T / 2 - EDGE:g} {T:g})\n"
          + f"Vdd0 d0 0 PULSE(0 {vdd:g} {T / 4:g} {EDGE:g} {EDGE:g} {T - EDGE:g} {2 * T:g})\n"
          + "\n".join(tops) + "\n"
          + f".control\nset wr_singlescale\ntran {T / 4000:g} {(ncyc + 0.5) * T:g}\n"
          + "wrdata tran.txt v(nclkd) v(nq) v(nqb) i(Vddd)\n.endc\n.end\n")
    d = run(run_dir, "tb_tran.cir", tb, "tran.txt")
    t, vc, vq, vqb, i = d[:, 0], d[:, 1], d[:, 2], d[:, 3], -d[:, 4]
    expect = [1 if k % 2 == 0 else 0 for k in range(ncyc)]
    ck_r = crossings(t, vc, vdd / 2, True)
    edges = []
    for k in range(ncyc):
        te = first_after(ck_r, (k + 0.5) * T - 0.05 * T, (k + 1.0) * T)
        if te is None:
            return None
        edges.append(te)
    if edges[-1] + 0.49 * T > t[-1]:
        return None
    for k in range(1, ncyc):
        tr = edges[k]
        hold_q = np.interp(tr - 0.01 * T, t, vq)
        cap_q = np.interp(tr + 0.49 * T, t, vq)
        cap_qb = np.interp(tr + 0.49 * T, t, vqb)
        prev, new = expect[k - 1], expect[k]
        okh = hold_q >= (1 - SETTLE) * vdd if prev else hold_q <= SETTLE * vdd
        okc = (cap_q >= (1 - SETTLE) * vdd and cap_qb <= SETTLE * vdd) if new else (cap_q <= SETTLE * vdd and cap_qb >= (1 - SETTLE) * vdd)
        if not (okh and okc):
            return None
    q_r, q_f = crossings(t, vq, vdd / 2, True), crossings(t, vq, vdd / 2, False)
    res = {}
    for k in (ncyc - 2, ncyc - 1):
        te = edges[k]
        tr0 = te
        if expect[k]:
            tq = first_after(q_r, te, tr0 + 0.5 * T)
            lo, hi = first_after(crossings(t, vq, 0.3 * vdd, True), te, tr0 + 0.5 * T), first_after(crossings(t, vq, 0.7 * vdd, True), te, tr0 + 0.5 * T)
            if tq is None or lo is None or hi is None:
                return None
            res["tcq_rise_s"], res["trise_s"] = tq - te, hi - lo
        else:
            tq = first_after(q_f, te, tr0 + 0.5 * T)
            hi, lo = first_after(crossings(t, vq, 0.7 * vdd, False), te, tr0 + 0.5 * T), first_after(crossings(t, vq, 0.3 * vdd, False), te, tr0 + 0.5 * T)
            if tq is None or lo is None or hi is None:
                return None
            res["tcq_fall_s"], res["tfall_s"] = tq - te, lo - hi
    res["tcq_max_s"] = max(res["tcq_rise_s"], res["tcq_fall_s"])
    res["asym_tcq"] = abs(res["tcq_rise_s"] - res["tcq_fall_s"]) / res["tcq_max_s"]
    res["asym_slew"] = abs(res["trise_s"] - res["tfall_s"]) / max(res["trise_s"], res["tfall_s"])
    w = (t >= edges[-2] - 0.5 * T) & (t <= edges[-2] + 1.5 * T)
    res["energy_cycle_J"] = vdd * float(_trapz(i[w], t[w])) / 2
    lk = []
    for k in (ncyc - 2, ncyc - 1):
        tr0 = edges[k]
        m = (t >= tr0 - 0.05 * T) & (t <= tr0 - 0.02 * T)
        lk.append(float(np.mean(i[m])))
    res["leak_W"] = vdd * float(np.mean(lk))
    return res


# Same bench with an arbitrary data waveform (PWL), used by the setup/hold search.
def tran_event(base_block, name, ports, corner, temp, vdd, T, d_pts, tstop, run_dir):
    tops = [inst(["A", "Y", "VDD", "GND"], "XC1", "drvinv", {"A": "ck0", "Y": "ck1", "VDD": "vddx", "GND": "0"}),
            inst(["A", "Y", "VDD", "GND"], "XC2", "drvinv", {"A": "ck1", "Y": "nclkd", "VDD": "vddx", "GND": "0"}),
            inst(["A", "Y", "VDD", "GND"], "XD1", "drvinv", {"A": "d0", "Y": "d1", "VDD": "vddx", "GND": "0"}),
            inst(["A", "Y", "VDD", "GND"], "XD2", "drvinv", {"A": "d1", "Y": "nd", "VDD": "vddx", "GND": "0"}),
            inst(ports, "XDUT", name, {"D": "nd", "CLK": "nclkd", "VDD": "vddd", "GND": "0", "Q": "nq", "QB": "nqb"})]
    lck = "ck0b" if CELL["load_clk"] == "inverted" else "ck0"
    tops += loads(ports, name, "nq", "LQ", lck, FANOUT)
    tops += loads(ports, name, "nqb", "LB", lck, FANOUT)
    pwl = " ".join(f"{t:g} {v:g}" for t, v in d_pts)
    tb = (header([base_block, driver_inv()], corner, temp)
          + f"Vddd vddd 0 DC {vdd:g}\nVddx vddx 0 DC {vdd:g}\n"
          + f"Vck ck0 0 PULSE(0 {vdd:g} {T / 2:g} {EDGE:g} {EDGE:g} {T / 2 - EDGE:g} {T:g})\n"
          + f"Vckb ck0b 0 PULSE({vdd:g} 0 {T / 2:g} {EDGE:g} {EDGE:g} {T / 2 - EDGE:g} {T:g})\n"
          + f"Vdd0 d0 0 PWL({pwl})\n"
          + "\n".join(tops) + "\n"
          + f".control\nset wr_singlescale\ntran {T / 4000:g} {tstop:g}\n"
          + "wrdata ev.txt v(nclkd) v(nd) v(nq)\n.endc\n.end\n")
    d = run(run_dir, "tb_ev.cir", tb, "ev.txt")
    return d[:, 0], d[:, 1], d[:, 2], d[:, 3]


# Data waveform: start at `old`, switch to `new` at t_sw, optionally back at t_back.
def d_wave(T, old, new, t_sw, t_back, vdd):
    pts = [(0, old * vdd)]
    for t, a, b in ((t_sw, old, new), (t_back, new, old)):
        if t is None:
            continue
        pts += [(t, a * vdd), (t + EDGE, b * vdd)]
    return pts


# Binary search for setup (latest data change before the capture edge that is still
# captured) and hold (earliest change back after the edge that does not corrupt it),
# for rising and falling data. Reported values are the worst of the two.
def setup_hold(base_block, name, ports, corner, temp, vdd, T, run_dir, steps=8):
    t_c = 2.5 * T if CELL["capture"] == "rise" else 3.0 * T
    tstop = t_c + T
    res = {}

    def capture(old, new, t_sw, t_back):
        t, vc, vd, vq = tran_event(base_block, name, ports, corner, temp, vdd, T, d_wave(T, old, new, t_sw, t_back, vdd), tstop, run_dir)
        ce = crossings(t, vc, vdd / 2, CELL["capture"] == "rise")
        ce = ce[(ce > t_c - 0.05 * T) & (ce < t_c + 0.5 * T)]
        if not len(ce):
            return False, t, vd, None
        ce = float(ce[0])
        if ce + 0.49 * T > t[-1]:
            return False, t, vd, ce
        q = np.interp(ce + 0.49 * T, t, vq)
        ok = q >= (1 - SETTLE) * vdd if new else q <= SETTLE * vdd
        return ok, t, vd, ce

    for old, new in ((0, 1), (1, 0)):
        tag = "rise" if new else "fall"
        lo, hi = -0.2 * T, 0.4 * T
        ok_hi, *_ = capture(old, new, t_c - hi, None)
        ok_lo, *_ = capture(old, new, t_c - lo, None)
        if ok_hi and not ok_lo:
            for _ in range(steps):
                mid = (lo + hi) / 2
                ok, *_ = capture(old, new, t_c - mid, None)
                if ok:
                    hi = mid
                else:
                    lo = mid
            ok, t, vd, ce = capture(old, new, t_c - hi, None)
            dc = crossings(t, vd, vdd / 2, bool(new))
            dc = dc[np.argmin(np.abs(dc - (t_c - hi)))] if len(dc) else None
            res[f"setup_{tag}_s"] = (ce - dc) if (ce is not None and dc is not None) else np.nan
        else:
            res[f"setup_{tag}_s"] = np.nan
        lo, hi = -0.3 * T, 0.4 * T
        t_new = t_c - 0.45 * T
        ok_hi, *_ = capture(old, new, t_new, t_c + hi)
        ok_lo, *_ = capture(old, new, t_new, t_c + lo)
        if ok_hi and not ok_lo:
            for _ in range(steps):
                mid = (lo + hi) / 2
                ok, *_ = capture(old, new, t_new, t_c + mid)
                if ok:
                    hi = mid
                else:
                    lo = mid
            ok, t, vd, ce = capture(old, new, t_new, t_c + hi)
            dc = crossings(t, vd, vdd / 2, not bool(new))
            dc = dc[np.argmin(np.abs(dc - (t_c + hi)))] if len(dc) else None
            res[f"hold_{tag}_s"] = (dc - ce) if (ce is not None and dc is not None) else np.nan
        elif ok_hi and ok_lo:
            res[f"hold_{tag}_s"] = -0.3 * T
        else:
            res[f"hold_{tag}_s"] = np.nan
    vals = [res[k] for k in ("setup_rise_s", "setup_fall_s")]
    res["setup_s"] = np.nanmax(vals) if np.any(np.isfinite(vals)) else np.nan
    vals = [res[k] for k in ("hold_rise_s", "hold_fall_s")]
    res["hold_s"] = np.nanmax(vals) if np.any(np.isfinite(vals)) else np.nan
    return res


# Static leakage averaged over both stored states, clock held at the hold level.
def leak_dc(base_block, name, ports, corner, temp, vdd, run_dir):
    vals = []
    hold = CELL["loops"][-1]["hold_clk"]
    for state in (0, 1):
        ns = " ".join(f"v(xdut.{lp['in']})={state * vdd:g}" for lp in CELL["loops"])
        tb = (header([base_block], corner, temp)
              + f"Vddd vddd 0 DC {vdd:g}\nVclk nclk 0 DC {hold * vdd:g}\nVd nd 0 DC {state * vdd:g}\n"
              + inst(ports, "XDUT", name, {"D": "nd", "CLK": "nclk", "VDD": "vddd", "GND": "0", "Q": "nq", "QB": "nqb"}) + "\n"
              + f".nodeset {ns}\n"
              + ".control\nset wr_singlescale\nop\nwrdata leak.txt i(Vddd) v(nq)\n.endc\n.end\n")
        d = np.atleast_2d(run(run_dir, "tb_leak.cir", tb, "leak.txt"))
        vals.append(-d[0, -2] * vdd)
    return float(np.mean(vals))


# One job = one design at one condition. Monte Carlo samples add Pelgrom Vth mismatch
# (seeded so reruns repeat); mismatch only goes into the SNM benches.
def evaluate(job):
    d, corner, temp, vdd, mode, ncyc, sample, seed = job
    t0 = time.time()
    row = {"cell": CELL_NAME, **d, "corner": corner, "temp_C": temp, "VDD_V": vdd, "mode": mode,
           "sample": sample, "status": "ok", "error": ""}
    tag = f"{CELL_NAME}_{'_'.join(str(d[k]) for k in KEYS)}_{corner}_{temp:g}_{mode}_{sample}"
    run_dir = os.path.join(RUNS, tag)
    os.makedirs(run_dir, exist_ok=True)
    try:
        name, ports, block = sd.load_subckt(NETLIST)
        sized = size_block(block, d)
        snm_block = sized
        if sample is not None and sample != "":
            geo = sd.device_geometry(sized)
            bases = sd.device_bases(sized)
            rng = np.random.default_rng([int(seed), int(sample)] + [int(round(float(d[k]) * 1e4)) for k in KEYS])
            dv = {}
            for b, k in bases:
                w, l = geo[b]
                dv[b] = rng.normal(0, (AVT_N if k == "n" else AVT_P) / np.sqrt(w * l))
            snm_block = sd.mismatch_block(sized, name, dv)
        snms = []
        for loop in CELL["loops"]:
            s = snm_loop(snm_block, sized, name, ports, loop, corner, temp, vdd, run_dir)
            row[f"snm_{loop['name']}_mV"] = s * 1e3
            snms.append(s)
        row["snm_mV"] = min(snms) * 1e3
        if mode == "sh":
            period, tr = PERIOD, None
            for _ in range(PERIOD_RETRIES + 1):
                tr = tran(sized, name, ports, corner, temp, vdd, period, 3, run_dir)
                if tr is not None:
                    break
                period *= 2
            row["period_s"] = period if tr is not None else period / 2
            if tr is None:
                row["status"] = "no_switch"
            else:
                row.update(setup_hold(sized, name, ports, corner, temp, vdd, period, run_dir))
        if mode == "full":
            period, tr = PERIOD, None
            for _ in range(PERIOD_RETRIES + 1):
                tr = tran(sized, name, ports, corner, temp, vdd, period, ncyc, run_dir)
                if tr is not None:
                    break
                period *= 2
            row["period_s"] = period if tr is not None else period / 2
            if tr is None:
                row["status"] = "no_switch"
            else:
                row.update(tr)
                row["leak_W"] = leak_dc(sized, name, ports, corner, temp, vdd, run_dir)
    except Exception as e:
        row["status"] = "sim_fail"
        row["error"] = str(e).replace("\n", " ")[:300]
    row["runtime_s"] = round(time.time() - t0, 1)
    shutil.rmtree(run_dir, ignore_errors=True)
    return row


def job_key(r):
    return (tuple(str(norm(r)[k]) for k in KEYS) + (str(r["corner"]), f"{float(r['temp_C']):g}", f"{float(r['VDD_V']):g}",
            str(r["mode"]), str(r.get("sample", ""))))


# Run jobs in parallel and append rows to the csv as they finish. Rows already in the csv
# (except failed ones) are skipped, so an interrupted run can just be restarted.
def run_jobs(jobs, csv_file, workers):
    done = set()
    if os.path.exists(csv_file) and os.path.getsize(csv_file):
        with open(csv_file) as f:
            for r in csv.DictReader(f):
                if r["status"] != "sim_fail":
                    done.add(job_key(r))
    todo = [j for j in jobs if job_key({**j[0], "corner": j[1], "temp_C": j[2], "VDD_V": j[3], "mode": j[4],
                                         "sample": "" if j[6] is None else j[6]}) not in done]
    print(f"{len(jobs)} requested, {len(jobs) - len(todo)} already done, {len(todo)} to simulate ({workers} workers) -> {csv_file}", flush=True)
    new = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
    os.makedirs(RUNS, exist_ok=True)
    with open(csv_file, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        if new:
            w.writeheader()
        with Pool(workers) as pool:
            for n, row in enumerate(pool.imap_unordered(evaluate, todo), 1):
                if row.get("sample") is None:
                    row["sample"] = ""
                w.writerow(row)
                f.flush()
                tc = row.get("tcq_max_s")
                print(f"[{n}/{len(todo)}] " + " ".join(f"{k}={row[k]}" for k in KEYS)
                      + f" {row['corner']}@{row['temp_C']:g}C {row['status']:<9} SNM={row.get('snm_mV', float('nan')):6.1f}mV"
                      + (f" tcq={tc * 1e6:8.2f}us" if tc else "") + (f" {row['error'][:80]}" if row["error"] else ""), flush=True)
    print(f"Saved: {csv_file}", flush=True)


# Space-filling sample of the free variables (Sobol), snapped to the allowed values.
def sobol(n, seed, fixed, free):
    from scipy.stats import qmc
    s = qmc.Sobol(d=len(free), scramble=True, seed=seed).random(n)
    out = []
    for u in s:
        d = dict(fixed)
        for j, k in enumerate(free):
            if k in ("Win_um", "Wfb_um"):
                d[k] = W_LEVELS[min(int(u[j] * len(W_LEVELS)), len(W_LEVELS) - 1)]
            elif k in ("kclk", "kout", "kqb"):
                d[k] = K_LEVELS[min(int(u[j] * len(K_LEVELS)), len(K_LEVELS) - 1)]
            else:
                lo, hi = LIN_BOX if k == "Lin_um" else LFB_BOX
                d[k] = round(round((lo + u[j] * (hi - lo)) / 0.01) * 0.01, 2)
        out.append(norm(d))
    uniq, seen = [], set()
    for d in out:
        key = tuple(d[k] for k in KEYS)
        if key not in seen:
            seen.add(key)
            uniq.append(d)
    return uniq


def read_designs(path):
    with open(path) as f:
        return [norm(r) for r in csv.DictReader(f)]


# Modes: point (one design, print everything), stage-a (loop sizing, SNM only),
# stage-b (input/clock sizing on the passing loops), pvt, mc, setup-hold.
def main():
    ap = argparse.ArgumentParser(description="Role-based sizing runs for DLX4 / DFFX4 (set SUBVT_SEQ_CELL).")
    ap.add_argument("--mode", required=True, choices=["point", "stage-a", "stage-b", "pvt", "mc", "setup-hold"])
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--conds", nargs="+", default=["critical"])
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--csv", default=None)
    ap.add_argument("--source", default=None, help="CSV with design columns (pvt, mc, stage-b loop candidates)")
    ap.add_argument("--cycles", type=int, default=3)
    ap.add_argument("--mc-n", type=int, default=50)
    ap.add_argument("--all-vars", action="store_true", help="stage-b: sweep all six role variables")
    for k in KEYS:
        ap.add_argument("--" + k.split("_")[0].lower(), type=float, default=None)
    a = ap.parse_args()
    conds = sd.parse_conds(a.conds, [VDD_NOM])
    base = dict(DEFAULT)
    for k in KEYS:
        v = getattr(a, k.split("_")[0].lower())
        if v is not None:
            base[k] = v
    base = norm(base)
    if a.mode == "point":
        for c, t, v in conds:
            r = evaluate((base, c, t, v, "full", a.cycles, None, 0))
            for k in FIELDS:
                if r.get(k) not in (None, ""):
                    print(f"  {k:<16} {r[k]}")
        return
    csv_file = a.csv or f"{a.mode}_{CELL_NAME}.csv"
    jobs = []
    if a.mode == "stage-a":
        designs = sobol(a.n, a.seed, base, ["Wfb_um", "Lfb_um", "kout"])
        print(f"stage A: {len(designs)} loop designs (Wfb, Lfb, kout) x {len(conds)} conditions, DC SNM only")
        jobs = [(d, c, t, v, "snm", 0, None, 0) for d in designs for c, t, v in conds]
    elif a.mode == "stage-b" and a.all_vars:
        designs = sobol(a.n, a.seed, base, KEYS)
        print(f"stage B: {len(designs)} designs (all six role variables) x {len(conds)} conditions")
        jobs = [(d, c, t, v, "full", a.cycles, None, 0) for d in designs for c, t, v in conds]
    elif a.mode == "stage-b":
        loops = read_designs(a.source) if a.source else [base]
        designs = []
        for lp in loops:
            fixed = {**base, "Wfb_um": lp["Wfb_um"], "Lfb_um": lp["Lfb_um"], "kout": lp["kout"]}
            designs += sobol(a.n, a.seed, fixed, ["Win_um", "Lin_um", "kclk"])
        print(f"stage B: {len(designs)} designs (Win, Lin, kclk for {len(loops)} loop sizings) x {len(conds)} conditions")
        jobs = [(d, c, t, v, "full", a.cycles, None, 0) for d in designs for c, t, v in conds]
    elif a.mode == "pvt":
        designs = read_designs(a.source)
        jobs = [(d, c, t, v, "full", a.cycles, None, 0) for d in designs for c, t, v in conds]
    elif a.mode == "setup-hold":
        designs = read_designs(a.source) if a.source else [base]
        jobs = [(d, c, t, v, "sh", 0, None, 0) for d in designs for c, t, v in conds]
    elif a.mode == "mc":
        designs = read_designs(a.source)
        jobs = [(d, c, t, v, "snm", 0, s, a.seed) for d in designs for c, t, v in conds for s in range(a.mc_n)]
        print(f"{len(jobs)} Monte Carlo runs requested")
    run_jobs(jobs, csv_file, a.workers)


if __name__ == "__main__":
    main()
