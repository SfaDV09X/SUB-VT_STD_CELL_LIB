#!/usr/bin/env python3
# Assemble the final Liberty files of one corner: take the raw lctime/seqchar timing, replace
# the internal power with the values from measure.py (power.csv, seq_power.csv), add leakage
# per state and max_capacitance, then write one .lib per cell and the merged corner library.
# Called by charflow.py.

import argparse, csv, difflib, os, re, sys
from collections import defaultdict
import numpy as np
from libtools import cell_blocks, cell_info, blocks, get_index, floats

# SCALE: lctime's power tables are indexed by the full input ramp; times 0.4 gives the
# 30-70 % transition used everywhere else. NBASE: events after this index come from the
# extended stimulus. W_DEQ: weight of D=Q vs D!=Q clock-fall events in the DFF CLK pin energy.
SCALE = 0.4
SEQ = {"dffx4", "dlx4"}
NBASE = 18
W_DEQ = 0.5


def fmt_list(v, f):
    return ", ".join(f % x for x in v)


# Liberty 2-D table text (index_1 = load, index_2 = slew).
def table_text(name, tmpl, idx1, idx2, vals, ind=8):
    p = lambda n: " " * n
    s = "%s%s (%s) {\n" % (p(ind), name, tmpl)
    s += "%sindex_1 ( \\\n%s\"%s\" \\\n%s);\n" % (p(ind + 2), p(ind + 4), fmt_list(idx1, "%.6f"), p(ind + 2))
    s += "%sindex_2 ( \\\n%s\"%s\" \\\n%s);\n" % (p(ind + 2), p(ind + 4), fmt_list(idx2, "%.6f"), p(ind + 2))
    rows = ['%s"%s"' % (p(ind + 4), fmt_list(r, "%.6e")) for r in vals]
    s += "%svalues ( \\\n%s \\\n%s);\n" % (p(ind + 2), ", \\\n".join(rows), p(ind + 2))
    return s + "%s}\n" % p(ind)


def scale_index2(text):
    def rep(m):
        v = [x * SCALE for x in floats(m.group(2))]
        return m.group(1) + fmt_list(v, "%.6f") + m.group(3)
    return re.sub(r"(index_2 \(\s*\\\n\s*\")([^\"]*)(\")", rep, text)





def table_text_1d(name, tmpl, idx, vals, ind=8):
    p = lambda n: " " * n
    s = "%s%s (%s) {\n" % (p(ind), name, tmpl)
    s += "%sindex_1 ( \\\n%s\"%s\" \\\n%s);\n" % (p(ind + 2), p(ind + 4), fmt_list(idx, "%.6f"), p(ind + 2))
    s += "%svalues ( \\\n%s\"%s\" \\\n%s);\n" % (p(ind + 2), p(ind + 4), fmt_list(vals, "%.6e"), p(ind + 2))
    return s + "%s}\n" % p(ind)


# internal_power groups for one pin of a latch/flip-flop: CLK and D pin energy (1-D in slew,
# D split by clock level) or output energy related to CLK/D (load x slew).
def seq_groups(sp, pin):
    g = []
    ind = "      "
    if pin in ("CLK", "D"):
        for when, key in ((None, "pin_clk"), ("!CLK", "d_clk0"), ("CLK", "d_clk1")):
            if (pin == "CLK") != (key == "pin_clk") or key not in sp["pin"]:
                continue
            r, f = sp["pin"][key]
            t = ind + "internal_power () {\n"
            if when:
                t += ind + "  when : \"%s\";\n" % when
            t += table_text_1d("rise_power", "energy_template_5", sp["slews"], r)
            t += table_text_1d("fall_power", "energy_template_5", sp["slews"], f)
            g.append(t + ind + "}\n")
    else:
        for rel in ("CLK", "D"):
            if (pin, rel) not in sp["arc"]:
                continue
            r, f = sp["arc"][(pin, rel)]
            t = ind + "internal_power () {\n" + ind + "  related_pin : \"%s\";\n" % rel
            t += table_text("rise_power", "energy_template_5x5", sp["loads"], sp["slews"], r)
            t += table_text("fall_power", "energy_template_5x5", sp["loads"], sp["slews"], f)
            g.append(t + ind + "}\n")
    return "".join(g)


def seq_patch(ct, sp):
    for s, e, m in reversed(blocks(ct, r"(?m)^\s*pin \((\w+)\) \{")):
        g = seq_groups(sp, m.group(1))
        if g:
            at = ct.rfind("\n", 0, e - 1) + 1
            ct = ct[:at] + g + ct[at:]
    return ct


