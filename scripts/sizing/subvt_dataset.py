#!/usr/bin/env python3
import argparse
import csv
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

from cells import CELL, CELL_NAME

BASE_DIR_CANDIDATES = [
    os.environ.get("SUBVT_BASE_DIR", ""),
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "/foss/designs/SUB-VT_STD_CELL_LIB",
]
CELL_REL = CELL["netlist"]
CELL_NETLIST_RELS = (CELL_REL, CELL_REL.lower())
INPUTS = [x.upper() for x in CELL["inputs"]]
OUTPUT = CELL["output"].upper()
NC = CELL.get("nc")
FIXED = {k.upper(): v for k, v in CELL.get("fixed", {}).items()}
W_SCALE = {k.upper(): float(v) for k, v in CELL.get("w_scale", {}).items()}


def snap_scaled(w):
    levels = [0.42] + [round(0.84 * i, 2) for i in range(1, 13)]
    return min(levels, key=lambda x: (abs(x - w), x))


def _arcs():
    if CELL.get("arcs"):
        out, seen = [], {}
        for a in CELL["arcs"]:
            pin = a["pin"].upper()
            seen[pin] = seen.get(pin, 0) + 1
            out.append({"pin": pin, "side": {k.upper(): int(v) for k, v in a.get("side", {}).items()},
                        "inv": bool(a.get("inv", True)), "label": a.get("label", pin)})
        return out
    return [{"pin": p, "side": {q: NC for q in INPUTS if q != p}, "inv": True, "label": p} for p in INPUTS]


ARCS = _arcs()
for _a in ARCS:
    if set(_a["side"]) != set(INPUTS) - {_a["pin"]}:
        raise SystemExit(f"cells.py: arc {_a['label']} must set every other input ({sorted(set(INPUTS) - {_a['pin']})})")
ARC_LABELS = [a["label"] for a in ARCS]
if len(set(ARC_LABELS)) != len(ARC_LABELS):
    raise SystemExit("cells.py: arc labels must be unique")

MODEL_LIB_CANDIDATES = [
    os.environ.get("SUBVT_MODEL_LIB", ""),
    os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "sky130A"), "libs.tech/combined/sky130.lib.spice"),
    os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "sky130A"), "libs.tech/ngspice/sky130.lib.spice"),
]
MODEL_LIB = next((m for m in MODEL_LIB_CANDIDATES if m and os.path.isfile(m)), MODEL_LIB_CANDIDATES[1])

from spec import (area_um2, KEY, L_MIN, W_STEP, split_fingers, snap_design, BOX_LO, BOX_HI, AVT_N, AVT_P, BASELINE, CRITICAL, FANOUT, L_STEP, PVT_CORNERS, PVT_TEMPS, VDD_NOM, VDD_TOL)

TEMPERATURE = 27.0
SCALE = 1e-6


ADD_GEOMETRY_PARAMS = True

DC_STEP = 0.001
EDGE_TIME = 50e-9
PERIOD = 40e-6
N_CYCLES = 5
TSTEP = 20e-9
GMIN = None
NGSPICE_TIMEOUT = 600
PERIOD_RETRIES = 3
SLEW_LO, SLEW_HI = 0.3, 0.7
SETTLE = 0.1
KEEP_RUN_DIRS = False


def _find_base_dir():
    tried = []
    for b in BASE_DIR_CANDIDATES:
        if not b:
            continue
        for rel in CELL_NETLIST_RELS:
            p = os.path.join(b, rel)
            tried.append(p)
            if os.path.isfile(p):
                return b, p
    raise FileNotFoundError(f"{CELL_NAME} netlist not found. Tried:\n  " + "\n  ".join(tried)
                            + "\nSet SUBVT_BASE_DIR to the repository folder.")


BASE_DIR, CELL_NETLIST = _find_base_dir()
OUTPUT_DIR = os.environ.get("SUBVT_OUT_DIR") or os.path.join(BASE_DIR, "sizing_work", "sim")
RUNS_DIR = os.path.join(OUTPUT_DIR, "runs")
os.makedirs(RUNS_DIR, exist_ok=True)

FIELDS = [
    "Wn_um", "Wp_um", "Ln_um", "Lp_um", "fingers_n", "fingers_p", "corner", "period_s", "VDD_V", "temp_C",
    "fanout", "load_F", "status", "func_ok",
    "VIL_V", "VIH_V", "VOL_V", "VOH_V", "NMH_V", "NML_V", "NM_min_V", "NM_min_norm",
    "Vm_V", "Vm_dev_norm", "worst_arc", "vout_max_V", "vout_min_V", "NM_fwd_V", "NM_rev_V", "dc_hyst_mV",
    "tp_cycle_diff", "e_cycle_diff",
    "tpHL_s", "tpLH_s", "tp_max_s", "tp_avg_s", "trise_s", "tfall_s",
    "asym_tp", "asym_slew",
    "leak_low_W", "leak_high_W", "leakage_avg_W", "leakage_max_W",
    "avg_power_W", "energy_cycle_J", "dyn_energy_cycle_J", "energy_op_J", "pdp_J", "edp_Js",
    "area_proxy_um2", "runtime_s",
] + [f"NM_arc_{l}_V" for l in ARC_LABELS] + [f"tp_arc_{l}_s" for l in ARC_LABELS] + [f"asym_slew_arc_{l}" for l in ARC_LABELS]

W_RE = re.compile(r"(?<![A-Za-z0-9_])W\s*=\s*([^\s]+)", re.I)
L_RE = re.compile(r"(?<![A-Za-z0-9_])L\s*=\s*([^\s]+)", re.I)
NF_RE = re.compile(r"(?<![A-Za-z0-9_])nf\s*=\s*\d+", re.I)
GEOM_RE = re.compile(r"(?<![A-Za-z0-9_])(ad|as|pd|ps|nrd|nrs)\s*=\s*('[^']*'|\S+)", re.I)


