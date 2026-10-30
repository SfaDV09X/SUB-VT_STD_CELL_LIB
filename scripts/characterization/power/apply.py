#!/usr/bin/env python3
import argparse, csv, difflib, os, re, sys
from collections import defaultdict
import numpy as np
from libtools import cell_blocks, cell_info, blocks, get_index, floats

SCALE = 0.4
SEQ = {"dffx1", "dlx1"}
LIB = "subvt_sky130_tt_0p40v_27c.lib"
NBASE = 18      # events 1..NBASE form the original stimulus program; later events are extensions
W_DEQ = 0.5     # DFF CLK-fall pin energy = W_DEQ * mean(D==Q events) + (1 - W_DEQ) * mean(D!=Q events)


def fmt_list(v, f):
    return ", ".join(f % x for x in v)


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


TEMPL = """  power_lut_template (energy_template_3x3) {
    variable_1 : total_output_net_capacitance;
    variable_2 : input_net_transition;
    index_1 ( \\
      "1000.000000, 1001.000000, 1002.000000" \\
    );
    index_2 ( \\
      "1000.000000, 1001.000000, 1002.000000" \\
    );
  }
  power_lut_template (energy_template_3) {
    variable_1 : input_net_transition;
    index_1 ( \\
      "1000.000000, 1001.000000, 1002.000000" \\
    );
  }
"""


def table_text_1d(name, tmpl, idx, vals, ind=8):
    p = lambda n: " " * n
    s = "%s%s (%s) {\n" % (p(ind), name, tmpl)
    s += "%sindex_1 ( \\\n%s\"%s\" \\\n%s);\n" % (p(ind + 2), p(ind + 4), fmt_list(idx, "%.6f"), p(ind + 2))
    s += "%svalues ( \\\n%s\"%s\" \\\n%s);\n" % (p(ind + 2), p(ind + 4), fmt_list(vals, "%.6e"), p(ind + 2))
    return s + "%s}\n" % p(ind)


def add_templates(text):
    if "energy_template_3x3" in text:
        return text
    i = re.search(r"(?m)^  cell \(", text).start()
    return text[:i] + TEMPL + text[i:]


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
            t += table_text_1d("rise_power", "energy_template_3", sp["slews"], r)
            t += table_text_1d("fall_power", "energy_template_3", sp["slews"], f)
            g.append(t + ind + "}\n")
    else:
        for rel in ("CLK", "D"):
            if (pin, rel) not in sp["arc"]:
                continue
            r, f = sp["arc"][(pin, rel)]
            t = ind + "internal_power () {\n" + ind + "  related_pin : \"%s\";\n" % rel
            t += table_text("rise_power", "energy_template_3x3", sp["loads"], sp["slews"], r)
            t += table_text("fall_power", "energy_template_3x3", sp["loads"], sp["slews"], f)
            g.append(t + ind + "}\n")
    return "".join(g)