# Turn the per-event energies of seq_power.csv into tables. Pin energy = events where the
# output does not switch; output arc energy = events where it does, minus the same event
# with no load (so the pin part is not counted twice).
def seq_tables(rows, cell, info, kind):
    loads, slews = None, None
    for tabs in info["tables"].values():
        loads, slews = tabs[0][0], tabs[0][1]
        break
    R = [r for r in rows if r["cell"] == cell]
    if not R:
        sys.exit("no seq_power rows for %s: rerun  run_patch.sh cell %s" % (cell, cell))
    idx = defaultdict(list)
    for r in R:
        key = (round(float(r["cq_pF"]), 9), round(float(r["cqb_pF"]), 9), int(r["jj"]))
        idx[key].append(dict(n=int(r["n"]), sig=r["sig"], edge=r["edge"], c=int(r["c"]), d=int(r["d"]),
                             qb=int(r["q_before"]), qa=int(r["q_after"]), E=float(r["Eint_fJ"])))
    nj = len(slews)

    def match(x, k, w):
        if k == "nosw":
            return (x["qb"] == x["qa"]) == w
        if k == "deq":
            return (x["d"] == x["qb"]) == w
        return x[k] == w

    def pick(cq, cqb, jj, ext=False, allow_empty=False, **kw):
        v = [x["E"] for x in idx.get((round(cq, 9), round(cqb, 9), jj), [])
             if (x["n"] > NBASE) == ext and all(match(x, k, w) for k, w in kw.items())]
        if not v and not allow_empty:
            sys.exit("%s: no events for config cq=%g cqb=%g jj=%d ext=%s %s" % (cell, cq, cqb, jj, ext, kw))
        return v

    mean = lambda v: float(np.mean(v)) * 1e-3
    out = dict(slews=slews, loads=loads, pin={}, arc={}, stats=[])
    for key, kw in (("pin_clk", dict(sig="CLK", nosw=True)),):
        r = [pick(0, 0, j, edge="rise", **kw) for j in range(nj)]
        f_eq = [pick(0, 0, j, edge="fall", deq=True, **kw) for j in range(nj)]
        f_ne = [pick(0, 0, j, ext=True, allow_empty=True, edge="fall", deq=False, **kw) for j in range(nj)]
        if kind == "dff":
            if not all(f_ne):
                sys.exit("%s: no CLK-fall events with D != Q in seq_power.csv: rerun  run_power.sh cell %s "
                         "with the extended stimulus program" % (cell, cell))
            f_mean = [W_DEQ * float(np.mean(a)) * 1e-3 + (1 - W_DEQ) * float(np.mean(b)) * 1e-3 for a, b in zip(f_eq, f_ne)]
            f_all = [a + b for a, b in zip(f_eq, f_ne)]
        else:
            if any(pick(0, 0, j, allow_empty=True, edge="fall", deq=False, **kw) for j in range(nj)):
                sys.exit("%s: CLK-fall events with D != Q found in a latch; the pin energy needs a state split" % cell)
            f_mean = [mean(a) for a in f_eq]
            f_all = f_eq
        out["pin"][key] = ([mean(v) for v in r], f_mean)
        out["stats"].append(("CLK pin rise", [(min(v) * 1e-3, mean(v), max(v) * 1e-3) for v in r]))
        if kind == "dff":
            out["stats"].append(("CLK fall, D=Q", [(min(v) * 1e-3, mean(v), max(v) * 1e-3) for v in f_eq]))
            out["stats"].append(("CLK fall, D!=Q", [(min(v) * 1e-3, mean(v), max(v) * 1e-3) for v in f_ne]))
        out["stats"].append(("CLK pin fall (table)", [(min(v) * 1e-3, m, max(v) * 1e-3) for v, m in zip(f_all, f_mean)]))
    for key, c in (("d_clk0", 0), ("d_clk1", 1)):
        if key == "d_clk1" and kind == "latch":
            continue
        r = [pick(0, 0, j, sig="D", edge="rise", c=c, nosw=True) for j in range(nj)]
        f = [pick(0, 0, j, sig="D", edge="fall", c=c, nosw=True) for j in range(nj)]
        out["pin"][key] = ([mean(v) for v in r], [mean(v) for v in f])
        out["stats"].append(("D pin rise, CLK=%d" % c, [(min(v) * 1e-3, mean(v), max(v) * 1e-3) for v in r]))
        out["stats"].append(("D pin fall, CLK=%d" % c, [(min(v) * 1e-3, mean(v), max(v) * 1e-3) for v in f]))

    def arc(rel, q_edge, ii, jj, out_pin):
        qb_, qa_ = (0, 1) if q_edge == "rise" else (1, 0)
        sel = dict(sig=rel, qb=qb_, qa=qa_)
        if rel == "CLK":
            sel.update(edge="rise")
        else:
            sel.update(c=1)
        if out_pin == "Q":
            e = mean(pick(loads[ii], 0, jj, **sel))
            if rel == "CLK":
                e -= mean(pick(0, 0, jj, sig="CLK", edge="rise", qb=qb_, qa=qb_))
            return e
        return mean(pick(0, loads[ii], jj, **sel)) - mean(pick(0, 0, jj, **sel))
    rels = ("CLK",) if kind == "dff" else ("CLK", "D")
    for rel in rels:
        for pin in ("Q", "QB"):
            rr, ff = [], []
            for ii in range(len(loads)):
                rr.append([arc(rel, "rise" if pin == "Q" else "fall", ii, jj, pin) for jj in range(nj)])
                ff.append([arc(rel, "fall" if pin == "Q" else "rise", ii, jj, pin) for jj in range(nj)])
            out["arc"][(pin, rel)] = (rr, ff)
    return out