def load_subckt(path):
    with open(path) as f:
        text = f.read()
    lines = []
    for ln in text.splitlines():
        if ln.lstrip().startswith("+") and lines:
            lines[-1] += " " + ln.lstrip()[1:].strip()
        else:
            lines.append(ln.rstrip())
    block, inside = [], False
    for ln in lines:
        low = ln.strip().lower()
        if low.startswith(".subckt"):
            inside = True
        if inside:
            block.append(ln)
            if low.startswith(".ends"):
                break
    if not block:
        raise RuntimeError(f"No .subckt found in {path}")
    head = block[0].split()
    return head[1], [p for p in head[2:] if "=" not in p], block


def device_kind(line):
    if not re.match(r"^\s*x", line, re.I):
        return None
    low = line.lower()
    if "nfet_01v8" in low:
        return "n"
    if "pfet_01v8" in low:
        return "p"
    return None


def _to_float(tok, what):
    try:
        return float(tok.strip("'\"{}"))
    except ValueError:
        raise RuntimeError(f"{what}={tok!r} is not a plain number in {CELL_NETLIST}")


def read_geometry(block):
    wn = wp = L = None
    for ln in block:
        k = device_kind(ln)
        if k is None:
            continue
        mw, ml = W_RE.search(ln), L_RE.search(ln)
        if not mw or not ml:
            raise RuntimeError(f"Cannot find W= / L= in device line:\n{ln}")
        w = _to_float(mw.group(1), "W")
        if k == "n" and wn is None:
            wn = w
        if k == "p" and wp is None:
            wp = w
        if L is None:
            L = _to_float(ml.group(1), "L")
    if wn is None or wp is None:
        raise RuntimeError("Did not find both an nfet_01v8 and a pfet_01v8 line.")
    return wn, wp, L


def geometry_params(w, nf):
    d = 0.29
    ad = int((nf + 1) / 2) * w / nf * d
    as_ = int((nf + 2) / 2) * w / nf * d
    pd = 2 * int((nf + 1) / 2) * (w / nf + d)
    ps = 2 * int((nf + 2) / 2) * (w / nf + d)
    nr = d / w
    return f"ad={ad:.6g} as={as_:.6g} pd={pd:.6g} ps={ps:.6g} nrd={nr:.6g} nrs={nr:.6g}"


def set_widths(block, wn, wp, ln, lp):
    out, seen = [], set()
    for ln_ in block:
        k = device_kind(ln_)
        if k is None:
            out.append(ln_)
            continue
        toks = ln_.split()
        dev = toks[0].upper()
        if dev in FIXED:
            w, length = FIXED[dev]
        else:
            w = wn if k == "n" else wp
            length = ln if k == "n" else lp
            if dev in W_SCALE:
                w = snap_scaled(w * W_SCALE[dev])
            seen.add(k)
        for i, (wf, nf) in enumerate(split_fingers(w)):
            t = list(toks)
            t[0] = f"{toks[0]}_f{i}"
            line = " ".join(t)
            line = W_RE.sub(lambda mm: f"W={wf * nf:g}", line)
            line = L_RE.sub(lambda mm: f"L={length:g}", line)
            line = NF_RE.sub(f"nf={nf}", line) if NF_RE.search(line) else line + f" nf={nf}"
            if ADD_GEOMETRY_PARAMS:
                line = GEOM_RE.sub("", line).rstrip() + " " + geometry_params(wf * nf, nf)
            out.append(line)
    if seen != {"n", "p"}:
        raise RuntimeError("Could not modify transistor widths in the netlist.")
    return out


def port_roles(ports):
    roles = []
    for p in ports:
        k = p.upper()
        if k in INPUTS:
            roles.append("in:" + k)
        elif k == OUTPUT:
            roles.append("out")
        elif k in ("VDD", "VPWR"):
            roles.append("vdd")
        elif k in ("GND", "VSS", "VGND"):
            roles.append("gnd")
        else:
            raise RuntimeError(f"Unknown subcircuit port '{p}' (inputs {INPUTS}, output {OUTPUT}, VDD, GND).")
    return roles


def inst(ports, name, sub, pins, n_out, n_vdd):
    m = {"out": n_out, "vdd": n_vdd, "gnd": "0"}
    return f"{name} " + " ".join(pins[r[3:]] if r.startswith("in:") else m[r] for r in port_roles(ports)) + f" {sub}"


def arc_pins(arc, node_sw):
    return {p: (node_sw if p == arc["pin"] else ("nside_hi" if arc["side"][p] else "0")) for p in INPUTS}


def nc_sources(arc, vdd):
    if len(INPUTS) == 1:
        return ""
    return f"Vside_hi nside_hi 0 DC {vdd:g}"


def header(block, corner, temp):
    gmin = f".option gmin={GMIN:g}" if GMIN else ""
    return (f".option scale={SCALE:g}\n{gmin}\n.temp {temp:g}\n.lib \"{MODEL_LIB}\" {corner}\n\n"
            + "\n".join(block) + "\n")


def loads(ports, sub, pins, prefix, n_vdd, count):
    return "\n".join(inst(ports, f"X{prefix}{i}", sub, pins, f"{prefix}o{i}", n_vdd) for i in range(1, count + 1))


def cap_line(load_cap):
    return f"CLOAD y 0 {load_cap:g}" if load_cap > 0 else "* no load capacitor"


BASE_RE = re.compile(r"_f\d+$")


def device_bases(block):
    seen = []
    for ln in block:
        k = device_kind(ln)
        if k is None:
            continue
        b = BASE_RE.sub("", ln.split()[0])
        if (b, k) not in seen:
            seen.append((b, k))
    return seen


def device_geometry(block):
    geo = {}
    for ln in block:
        if device_kind(ln) is None:
            continue
        b = BASE_RE.sub("", ln.split()[0])
        w = float(W_RE.search(ln).group(1))
        l = float(L_RE.search(ln).group(1))
        geo[b] = (geo.get(b, (0.0, l))[0] + w, l)
    return geo


