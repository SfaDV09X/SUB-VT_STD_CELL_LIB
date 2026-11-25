#!/usr/bin/env python3
# HTML datasheets from the corner libraries: datasheets/index.html (cell list + frame) and one
# page per cell with truth table, area, pin caps, leakage, timing and power, and a drop-down to
# switch between the 15 corners. Usage: python3 datasheet.py --libdir lib --out datasheets

import argparse, glob, html, itertools, os, re, sys
import numpy as np
from libtools import blocks, cell_blocks, floats, get_index, get_values, eval_function

ORDER = ["inv1x4", "nand2x4", "nor2x4", "and2x4", "or2x4", "xor2x4", "xnor2x4", "aoi3x4", "oai3x4",
         "maoi4x4", "moai4x4", "dlx4", "dffx4"]
PROCS = ["tt", "ss", "ff", "sf", "fs"]
TEMPS = [0, 27, 85]
LIBNAME = "SUBVT_SKY130"
F = "%.5f"


def pins(ct):
    return {m.group(1): ct[s:e] for s, e, m in blocks(ct, r"(?m)^\s*pin \((\w+)\) \{")}


def attr(t, k):
    m = re.search(r"\b%s : \"?([^\";]*)\"?;" % k, t)
    return m.group(1) if m else None


def tables(t, name):
    return [(get_index(t[s:e], 1), get_index(t[s:e], 2) if "index_2" in t[s:e] else None, get_values(t[s:e]))
            for s, e, m in blocks(t, r"(?m)^\s*%s \(\w+\) \{" % name)]