# Put the measured internal power, leakage and max_capacitance into one raw cell block.
def patch_cell(ct, name, power, leak, seqp=None):
    if "leakage_power" in ct or "cell_leakage_power" in ct:
        raise SystemExit("%s already has leakage groups; refusing to double-patch" % name)
    if power is not None:
        ct = scale_index2(ct)
        for s, e, m in reversed(blocks(ct, r"(?m)^\s*internal_power \(\) \{")):
            old = ct[s:e]
            pin = re.search(r"related_pin : \"(\w+)\";", old).group(1)
            idx1, idx2 = get_index(old, 1), get_index(old, 2)
            new = "      internal_power () {\n        related_pin : \"%s\";\n" % pin
            new += table_text("rise_power", "energy_template_5x5", idx1, idx2, power[(pin, "rise")])
            new += table_text("fall_power", "energy_template_5x5", idx1, idx2, power[(pin, "fall")])
            new += "      }\n"
            ct = ct[:s] + new.rstrip("\n") + ct[e:]
    if seqp is not None:
        ct = seq_patch(ct, seqp)
    mean = float(np.mean([w for _, w in leak]))
    ins = "\n    cell_leakage_power : %.6g;" % mean
    for when, w in leak:
        ins += "\n    leakage_power () {\n      when : \"%s\";\n      value : %.6g;\n    }" % (when, w)
    m = re.search(r"\n\s*area : [\d.eE+-]+;", ct)
    ct = ct[:m.end()] + ins + ct[m.end():]
    for s_, e_, m_ in reversed(blocks(ct, r"(?m)^\s*pin \((\w+)\) \{")):
        pt = ct[s_:e_]
        if "direction : output;" not in pt or "max_capacitance" in pt:
            continue
        loads = [x for b in re.findall(r"index_1 \(\s*\\?\s*\"([^\"]*)\"", pt) for x in floats(b)]
        if not loads:
            continue
        k = pt.index("direction : output;") + len("direction : output;")
        pt = pt[:k] + "\n      max_capacitance : %.6f;" % max(loads) + pt[k:]
        ct = ct[:s_] + pt + ct[e_:]
    return ct


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


# Library header: units, 50 % delay thresholds, 30-70 % slew thresholds, 0.40 V.
HEAD = """library (%(lib)s) {
  delay_model : table_lookup;
  time_unit : "1ns";
  voltage_unit : "1V";
  current_unit : "1uA";
  pulling_resistance_unit : "1kohm";
  leakage_power_unit : "1nW";
  capacitive_load_unit (1, pf);
  nom_process : 1;
  nom_temperature : %(temp)g;
  nom_voltage : 0.4;
  default_cell_leakage_power : 0;
  default_fanout_load : 1;
  default_inout_pin_cap : 0;
  default_input_pin_cap : 0;
  default_output_pin_cap : 0;
  default_leakage_power_density : 0;
  input_threshold_pct_rise : 50;
  input_threshold_pct_fall : 50;
  output_threshold_pct_rise : 50;
  output_threshold_pct_fall : 50;
  slew_lower_threshold_pct_rise : 30;
  slew_upper_threshold_pct_rise : 70;
  slew_lower_threshold_pct_fall : 30;
  slew_upper_threshold_pct_fall : 70;
  slew_derate_from_library : 1.0;
  voltage_map (VDD, 0.4);
  voltage_map (GND, 0);
  operating_conditions (%(oc)s) {
    process : 1;
    temperature : %(temp)g;
    voltage : 0.4;
  }
  default_operating_conditions : %(oc)s;
%(templ)s"""