def mismatch_block(block, name, dv):
    out = []
    for ln in block:
        low = ln.strip().lower()
        if low.startswith(".subckt"):
            toks = ln.split()
            toks[1] = name + "_mm"
            out.append(" ".join(toks))
            continue
        if low.startswith(".ends"):
            out.append(".ends")
            continue
        k = device_kind(ln)
        if k is None:
            out.append(ln)
            continue
        toks = ln.split()
        dev, gate = toks[0], toks[2]
        gi = f"{dev}_gmm"
        toks[2] = gi
        out.append(" ".join(toks))
        shift = dv[BASE_RE.sub("", dev)]
        out.append(f"V{dev}_mm {gi} {gate} DC {(-shift if k == 'n' else shift):.9g}")
    return out


def build_dc_tb(block, name, ports, corner, vdd, temp, fanout, load_cap, arc=None, dut_block=None):
    arc = arc or ARCS[0]
    sw = arc["label"]
    dut_name = name
    extra = ""
    if dut_block is not None:
        dut_name = name + "_mm"
        extra = "\n".join(dut_block) + "\n"
    return f"""* DC testbench, switching input {sw}
{header(block, corner, temp)}
{extra}
VSUP vddd 0 DC {vdd}
VAUX vddx 0 DC {vdd}
VIN a 0 DC 0
{nc_sources(arc, vdd)}
{inst(ports, "XDUT", dut_name, arc_pins(arc, "a"), "y", "vddd")}
{loads(ports, name, arc_pins(arc, "y"), "L", "vddx", fanout)}
{cap_line(load_cap)}

.control
set noaskquit
set wr_singlescale
set numdgt=10
dc VIN 0 {vdd} {DC_STEP}
wrdata dc_data.txt v(a) v(y) i(VSUP)
dc VIN {vdd} 0 -{DC_STEP}
wrdata dc_data_rev.txt v(a) v(y) i(VSUP)
quit
.endc

.end
"""


def vectors():
    n = len(INPUTS)
    return [tuple((i >> (n - 1 - j)) & 1 for j in range(n)) for i in range(2 ** n)]


def build_vec_tb(block, name, ports, corner, vdd, temp):
    srcs = "\n".join(f"VI_{p.lower()} {p.lower()}_in 0 DC 0" for p in INPUTS)
    pins = {p: p.lower() + "_in" for p in INPUTS}
    cmds = []
    for i, v in enumerate(vectors()):
        cmds += [f"alter VI_{p.lower()} dc = {b * vdd:g}" for p, b in zip(INPUTS, v)] + ["op", f"wrdata vec_{i}.txt v(y) i(VSUP)"]
    body = "\n".join(cmds)
    return f"""* static vector testbench (leakage and truth table)
{header(block, corner, temp)}
VSUP vddd 0 DC {vdd}
{srcs}
{inst(ports, "XDUT", name, pins, "y", "vddd")}

.control
set noaskquit
set wr_singlescale
set numdgt=10
{body}
quit
.endc

.end
"""


def build_tran_tb(block, name, ports, corner, vdd, temp, fanout, load_cap, period, arc=None):
    arc = arc or ARCS[0]
    sw = arc["label"]
    pw = period / 2 - EDGE_TIME
    sim_time = N_CYCLES * period
    tstep = min(TSTEP, period / 2000)
    return f"""* transient testbench, switching input {sw}, FO{fanout} driver stage and FO{fanout} load
{header(block, corner, temp)}
VSUP vddd 0 DC {vdd}
VAUX vddx 0 DC {vdd}
VPUL x 0 DC 0 PULSE(0 {vdd} 0 {EDGE_TIME:g} {EDGE_TIME:g} {pw:g} {period:g})
{nc_sources(arc, vdd)}
{inst(ports, "XDRV", name, arc_pins(arc, "x"), "a", "vddx")}
{loads(ports, name, arc_pins(arc, "a"), "D", "vddx", max(fanout - 1, 0))}
{inst(ports, "XDUT", name, arc_pins(arc, "a"), "y", "vddd")}
{loads(ports, name, arc_pins(arc, "y"), "L", "vddx", fanout)}
{cap_line(load_cap)}

.control
set noaskquit
set wr_singlescale
set numdgt=10
tran {tstep:g} {sim_time:g}
wrdata tran_data.txt v(a) v(y) i(VSUP)
quit
.endc

.end
"""