# First, middle and last entry of a table (min / FO4 / max corner of the grid).
def fml(tab):
    i1, i2, v = tab
    v = np.array(v)
    if v.ndim == 1 or v.shape[0] == 1 and i2 is None:
        v = v.reshape(-1)
        return [v[0], v[len(v) // 2], v[-1]]
    n = min(v.shape)
    return [v[0][0], v[n // 2][n // 2], v[n - 1][n - 1]]


# Area, pins, leakage per state and whether the cell is a flip-flop or latch.
def parse(ct):
    P = pins(ct)
    info = dict(area=float(attr(ct, "area")), pins=P, inputs=[], outputs=[], leak=[], ff=None, latch=None)
    for p, t in P.items():
        (info["inputs"] if attr(t, "direction") == "input" else info["outputs"]).append(p)
    for s, e, m in blocks(ct, r"(?m)^\s*leakage_power \(\) \{"):
        info["leak"].append(float(attr(ct[s:e], "value")))
    if re.search(r"(?m)^\s*ff \(", ct):
        info["ff"] = True
    if re.search(r"(?m)^\s*latch \(", ct):
        info["latch"] = True
    return info


# All corner libraries found, as {(process, temp): {cell: cell text}}.
def load_libs(libdir):
    libs = {}
    for p, t in itertools.product(PROCS, TEMPS):
        f = os.path.join(libdir, "%s_%dc" % (p, t), "subvt_sky130_%s_0p40v_%dc.lib" % (p, t))
        if os.path.isfile(f):
            txt = open(f).read()
            libs[(p, t)] = {n: txt[s:e] for n, (s, e) in cell_blocks(txt).items()}
    return libs


def th(x, extra=""):
    return "<TH%s>%s</TH>" % (extra, x)


def td(x):
    return "<TD align=center>%s</TD>" % (F % x if isinstance(x, (float, np.floating)) else x)


def section(title):
    return "<BR>\n<FONT SIZE=+2><B>%s</B></FONT>\n<BR>\n" % title


def sub(title):
    return "<BR>\n<FONT><B>%s</B></FONT>\n" % title


def head3(cols, first, label):
    return ("<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=4 WIDTH=100%%>\n<TR valign=middle>%s<TH colspan=3>%s</TH></TR>\n"
            "<TR><TH>%s</TH><TH>%s</TH><TH>%s</TH></TR>\n" % ("".join(th(c, " rowspan=2") for c in cols), label, *first))


def truth_comb(name, info, fn):
    ins, out = info["inputs"], info["outputs"][0]
    h = ("<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=4>\n<TR valign=middle><TH colspan=%d>INPUT</TH><TH colspan=1>OUTPUT</TH></TR>\n"
         "<TR>%s%s</TR>\n" % (len(ins), "".join(th(i) for i in ins), th(out)))
    for bits in itertools.product((0, 1), repeat=len(ins)):
        y = int(eval_function(fn, dict(zip(ins, bits))))
        h += "<TR>%s%s</TR>\n" % ("".join(th("<font size=2>%d</font>" % b) for b in bits), th("<font size=2>%d</font>" % y))
    return h + "</TABLE>\n"


def truth_seq(kind):
    if kind == "dff":
        rows = [("R", "0", "0", "1"), ("R", "1", "1", "0"), ("0", "x", "Q", "QB"), ("1", "x", "Q", "QB"), ("F", "x", "Q", "QB")]
    else:
        rows = [("1", "0", "0", "1"), ("1", "1", "1", "0"), ("0", "x", "Q", "QB")]
    h = ("<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=4>\n<TR valign=middle><TH colspan=2>INPUT</TH><TH colspan=2>OUTPUT</TH></TR>\n"
         "<TR><TH>CLK</TH><TH>D</TH><TH>Q</TH><TH>QB</TH></TR>\n")
    for r in rows:
        h += "<TR>%s</TR>\n" % "".join(th("<font size=2>%s</font>" % x) for x in r)
    return h + "</TABLE>\n"


# Arc label like RF (input rise -> output fall) from the timing sense.
def edge_dir(sense, out_rise):
    o = "R" if out_rise else "F"
    if sense == "positive_unate":
        return o + o
    if sense == "negative_unate":
        return ("F" if out_rise else "R") + o
    return "X" + o


# Datasheet tables for one cell at one corner.
def corner_body(name, ct, kind):
    info = parse(ct)
    U = name.upper()
    h = ""
    h += section("Footprint")
    h += "<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=4 WIDTH=60%%>\n<TR><TH>Cell Name</TH><TH>Area (um<sup>2</sup>)</TH></TR>\n<TR><TH>%s</TH>%s</TR>\n</TABLE>\n" % (U, td(info["area"]))
    h += section("Pin Capacitance Information")
    ins, outs = info["inputs"], info["outputs"]
    h += ("<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=4 WIDTH=100%%>\n<TR valign=middle><TH rowspan=2>Cell Name</TH>"
          "<TH colspan=%d>Pin Cap(pf)</TH><TH colspan=%d>Max Cap(pf)</TH></TR>\n<TR>%s%s</TR>\n<TR><TH>%s</TH>%s%s</TR>\n</TABLE>\n" %
          (len(ins), len(outs), "".join(th(i) for i in ins), "".join(th(o) for o in outs), U,
           "".join(td(float(attr(info["pins"][i], "capacitance"))) for i in ins),
           "".join(td(float(attr(info["pins"][o], "max_capacitance") or "nan")) for o in outs)))
    lk = info["leak"]
    h += section("Leakage Information")
    h += ("<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=4 WIDTH=100%%>\n<TR valign=middle><TH rowspan=2>Cell Name</TH><TH colspan=3>Leakage(nW)</TH></TR>\n"
          "<TR><TH>Min.</TH><TH>Avg</TH><TH>Max.</TH></TR>\n<TR><TH>%s</TH>%s%s%s</TR>\n</TABLE>\n" %
          (U, td(min(lk)), td(float(np.mean(lk))), td(max(lk))))
    h += "<!--NewPage-->\n" + section("Delay Information")
    grid_note = None
    for o in outs:
        arcs = {True: [], False: []}
        for s, e, m in blocks(info["pins"][o], r"(?m)^\s*timing \(\) \{"):
            t = info["pins"][o][s:e]
            rel, sense, ttype = attr(t, "related_pin"), attr(t, "timing_sense"), attr(t, "timing_type") or "combinational"
            for rise, nm in ((True, "cell_rise"), (False, "cell_fall")):
                for tab in tables(t, nm):
                    if grid_note is None:
                        grid_note = tab
                    d = ("R" if ttype in ("rising_edge",) else "F" if ttype == "falling_edge" else None)
                    dd = (d + ("R" if rise else "F")) if d else edge_dir(sense, rise)
                    arcs[rise].append(("%s->%s (%s)" % (rel, o, dd), fml(tab)))
        for rise in (True, False):
            if not arcs[rise]:
                continue
            h += sub("Delay(ns) to %s %s :" % (o, "rising" if rise else "falling"))
            h += head3(["Cell Name", "Timing Arc(Dir)"], ["First", "Mid", "Last"], "Delay(ns)")
            for k, (lab, v) in enumerate(arcs[rise]):
                h += "<TR>%s<TH><font>%s</font></TH>%s</TR>\n" % (th(U, " rowspan=%d" % len(arcs[rise])) if k == 0 else "", lab, "".join(td(x) for x in v))
            h += "</TABLE>\n"
    if grid_note:
        i1, i2, _ = grid_note
        n = len(i1) // 2
        h += ("<BR><em>First / Mid / Last = (input slew, output load) = (%s ns, %s pF) / (%s ns, %s pF) / (%s ns, %s pF); "
              "slew 30-70 %%, delay 50-50 %%.</em><BR>\n" % (F % i2[0], F % i1[0], F % i2[n], F % i1[n], F % i2[-1], F % i1[-1]))
    h += "<!--NewPage-->\n" + section("Power Information")
    for o in outs:
        rows = {True: [], False: []}
        for s, e, m in blocks(info["pins"][o], r"(?m)^\s*internal_power \(\) \{"):
            t = info["pins"][o][s:e]
            rel = attr(t, "related_pin") or o
            for rise, nm in ((True, "rise_power"), (False, "fall_power")):
                for tab in tables(t, nm):
                    rows[rise].append((rel, fml(tab)))
        for rise in (True, False):
            if not rows[rise]:
                continue
            h += sub("Internal switching power(pJ) to %s %s :" % (o, "rising" if rise else "falling"))
            h += head3(["Cell Name", "Input"], ["first", "mid", "last"], "Power(pJ)")
            for k, (lab, v) in enumerate(rows[rise]):
                h += "<TR>%s<TH><font>%s</font></TH>%s</TR>\n" % (th(U, " rowspan=%d" % len(rows[rise])) if k == 0 else "", lab, "".join(td(x) for x in v))
            h += "</TABLE>\n"
    for i in ins:
        for rise, nm in ((True, "rise_power"), (False, "fall_power")):
            rows = []
            for s, e, m in blocks(info["pins"][i], r"(?m)^\s*internal_power \(\) \{"):
                t = info["pins"][i][s:e]
                for tab in tables(t, nm):
                    rows.append((attr(t, "when") or "-", fml(tab)))
            if not rows:
                continue
            h += sub("Passive power(pJ) for %s %s%s:" % (i, "rising" if rise else "falling", " (conditional)" if any(r[0] != "-" for r in rows) else ""))
            h += head3(["Cell Name", "When"], ["first", "mid", "last"], "Power(pJ)")
            for k, (lab, v) in enumerate(rows):
                h += "<TR>%s<TH><font>%s</font></TH>%s</TR>\n" % (th(U, " rowspan=%d" % len(rows)) if k == 0 else "", html.escape(lab), "".join(td(x) for x in v))
            h += "</TABLE>\n"
    if kind:
        h += "<!--NewPage-->\n" + section("Constraint Information")
        for i in ins:
            for rise, nm in ((True, "rise_constraint"), (False, "fall_constraint")):
                rows = []
                for s, e, m in blocks(info["pins"][i], r"(?m)^\s*timing \(\) \{"):
                    t = info["pins"][i][s:e]
                    tt = attr(t, "timing_type")
                    chk, edge = tt.split("_")
                    for tab in tables(t, nm):
                        rows.append((chk, "%s (%s)" % (attr(t, "related_pin"), "R" if edge == "rising" else "F"), fml(tab)))
                if not rows:
                    continue
                h += sub("Constraints(ns) for %s %s :" % (i, "rising" if rise else "falling"))
                h += head3(["Cell Name", "Timing Check", "Ref Pin(trans)"], [" first ", " mid ", " last "], "Reference Slew Rate(ns)")
                for k, (c, r, v) in enumerate(rows):
                    h += "<TR>%s<TH><font>%s</font></TH><TH><font>%s</font></TH>%s</TR>\n" % (th(U, " rowspan=%d" % len(rows)) if k == 0 else "", c, r, "".join(td(x) for x in v))
                h += "</TABLE>\n"
    return h


# Full page of one cell; every corner is a hidden DIV and the select box shows one of them.
# The last chosen corner is remembered in the browser.
def page(name, libs, prev, nxt, fns):
    U = name.upper()
    corners = [c for c in itertools.product(PROCS, TEMPS) if c in libs and name in libs[c]]
    if not corners:
        return None
    first = libs[corners[0]][name]
    kind = "dff" if re.search(r"(?m)^\s*ff \(", first) else "latch" if re.search(r"(?m)^\s*latch \(", first) else None
    info = parse(first)
    out = ["<HTML>\n<HEAD><TITLE>%s</TITLE>\n<SCRIPT>\nfunction sel(v){var d=document.getElementsByClassName('corner');"
           "for(var i=0;i<d.length;i++){d[i].style.display=(d[i].id==v)?'block':'none';}"
           "var o=document.getElementById('cs');for(var i=0;i<o.options.length;i++){if(o.options[i].value==v){o.selectedIndex=i;"
           "document.getElementById('hdr').innerHTML=o.options[i].getAttribute('data-h');}}"
           "try{window.localStorage.setItem('subvt_corner',v);}catch(e){}}\n"
           "window.onload=function(){var v=null;try{v=window.localStorage.getItem('subvt_corner');}catch(e){}"
           "if(!v||!document.getElementById(v)){v='%s';}sel(v);};\n</SCRIPT>\n</HEAD>\n"
           "<BODY TEXT=\"#000000\" LINK=\"#0000FF\" VLINK=\"#0000FF\" ALINK=\"#00FFFF\">\n" % (U, "c_%s_%d" % corners[0])]
    out.append("<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=5 WIDTH=100%%>\n<TR align=center><th align=left><H1><font size=+3>%s</font></H1></th>"
               "<th align=right>Corner: <SELECT id=cs onchange=\"sel(this.value)\">%s</SELECT></th></TR>\n"
               "<TR align=center><th align=left></th><th align=right><h5><em><A id=hdr></A></em></h5></th></TR>\n</TABLE>\n<HR>\n" %
               (U, "".join("<OPTION value=\"c_%s_%d\" data-h=\"%s Cell Library: Process %s, Voltage 0.40, Temp %.2f\">%s, %d C</OPTION>" %
                           (p, t, LIBNAME, p, t, p, t) for p, t in corners)))
    out.append("<BR>\n<FONT SIZE=+2><B>Truth Table</B></FONT>\n")
    out.append(truth_seq(kind) if kind else truth_comb(name, info, fns.get(name) or attr(info["pins"][info["outputs"][0]], "function")))
    for p, t in corners:
        out.append("<DIV class=corner id=\"c_%s_%d\" style=\"display:none\">\n%s</DIV>\n" % (p, t, corner_body(name, libs[(p, t)][name], kind)))
    nav = "<BR>\n<DIV class=NOPRINT>\n<HR>\n<TABLE BORDER=0 WIDTH=100%>\n<TR>"
    nav += "<TD ALIGN=LEFT>%s</TD>" % ("<TABLE BORDER=5><TR><TD><em><A hREF=\"%s.html\">Prev (%s)</A></em></TD></TR></TABLE>" % (prev, prev) if prev else "")
    nav += "<TD ALIGN=RIGHT>%s</TD>" % ("<TABLE BORDER=5><TR><TD><em><A hREF=\"%s.html\">Next (%s)</A></em></TD></TR></TABLE>" % (nxt, nxt) if nxt else "")
    out.append(nav + "</TR>\n</TABLE>\n</DIV>\n</BODY>\n</HTML>\n")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--libdir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tsv", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "cells.tsv"))
    A = ap.parse_args()
    libs = load_libs(A.libdir)
    if not libs:
        sys.exit("no corner libraries in " + A.libdir)
    # Functions from cells.tsv, used for the truth tables.
    fns = {}
    for l in open(A.tsv):
        if l.strip() and not l.startswith("#"):
            c = l.rstrip("\n").split("\t")
            fns[c[0]] = c[3]
    present = [n for n in ORDER if any(n in v for v in libs.values())]
    os.makedirs(A.out, exist_ok=True)
    U = [n.upper() for n in present]
    for k, n in enumerate(present):
        h = page(n, libs, U[k - 1] if k else None, U[k + 1] if k + 1 < len(U) else None, fns)
        open(os.path.join(A.out, n.upper() + ".html"), "w").write(h)
    cl = ("<HTML><BODY TEXT=\"#000000\" LINK=\"#0000FF\" VLINK=\"#0000FF\" ALINK=\"#00FFFF\"><CENTER><H1>%s Library</H1></CENTER><HR><BR>\n"
          "<TABLE BORDER=3 CELLSPACING=2 CELLPADDING=5 WIDTH=100%%>\n<TR><TH>Cell Groups</th></TR>\n" % LIBNAME)
    cl += "".join("<TR><TH align=left><a href=\"%s.html\" target=celldata>%s</a></TR>\n" % (u, u) for u in U)
    cl += "</TABLE>\n<BR><em>%d corners: %s</em>\n</BODY></HTML>\n" % (len(libs), ", ".join("%s %dC" % c for c in sorted(libs, key=lambda c: (PROCS.index(c[0]), c[1]))))
    open(os.path.join(A.out, "celllist.html"), "w").write(cl)
    open(os.path.join(A.out, "index.html"), "w").write(
        "<HTML>\n<HEAD>\n<TITLE>%s Library Datasheet</TITLE>\n</HEAD>\n<FRAMESET COLS=\"150,700\">\n"
        "<FRAME NAME=\"celllist\" SRC=\"celllist.html\" SCROLLING=YES>\n<FRAME NAME=\"celldata\" SRC=\"%s.html\" SCROLLING=YES>\n"
        "</FRAMESET>\n</HTML>\n" % (LIBNAME, U[0]))
    print("wrote %d cell pages, %d corners, to %s" % (len(U), len(libs), A.out))


if __name__ == "__main__":
    main()