# Table templates; the index values here are placeholders, every table carries its own.
def templates():
    d = '"1000.000000, 1001.000000, 1002.000000, 1003.000000, 1004.000000"'
    two = lambda kind, name, v1, v2: ("  %s (%s) {\n    variable_1 : %s;\n    variable_2 : %s;\n"
                                       "    index_1 ( \\\n      %s \\\n    );\n    index_2 ( \\\n      %s \\\n    );\n  }\n"
                                       % (kind, name, v1, v2, d, d))
    t = two("lu_table_template", "delay_template_5x5", "total_output_net_capacitance", "input_net_transition")
    t += two("lu_table_template", "constraint_template_5x5", "constrained_pin_transition", "related_pin_transition")
    t += two("power_lut_template", "energy_template_5x5", "total_output_net_capacitance", "input_transition_time")
    t += "  power_lut_template (energy_template_5) {\n    variable_1 : input_transition_time;\n    index_1 ( \\\n      %s \\\n    );\n  }\n" % d
    return t


def wrap(libname, temp, oc, blocks_):
    return HEAD % dict(lib=libname, temp=temp, oc=oc, templ=templates()) + "".join("  " + b.lstrip() + "\n" for b in blocks_) + "}\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--meas", required=True)
    ap.add_argument("--libname", required=True)
    ap.add_argument("--temp", type=float, required=True)
    ap.add_argument("--cellfmt", required=True)
    ap.add_argument("--libout", required=True)
    A = ap.parse_args()
    d = A.meas
    prow = load_csv(os.path.join(d, "power.csv"))
    lrow = load_csv(os.path.join(d, "leakage.csv"))
    srow = load_csv(os.path.join(d, "seq_power.csv")) if os.path.isfile(os.path.join(d, "seq_power.csv")) else []
    bad = [r for r in srow if r["error"]] + [r for r in prow if r["error"]] + [r for r in lrow if r["error"] and "unreachable" not in r["error"]]
    if bad:
        sys.exit("measurement errors present, not patching:\n" + "\n".join(str(b) for b in bad[:10]))
    # Average the energy of repeated events per (cell, pin, output edge, load, slew).
    acc = defaultdict(list)
    for r in prow:
        acc[(r["cell"], r["pin"], r["out_edge"], int(r["i"]), int(r["j"]))].append(float(r["Eint_fJ"]) * 1e-3)
    leak = defaultdict(list)
    for r in lrow:
        if not r["error"]:
            leak[r["cell"]].append((r["when"], float(r["P_nW"])))
    oc = A.libname.replace("subvt_sky130_", "")
    raw = open(A.raw).read()
    cb = cell_blocks(raw)
    out = []
    for name in sorted(cb, key=lambda n: cb[n][0]):
        s, e = cb[name]
        ct = raw[s:e]
        if name not in leak:
            sys.exit("no leakage rows for " + name)
        power, seqp = None, None
        if name in SEQ:
            seqp = seq_tables(srow, name, cell_info(ct), "dff" if name == "dffx4" else "latch")
        else:
            info = cell_info(ct)
            power = {}
            n1 = len(next(iter(info["tables"].values()))[0][0])
            n2 = len(next(iter(info["tables"].values()))[0][1])
            for pin in info["inputs"]:
                for oe in ("rise", "fall"):
                    tab = [[None] * n2 for _ in range(n1)]
                    for i in range(n1):
                        for j in range(n2):
                            v = acc.get((name, pin, oe, i, j))
                            if not v:
                                sys.exit("missing power data %s %s %s %d %d" % (name, pin, oe, i, j))
                            tab[i][j] = float(np.mean(v))
                    power[(pin, oe)] = tab
        new = patch_cell(ct, name, power, leak[name], seqp)
        out.append(new)
        p = A.cellfmt % dict(CELL=name.upper(), cell=name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(wrap(A.libname, A.temp, oc, [new]))
        print("%-8s %s  leakage %.4g nW" % (name, "combinational" if power else "sequential", float(np.mean([w for _, w in leak[name]]))))
    os.makedirs(os.path.dirname(os.path.abspath(A.libout)), exist_ok=True)
    open(A.libout, "w").write(wrap(A.libname, A.temp, oc, out))
    print("wrote " + A.libout)


if __name__ == "__main__":
    main()