def seq_patch(ct, sp):
    for s, e, m in reversed(blocks(ct, r"(?m)^\s*pin \((\w+)\) \{")):
        g = seq_groups(sp, m.group(1))
        if g:
            at = ct.rfind("\n", 0, e - 1) + 1
            ct = ct[:at] + g + ct[at:]
    return ct


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
        # ext=False: original program only (events 1..NBASE), so every table except the DFF CLK-fall pin energy
        # is computed exactly as before; ext=True: events beyond NBASE only
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
    return ct[:m.end()] + ins + ct[m.end():]


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--meas", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    dirs = [A.meas] if os.path.isfile(os.path.join(A.meas, "power.csv")) else \
        sorted(os.path.join(A.meas, d) for d in os.listdir(A.meas) if os.path.isfile(os.path.join(A.meas, d, "power.csv")))
    if not dirs:
        sys.exit("no power.csv under " + A.meas)
    prow = [r for d in dirs for r in load_csv(os.path.join(d, "power.csv"))]
    lrow = [r for d in dirs for r in load_csv(os.path.join(d, "leakage.csv"))]
    srow = [r for d in dirs if os.path.isfile(os.path.join(d, "seq_power.csv"))
            for r in load_csv(os.path.join(d, "seq_power.csv"))]
    bad = [r for r in srow if r["error"]] + [r for r in prow if r["error"]] + [r for r in lrow if r["error"] and "unreachable" not in r["error"]]
    if bad:
        sys.exit("measurement errors present, not patching:\n" + "\n".join(str(b) for b in bad[:10]))

    acc = defaultdict(list)
    for r in prow:
        acc[(r["cell"], r["pin"], r["out_edge"], int(r["i"]), int(r["j"]))].append(float(r["Eint_fJ"]) * 1e-3)
    leak = defaultdict(list)
    for r in lrow:
        if not r["error"]:
            leak[r["cell"]].append((r["when"], float(r["P_nW"])))

    lib_path = os.path.join(A.repo, "lib", LIB)
    lib = open(lib_path).read()
    cb = cell_blocks(lib)
    out_lib, new_cells = lib, {}
    report, seq_report = [], []
    for name in sorted(cb, key=lambda n: cb[n][0], reverse=True):
        s, e = cb[name]
        ct = lib[s:e]
        per = os.path.join(A.repo, "cells", name.upper(), "characterization", name + ".lib")
        ptxt = open(per).read()
        ps, pe = cell_blocks(ptxt)[name]
        if ptxt[ps:pe] != ct:
            report.append("NOTE %s: per-cell lib block differs from combined lib block (each patched separately)" % name)
        if name not in leak:
            sys.exit("no leakage rows for " + name)
        power = None
        if name not in SEQ:
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
        seqp = None
        if name in SEQ:
            seqp = seq_tables(srow, name, cell_info(ct), "dff" if name == "dffx1" else "latch")
            seq_report.append((name, seqp))
        new_ct = patch_cell(ct, name, power, leak[name], seqp)
        out_lib = out_lib[:s] + new_ct + out_lib[e:]
        new_p = patch_cell(ptxt[ps:pe], name, power, leak[name], seqp)
        head = add_templates(ptxt[:ps] + "  cell (") [:-len("  cell (")] if seqp else ptxt[:ps]
        new_cells[name] = (per, head + new_p + ptxt[pe:])
        if True:
            report.append("%-8s patched (%s)" % (name, "combinational" if power else "sequential: pin and arc power, leakage"))

    os.makedirs(os.path.join(A.out, "lib"), exist_ok=True)
    os.makedirs(os.path.join(A.out, "diffs"), exist_ok=True)
    if seq_report:
        out_lib = add_templates(out_lib)
    open(os.path.join(A.out, "lib", LIB), "w").write(out_lib)

    def write_diff(tag, a, b):
        d = "".join(difflib.unified_diff(a.splitlines(True), b.splitlines(True), "repo/" + tag, "patched/" + tag))
        open(os.path.join(A.out, "diffs", tag.replace("/", "__") + ".diff"), "w").write(d)
        return sum(1 for l in d.splitlines() if l.startswith(("+", "-")) and not l.startswith(("+++", "---")))

    n = write_diff("lib/" + LIB, lib, out_lib)
    report.append("lib/%s: %d changed lines" % (LIB, n))
    for name, (per, txt) in sorted(new_cells.items()):
        rel = os.path.relpath(per, A.repo).replace("\\", "/")
        dst = os.path.join(A.out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w").write(txt)
        report.append("%s: %d changed lines" % (rel, write_diff(rel, open(per).read(), txt)))

    report.append("\nFO1 power at grid point (load idx 1, ramp idx 2), pJ -- library before vs after")
    for name in sorted(cb):
        if name in SEQ:
            continue
        ct = lib[cb[name][0]:cb[name][1]]
        for s, e, m in blocks(ct, r"(?m)^\s*internal_power \(\) \{"):
            pin = re.search(r"related_pin : \"(\w+)\";", ct[s:e]).group(1)
            old = {}
            for nm in ("rise_power", "fall_power"):
                bs = blocks(ct[s:e], r"(?m)^\s*%s \(\w+\) \{" % nm)[0]
                vals = re.findall(r"\"([^\"]*)\"", re.search(r"values \(((?:.|\n)*?)\);", ct[s:e][bs[0]:bs[1]]).group(1))
                old[nm] = floats(vals[1])[2]
            report.append("%-8s %s  before: rise_power(in rise) %.3e  fall_power(in fall) %.3e | after: rise_power(out rise) %.3e  fall_power(out fall) %.3e" %
                          (name, pin, old["rise_power"], old["fall_power"],
                           float(np.mean(acc[(name, pin, "rise", 1, 2)])), float(np.mean(acc[(name, pin, "fall", 1, 2)]))))
    for name, sp in sorted(seq_report):
        report.append("\n%s: pin energies (pJ, numerically; fJ x 1e-3) at the 3 CLK/D slews, mean (min..max over the averaged events)" % name)
        for label, vals in sp["stats"]:
            report.append("  %-22s %s" % (label, "   ".join("%.3e (%.3e..%.3e)" % (m, lo, hi) for lo, m, hi in vals)))
        for (pin, rel), (rr, ff) in sorted(sp["arc"].items()):
            report.append("  %s related %-3s centre point (load idx 1, slew idx 1): rise_power %.3e  fall_power %.3e" %
                          (pin, rel, rr[1][1], ff[1][1]))
    report.append("\nleakage (nW): mean over states")
    for name in sorted(leak):
        report.append("%-8s %.4g  (%d states)" % (name, np.mean([w for _, w in leak[name]]), len(leak[name])))
    txt = "\n".join(report) + "\n"
    open(os.path.join(A.out, "summary.txt"), "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