def run_ngspice(run_dir, tb_name, outfile):
    for f in (outfile, tb_name + ".log"):
        p = os.path.join(run_dir, f)
        if os.path.exists(p):
            os.remove(p)
    try:
        subprocess.run(["ngspice", "-b", "-o", tb_name + ".log", tb_name],
                       cwd=run_dir, capture_output=True, text=True, timeout=NGSPICE_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise RuntimeError("ngspice timeout")
    p = os.path.join(run_dir, outfile)
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        log = ""
        lp = os.path.join(run_dir, tb_name + ".log")
        if os.path.exists(lp):
            with open(lp, errors="replace") as fh:
                log = fh.read()[-800:]
        raise RuntimeError(f"ngspice did not produce {outfile}\n{log}")


def dc_metrics(path, vdd, inv=True):
    d = np.loadtxt(path)
    vin, vout, isup = d[:, 0], d[:, 2], d[:, 3]
    if not inv:
        return dc_metrics_noninv(vin, vout, isup, vdd)
    res = {
        "leak_low_W": vdd * abs(isup[0]),
        "leak_high_W": vdd * abs(isup[-1]),
        "vout_max_V": float(vout.max()),
        "vout_min_V": float(vout.min()),
    }
    dv = vout - vin
    k = np.where(dv[:-1] * dv[1:] <= 0)[0]
    if len(k):
        i = k[0]
        den = dv[i + 1] - dv[i]
        vm = float(vin[i] + (-dv[i]) * (vin[i + 1] - vin[i]) / den) if den != 0 else float(vin[i])
        res["Vm_V"] = vm
        res["Vm_dev_norm"] = (vm - vdd / 2) / vdd
    gain = np.gradient(vout, vin)
    s = gain + 1.0
    idx = np.where(s[:-1] * s[1:] < 0)[0]
    if len(idx) < 2:
        return res, False

    def at(i):
        return vin[i] + (-1.0 - gain[i]) * (vin[i + 1] - vin[i]) / (gain[i + 1] - gain[i])

    vil, vih = float(at(idx[0])), float(at(idx[-1]))
    voh = float(np.interp(vil, vin, vout))
    vol = float(np.interp(vih, vin, vout))
    res.update(VIL_V=vil, VIH_V=vih, VOH_V=voh, VOL_V=vol, NMH_V=voh - vih, NML_V=vil - vol)
    res["NM_min_V"] = min(res["NMH_V"], res["NML_V"])
    res["NM_min_norm"] = res["NM_min_V"] / vdd
    return res, True


def dc_metrics_noninv(vin, vout, isup, vdd):
    res = {
        "leak_low_W": vdd * abs(isup[0]),
        "leak_high_W": vdd * abs(isup[-1]),
        "vout_max_V": float(vout.max()),
        "vout_min_V": float(vout.min()),
    }
    dv = vout - vdd / 2
    k = np.where(dv[:-1] * dv[1:] <= 0)[0]
    if len(k):
        i = k[0]
        den = dv[i + 1] - dv[i]
        vm = float(vin[i] + (-dv[i]) * (vin[i + 1] - vin[i]) / den) if den != 0 else float(vin[i])
        res["Vm_V"] = vm
        res["Vm_dev_norm"] = (vm - vdd / 2) / vdd
    gain = np.gradient(vout, vin)
    s = gain - 1.0
    idx = np.where(s[:-1] * s[1:] < 0)[0]
    if len(idx) < 2:
        return res, False

    def at(i):
        return vin[i] + (1.0 - gain[i]) * (vin[i + 1] - vin[i]) / (gain[i + 1] - gain[i])

    vil, vih = float(at(idx[0])), float(at(idx[-1]))
    vol = float(np.interp(vil, vin, vout))
    voh = float(np.interp(vih, vin, vout))
    res.update(VIL_V=vil, VIH_V=vih, VOH_V=voh, VOL_V=vol, NMH_V=voh - vih, NML_V=vil - vol)
    res["NM_min_V"] = min(res["NMH_V"], res["NML_V"])
    res["NM_min_norm"] = res["NM_min_V"] / vdd
    return res, True


def dc_full(run_dir, vdd, inv=True):
    fwd, ok_f = dc_metrics(os.path.join(run_dir, "dc_data.txt"), vdd, inv)
    p = os.path.join(run_dir, "dc_data_rev.txt")
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        raise RuntimeError("reverse DC sweep produced no data")
    rev_raw = np.loadtxt(p)[::-1]
    tmp = os.path.join(run_dir, "dc_data_rev_sorted.txt")
    np.savetxt(tmp, rev_raw)
    rev, ok_r = dc_metrics(tmp, vdd, inv)
    fw = np.loadtxt(os.path.join(run_dir, "dc_data.txt"))
    res = dict(fwd)
    n = min(len(fw), len(rev_raw))
    res["dc_hyst_mV"] = float(np.max(np.abs(np.interp(fw[:, 0], rev_raw[:, 0], rev_raw[:, 2]) - fw[:, 2])) * 1e3)
    if ok_f and ok_r:
        res["NM_fwd_V"], res["NM_rev_V"] = fwd["NM_min_V"], rev["NM_min_V"]
        for k in ("NM_min_V", "NMH_V", "NML_V"):
            res[k] = min(fwd[k], rev[k])
        res["NM_min_norm"] = res["NM_min_V"] / vdd
        return res, True
    return res, False


def crossings(t, v, level, rising):
    s = v - level
    if rising:
        i = np.where((s[:-1] < 0) & (s[1:] >= 0))[0]
    else:
        i = np.where((s[:-1] > 0) & (s[1:] <= 0))[0]
    return t[i] + (-s[i]) * (t[i + 1] - t[i]) / (s[i + 1] - s[i])


def first_after(tc, t0, t1):
    c = tc[(tc >= t0) & (tc <= t1)]
    return float(c[0]) if len(c) else None


def asym(a, b):
    m = max(a, b)
    return abs(a - b) / m if m > 0 else None


def tran_metrics(path, leakage_avg_W, vdd, back=0, inv=True):
    d = np.loadtxt(path)
    t, vin, vout, ivdd = d[:, 0], d[:, 1], d[:, 2], d[:, 3]
    if not inv:
        vout = vdd - vout
    half, lo, hi = vdd / 2, SLEW_LO * vdd, SLEW_HI * vdd

    in_r = crossings(t, vin, half, True)
    in_f = crossings(t, vin, half, False)
    if len(in_r) < 2 + back or len(in_f) < 1:
        return {}, False
    t_r = in_r[-2 - back]
    later_f = in_f[in_f > t_r]
    if len(later_f) == 0:
        return {}, False
    t_f = later_f[0]
    t_end = in_r[-1 - back]
    T = t_end - t_r

    y_low = float(np.interp(t_f - 0.01 * T, t, vout))
    y_high = float(np.interp(t_end - 0.01 * T, t, vout))
    settled = (y_low <= SETTLE * vdd) and (y_high >= (1 - SETTLE) * vdd)

    o_f_half, o_r_half = crossings(t, vout, half, False), crossings(t, vout, half, True)
    o_f_hi, o_f_lo = crossings(t, vout, hi, False), crossings(t, vout, lo, False)
    o_r_lo, o_r_hi = crossings(t, vout, lo, True), crossings(t, vout, hi, True)

    a = first_after(o_f_half, t_r, t_f)
    b = first_after(o_r_half, t_f, t_end)
    tpHL = a - t_r if a is not None else None
    tpLH = b - t_f if b is not None else None

    a, b = first_after(o_f_hi, t_r, t_f), first_after(o_f_lo, t_r, t_f)
    tfall = b - a if (a is not None and b is not None) else None
    a, b = first_after(o_r_lo, t_f, t_end), first_after(o_r_hi, t_f, t_end)
    trise = b - a if (a is not None and b is not None) else None

    m = (t >= t_r) & (t <= t_end)
    tt, ii = t[m], ivdd[m]
    energy = -vdd * float(np.sum(0.5 * (ii[1:] + ii[:-1]) * np.diff(tt)))

    res = {
        "tpHL_s": tpHL, "tpLH_s": tpLH, "trise_s": trise, "tfall_s": tfall,
        "avg_power_W": energy / T,
        "energy_cycle_J": energy,
        "dyn_energy_cycle_J": energy - leakage_avg_W * T,
    }
    if tpHL is not None and tpLH is not None:
        res["tp_max_s"] = max(tpHL, tpLH)
        res["tp_avg_s"] = 0.5 * (tpHL + tpLH)
        res["asym_tp"] = asym(tpHL, tpLH)
        e_op = res["dyn_energy_cycle_J"] + leakage_avg_W * (tpHL + tpLH)
        res["energy_op_J"] = e_op
        res["pdp_J"] = 0.5 * e_op
        res["edp_Js"] = e_op * res["tp_max_s"]
    if not inv:
        res["tpHL_s"], res["tpLH_s"] = res["tpLH_s"], res["tpHL_s"]
        res["trise_s"], res["tfall_s"] = res["tfall_s"], res["trise_s"]
    if trise is not None and tfall is not None:
        res["asym_slew"] = asym(trise, tfall)
    ok = settled and all(res.get(k) is not None for k in ("tpHL_s", "tpLH_s", "trise_s", "tfall_s"))
    return res, ok


def dc_cell(block, name, ports, corner, vdd, temp, fanout, load_cap, run_dir, dut_block=None):
    per, ok_all = {}, True
    for arc in ARCS:
        with open(os.path.join(run_dir, "tb_dc.cir"), "w") as f:
            f.write(build_dc_tb(block, name, ports, corner, vdd, temp, fanout, load_cap, arc, dut_block))
        run_ngspice(run_dir, "tb_dc.cir", "dc_data.txt")
        dc, ok = dc_full(run_dir, vdd, arc["inv"])
        per[arc["label"]] = (dc, ok)
        ok_all = ok_all and ok
    if ok_all:
        worst = min(ARC_LABELS, key=lambda p: per[p][0]["NM_min_V"])
    else:
        worst = next(p for p in ARC_LABELS if not per[p][1])
    res = dict(per[worst][0])
    res["worst_arc"] = worst
    res["vout_max_V"] = min(per[p][0]["vout_max_V"] for p in ARC_LABELS)
    res["vout_min_V"] = max(per[p][0]["vout_min_V"] for p in ARC_LABELS)
    res["dc_hyst_mV"] = max(per[p][0].get("dc_hyst_mV", 0.0) for p in ARC_LABELS)
    for p in ARC_LABELS:
        if per[p][1]:
            res[f"NM_arc_{p}_V"] = per[p][0]["NM_min_V"]
    return res, ok_all, per


def read_vectors(run_dir, vdd):
    out = {}
    for i, v in enumerate(vectors()):
        a = np.loadtxt(os.path.join(run_dir, f"vec_{i}.txt")).ravel()
        out[v] = (float(a[1]), vdd * abs(float(a[2])))
    return out


def function_ok(vec, vdd):
    for v, (vy, _) in vec.items():
        if CELL["func"](v):
            if vy < 0.8 * vdd:
                return False
        elif vy > 0.2 * vdd:
            return False
    return True


def arc_leak(vec, arc):
    vals = []
    for b in (0, 1):
        v = tuple(b if p == arc["pin"] else arc["side"][p] for p in INPUTS)
        vals.append(vec[v][1])
    return 0.5 * sum(vals)


AGG_MAX = ("tpHL_s", "tpLH_s", "trise_s", "tfall_s", "tp_max_s", "tp_avg_s", "avg_power_W", "energy_cycle_J", "dyn_energy_cycle_J",
           "energy_op_J", "pdp_J", "edp_Js", "asym_tp", "asym_slew", "tp_cycle_diff", "e_cycle_diff")


def tran_cell(block, name, ports, corner, vdd, temp, fanout, load_cap, run_dir, vec):
    period_max = PERIOD
    agg, per_tp, per_slew = {}, {}, {}
    for arc in ARCS:
        period = PERIOD
        sw, inv = arc["label"], arc["inv"]
        lk = arc_leak(vec, arc)
        tr, tr_ok = {}, False
        for attempt in range(PERIOD_RETRIES + 1):
            with open(os.path.join(run_dir, "tb_tran.cir"), "w") as f:
                f.write(build_tran_tb(block, name, ports, corner, vdd, temp, fanout, load_cap, period, arc))
            run_ngspice(run_dir, "tb_tran.cir", "tran_data.txt")
            tr, tr_ok = tran_metrics(os.path.join(run_dir, "tran_data.txt"), lk, vdd, inv=inv)
            if tr_ok:
                prev, prev_ok = tran_metrics(os.path.join(run_dir, "tran_data.txt"), lk, vdd, back=1, inv=inv)
                if prev_ok and prev.get("tp_max_s") and tr.get("tp_max_s"):
                    tr["tp_cycle_diff"] = abs(prev["tp_max_s"] - tr["tp_max_s"]) / tr["tp_max_s"]
                    tr["e_cycle_diff"] = abs(prev["energy_op_J"] - tr["energy_op_J"]) / max(abs(tr["energy_op_J"]), 1e-30)
                else:
                    tr_ok = False
            if tr_ok or attempt == PERIOD_RETRIES:
                break
            period *= 2
        period_max = max(period_max, period)
        if not tr_ok:
            return {}, False, period_max
        per_tp[sw] = tr["tp_max_s"]
        per_slew[sw] = tr.get("asym_slew")
        for k in AGG_MAX:
            if tr.get(k) is not None:
                agg[k] = max(agg.get(k, tr[k]), tr[k])
    for sw, v in per_tp.items():
        agg[f"tp_arc_{sw}_s"] = v
        agg[f"asym_slew_arc_{sw}"] = per_slew[sw]
    return agg, True, period_max


def evaluate(wn, wp, ln, lp, corner="tt", temp=None, vdd=None, fanout=FANOUT, load_cap=0.0,
             run_id=None, keep=KEEP_RUN_DIRS):
    t0 = time.time()
    temp = TEMPERATURE if temp is None else float(temp)
    vdd = VDD_NOM if vdd is None else float(vdd)
    row = {
        "Wn_um": wn, "Wp_um": wp, "Ln_um": ln, "Lp_um": lp, "corner": corner, "VDD_V": vdd,
        "temp_C": temp, "fanout": fanout, "load_F": load_cap, "status": "ok",
        "area_proxy_um2": area_um2(wn, wp, ln, lp),
    }
    run_id = run_id or f"wn{wn:g}_wp{wp:g}_ln{ln:g}_lp{lp:g}_{corner}_t{temp:g}_v{vdd:g}_fo{fanout}_cl{load_cap:g}_pid{os.getpid()}"
    run_dir = os.path.join(RUNS_DIR, run_id)
    if os.path.isdir(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(run_dir)

    try:
        name, ports, block = load_subckt(CELL_NETLIST)
        block = set_widths(block, wn, wp, ln, lp)
        row["fingers_n"] = "+".join(f"{n}x{w:g}" for w, n in split_fingers(wn))
        row["fingers_p"] = "+".join(f"{n}x{w:g}" for w, n in split_fingers(wp))

        with open(os.path.join(run_dir, "tb_vec.cir"), "w") as f:
            f.write(build_vec_tb(block, name, ports, corner, vdd, temp))
        run_ngspice(run_dir, f"tb_vec.cir", f"vec_{len(vectors()) - 1}.txt")
        vec = read_vectors(run_dir, vdd)
        row["func_ok"] = int(function_ok(vec, vdd))
        leaks = [x[1] for x in vec.values()]
        leak = sum(leaks) / len(leaks)
        row["leakage_avg_W"], row["leakage_max_W"] = leak, max(leaks)
        row["leak_low_W"], row["leak_high_W"] = min(leaks), max(leaks)

        dc, dc_ok, _ = dc_cell(block, name, ports, corner, vdd, temp, fanout, load_cap, run_dir)
        row.update(dc)
        row["leak_low_W"], row["leak_high_W"] = min(leaks), max(leaks)

        tr, tr_ok, period = {}, False, PERIOD
        if dc_ok and row["func_ok"]:
            tr, tr_ok, period = tran_cell(block, name, ports, corner, vdd, temp, fanout, load_cap, run_dir, vec)
        row.update(tr)
        row["period_s"] = period
        if not row["func_ok"]:
            row["status"] = "wrong_function"
        elif not dc_ok:
            row["status"] = "no_gain"
        elif not tr_ok:
            row["status"] = "no_switch"
    except Exception as e:
        row["status"] = "sim_fail"
        row["error"] = str(e)[:300]
        keep = True

    row["runtime_s"] = time.time() - t0
    if not keep:
        shutil.rmtree(run_dir, ignore_errors=True)
    return row


def sigma_vth(wn, wp, ln, lp):
    return AVT_N / np.sqrt(wn * ln), AVT_P / np.sqrt(wp * lp)


MC_FIELDS = ["Wn_um", "Wp_um", "Ln_um", "Lp_um", "corner", "temp_C", "VDD_V", "sample", "dVthn_mV", "dVthp_mV", "status",
             "VIL_V", "VIH_V", "VOL_V", "VOH_V", "NMH_V", "NML_V", "NM_min_V", "Vm_V", "leakage_avg_W", "error"]


def evaluate_mc(wn, wp, ln, lp, corner, temp, vdd, sample, seed):
    rng = np.random.default_rng([seed, int(round(wn * 1e4)), int(round(wp * 1e4)), int(round(ln * 1e4)), int(round(lp * 1e4)), sample])
    name, ports, block = load_subckt(CELL_NETLIST)
    block = set_widths(block, wn, wp, ln, lp)
    bases = device_bases(block)
    geo = device_geometry(block)
    nn = [b for b, k in bases if k == "n"]
    npp = [b for b, k in bases if k == "p"]
    dvn = rng.normal(0, 1, size=len(nn)) * np.array([AVT_N / np.sqrt(geo[b][0] * geo[b][1]) for b in nn])
    dvp = rng.normal(0, 1, size=len(npp)) * np.array([AVT_P / np.sqrt(geo[b][0] * geo[b][1]) for b in npp])
    dv = dict(zip(nn, dvn))
    dv.update(zip(npp, dvp))
    row = {"Wn_um": wn, "Wp_um": wp, "Ln_um": ln, "Lp_um": lp, "corner": corner, "temp_C": temp, "VDD_V": vdd, "sample": sample,
           "dVthn_mV": ";".join(f"{x * 1e3:.3f}" for x in dvn), "dVthp_mV": ";".join(f"{x * 1e3:.3f}" for x in dvp), "status": "ok"}
    run_dir = os.path.join(RUNS_DIR, f"mc_wn{wn:g}_wp{wp:g}_ln{ln:g}_lp{lp:g}_{corner}_t{temp:g}_v{vdd:g}_s{sample}_pid{os.getpid()}")
    if os.path.isdir(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(run_dir)
    try:
        dut = mismatch_block(block, name, dv)
        dc, ok, per = dc_cell(block, name, ports, corner, vdd, temp, FANOUT, 0.0, run_dir, dut_block=dut)
        row.update(dc)
        row["leakage_avg_W"] = float(np.mean([0.5 * (per[p][0]["leak_low_W"] + per[p][0]["leak_high_W"]) for p in ARC_LABELS]))
        if not ok:
            row["status"] = "no_gain"
    except Exception as e:
        row["status"] = "sim_fail"
        row["error"] = str(e)[:200]
    shutil.rmtree(run_dir, ignore_errors=True)
    return row


def mc_run(designs, conds, n, seed, workers, resume, csv_file, force):
    if os.path.exists(csv_file) and not resume and not force:
        raise SystemExit(f"{csv_file} already exists. Use --resume, --force or --csv <other name>.")
    done = set()
    if resume and os.path.exists(csv_file):
        with open(csv_file, newline="") as f:
            for r in csv.DictReader(f):
                done.add((round(float(r["Wn_um"]), 4), round(float(r["Wp_um"]), 4), round(float(r["Ln_um"]), 4),
                          round(float(r["Lp_um"]), 4), r["corner"],
                          round(float(r["temp_C"]), 3), round(float(r["VDD_V"]), 4), int(r["sample"])))
    jobs = [tuple(d) + (c, t, v, k) for d in designs for (c, t, v) in conds for k in range(n)]
    todo = [j for j in jobs if (round(j[0], 4), round(j[1], 4), round(j[2], 4), round(j[3], 4), j[4], round(j[5], 3), round(j[6], 4), j[7]) not in done]
    print(f"{len(jobs)} Monte Carlo runs requested, {len(todo)} to simulate ({workers} workers) -> {csv_file}")
    new_file = not (resume and os.path.exists(csv_file) and os.path.getsize(csv_file) > 0)
    with open(csv_file, "w" if new_file else "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=MC_FIELDS, extrasaction="ignore", restval="")
        if new_file:
            w.writeheader()
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(evaluate_mc, wn, wp, ln, lp, c, t, v, k, seed) for wn, wp, ln, lp, c, t, v, k in todo]
            for i, fu in enumerate(as_completed(futs), 1):
                w.writerow(fu.result())
                if i % 50 == 0:
                    fh.flush()
                    print(f"  [{i}/{len(todo)}]", flush=True)
    print("Saved:", csv_file)


def job_key(wn, wp, ln, lp, corner, temp, vdd, fanout, load_cap):
    return (round(float(wn), 4), round(float(wp), 4), round(float(ln), 4), round(float(lp), 4), corner, round(float(temp), 3),
            round(float(vdd), 4), int(fanout), float(load_cap))


def load_done(csv_path):
    done = set()
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as f:
            for r in csv.DictReader(f):
                if r.get("status") == "ok" and r.get("fanout") not in (None, ""):
                    done.add(job_key(r["Wn_um"], r["Wp_um"], r["Ln_um"], r["Lp_um"], r["corner"], r["temp_C"], r["VDD_V"],
                                     r["fanout"], r["load_F"]))
    return done


def fmt_row(n, total, row):
    nm = row.get("NM_min_V")
    return (f"[{n}/{total}] Wn={row['Wn_um']:g} Wp={row['Wp_um']:g} Ln={row['Ln_um']:g} Lp={row['Lp_um']:g} {row['corner']:>2}@{float(row['temp_C']):g}C "
            f"{float(row['VDD_V']):g}V {row['status']:9s} "
            + (f"NM={nm * 1e3:6.1f}mV " if nm is not None else "")
            + (f"Vm={row['Vm_V'] * 1e3:5.0f}mV " if row.get("Vm_V") is not None else "")
            + (f"tp={row['tp_max_s'] * 1e9:9.1f}ns " if row.get("tp_max_s") else "")
            + (f"asym={row['asym_tp']:.2f} " if row.get("asym_tp") is not None else "")
            + (f"| {row['error'].splitlines()[0]}" if row.get("error") else ""))


def run_jobs(jobs, fanout, load_cap, workers, resume, csv_file, force=False, have=()):
    if os.path.exists(csv_file) and not resume and not force:
        raise SystemExit(f"{csv_file} already exists. Use --resume, --force or --csv <other name>.")
    done = load_done(csv_file) if resume else set()
    for h in have:
        done |= load_done(h)
    todo = [j for j in jobs if job_key(*j, fanout, load_cap) not in done]
    print(f"{len(jobs)} requested, {len(jobs) - len(todo)} already done, {len(todo)} to simulate "
          f"({workers} workers, FO{fanout}, extra cap {load_cap:g} F) -> {csv_file}")
    new_file = not (resume and os.path.exists(csv_file) and os.path.getsize(csv_file) > 0)
    with open(csv_file, "w" if new_file else "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore", restval="")
        if new_file:
            w.writeheader()
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(evaluate, wn, wp, ln, lp, c, t, v, fanout, load_cap, None, KEEP_RUN_DIRS)
                    for wn, wp, ln, lp, c, t, v in todo]
            for n, fu in enumerate(as_completed(futs), 1):
                row = fu.result()
                w.writerow(row)
                fh.flush()
                print(fmt_row(n, len(todo), row), flush=True)
    print("Saved:", csv_file)


def parse_conds(tokens, vdds):
    out = []
    for tok in tokens:
        low = tok.lower()
        if low == "critical":
            out += [(c, t, v) for c, t in CRITICAL for v in vdds]
        elif low == "full15":
            out += [(c, t, v) for c in PVT_CORNERS for t in PVT_TEMPS for v in vdds]
        else:
            p = low.rstrip("c").split("@")
            if len(p) == 3:
                out.append((p[0], float(p[1]), float(p[2])))
            elif len(p) == 2:
                out += [(p[0], float(p[1]), v) for v in vdds]
            else:
                raise SystemExit(f"bad condition '{tok}' (use corner@temp, corner@temp@vdd, critical or full15)")
    seen, res = set(), []
    for c in out:
        if c not in seen:
            seen.add(c)
            res.append(c)
    return res


def read_designs(source, select, n):
    with open(source, newline="") as f:
        rows = list(csv.DictReader(f))
    uniq = {}
    for r in rows:
        if r.get("Wn_um") in (None, ""):
            continue
        k = snap_design(r["Wn_um"], r["Wp_um"], r["Ln_um"], r["Lp_um"])
        uniq[k] = r
    pts = list(uniq.keys())
    if select == "all" or n >= len(pts):
        return pts
    Z = np.log(np.array(pts))
    Z = (Z - Z.min(0)) / np.maximum(Z.max(0) - Z.min(0), 1e-12)
    d0 = np.abs(np.array(pts) - np.array(BASELINE)).sum(1)
    chosen = [int(np.argmin(d0))]
    dist = np.linalg.norm(Z - Z[chosen[0]], axis=1)
    while len(chosen) < n:
        i = int(np.argmax(dist))
        chosen.append(i)
        dist = np.minimum(dist, np.linalg.norm(Z - Z[i], axis=1))
    return [pts[i] for i in chosen]


def sobol_designs(n, seed):
    from scipy.stats import qmc
    from spec import W_LEVELS_N, W_LEVELS_P
    u = qmc.Sobol(d=4, scramble=True, seed=seed).random(n)
    pts = []
    for ui in u:
        wn = W_LEVELS_N[min(int(ui[0] * len(W_LEVELS_N)), len(W_LEVELS_N) - 1)]
        wp = W_LEVELS_P[min(int(ui[1] * len(W_LEVELS_P)), len(W_LEVELS_P) - 1)]
        ln = BOX_LO[2] + ui[2] * (BOX_HI[2] - BOX_LO[2])
        lp = BOX_LO[3] + ui[3] * (BOX_HI[3] - BOX_LO[3])
        pts.append(snap_design(wn, wp, ln, lp))
    base = snap_design(*BASELINE)
    return [base] + [q for q in dict.fromkeys(pts) if q != base]


def print_row(row):
    for k in FIELDS + ["error"]:
        if k in row and row[k] not in (None, ""):
            v = row[k]
            print(f"  {k:20s} {v:.6g}" if isinstance(v, float) else f"  {k:20s} {v}")


def point(wn, wp, ln, lp, corner, temp, vdd, fanout, load_cap):
    print(f"Point: Wn={wn:g} Wp={wp:g} Ln={ln:g} Lp={lp:g} {corner}@{temp:g}C {vdd:g}V FO{fanout}")
    row = evaluate(wn, wp, ln, lp, corner, temp, vdd, fanout, load_cap, run_id="point", keep=True)
    print_row(row)
    print(f"\nRun directory kept at: {os.path.join(RUNS_DIR, 'point')}")


def check(corner, temp, vdd, fanout, load_cap):
    _, _, block = load_subckt(CELL_NETLIST)
    wn, wp, L = read_geometry(block)
    print(f"Original netlist: Wn={wn:g} um  Wp={wp:g} um  L={L:g} um")
    point(wn, wp, L, L, corner, temp, vdd, fanout, load_cap)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["check", "point", "sweep", "pvt", "mc"], default="check")
    ap.add_argument("--conds", nargs="+", default=["tt@27"],
                    help="corner@temp, corner@temp@vdd, critical, full15")
    ap.add_argument("--vdds", nargs="+", type=float, default=[VDD_NOM],
                    help="supply voltages applied to conditions without an explicit vdd")
    ap.add_argument("--select", choices=["all", "spread"], default="all")
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--have", nargs="*", default=[])
    ap.add_argument("--wn", type=float)
    ap.add_argument("--wp", type=float)
    ap.add_argument("--fanout", type=int, default=FANOUT)
    ap.add_argument("--load", type=float, default=0.0, help="extra lumped output capacitance in F")
    ap.add_argument("--ln", type=float, default=L_MIN)
    ap.add_argument("--lp", type=float, default=L_MIN)
    ap.add_argument("--mc-n", type=int, default=100)
    ap.add_argument("--mc-seed", type=int, default=1)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument("--source", default="verify_designs.csv")
    ap.add_argument("--csv", default=None)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    path = os.path.abspath
    conds = parse_conds(a.conds, a.vdds)
    print("Netlist:", CELL_NETLIST)
    print("Models :", MODEL_LIB)
    if a.mode == "check":
        c, t, v = conds[0]
        check(c, t, v, a.fanout, a.load)
    elif a.mode == "point":
        if a.wn is None or a.wp is None:
            ap.error("--mode point needs --wn and --wp")
        c, t, v = conds[0]
        point(a.wn, a.wp, a.ln, a.lp, c, t, v, a.fanout, a.load)
    elif a.mode == "sweep":
        designs = sobol_designs(a.n, a.mc_seed)
        print(f"{len(designs)} Sobol designs (Wn, Wp, Ln, Lp) x {len(conds)} conditions")
        jobs = [tuple(d) + (c, t, v) for d in designs for (c, t, v) in conds]
        run_jobs(jobs, a.fanout, a.load, a.workers, a.resume, path(a.csv or "dataset_sweep.csv"), a.force)
    elif a.mode == "mc":
        designs = read_designs(path(a.source), a.select, a.n)
        mc_run(designs, conds, a.mc_n, a.mc_seed, a.workers, a.resume, path(a.csv or "mc_samples.csv"), a.force)
    else:
        designs = read_designs(path(a.source), a.select, a.n)
        print(f"{len(designs)} designs x {len(conds)} conditions = {len(designs) * len(conds)} simulations")
        jobs = [tuple(d) + (c, t, v) for d in designs for (c, t, v) in conds]
        run_jobs(jobs, a.fanout, a.load, a.workers, a.resume, path(a.csv or "dataset_pvt.csv"), a.force,
                 [path(h) for h in a.have])


if __name__ == "__main__":
    main()
