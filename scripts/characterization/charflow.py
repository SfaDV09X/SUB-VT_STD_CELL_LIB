#!/usr/bin/env python3
import argparse, math, os, re, shutil, subprocess, sys, time
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from liberty.parser import parse_liberty
from libtools import cell_blocks

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply as AP

SEQ = {"dffx4": "dff", "dlx4": "latch"}
ORDER = ["inv1x4", "nand2x4", "nor2x4", "and2x4", "or2x4", "xor2x4", "xnor2x4", "aoi3x4", "oai3x4",
         "maoi4x4", "moai4x4", "dlx4", "dffx4"]
GRID = np.array([0.25, 0.5, 1, 2, 4])
ALL_CORNERS = [(p, t) for p in ("tt", "ss", "ff", "sf", "fs") for t in (0, 27, 85)]


def log(s):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), s), flush=True)


def tsv(path):
    rows = {}
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        c = line.rstrip("\n").split("\t")
        rows[c[0]] = (c[1].split(","), c[2], c[3])
    return rows


def area(lef):
    m = re.search(r"SIZE\s+([\d.]+)\s+BY\s+([\d.]+)", open(lef).read())
    return float(m.group(1)) * float(m.group(2))


def template(path, libname, temp, cell, row, ar):
    ins, out, fn = row
    pins = "\n".join("    pin (%s) { direction : input; }" % i for i in ins)
    open(path, "w").write(AP.HEAD % dict(lib=libname, temp=temp, oc=libname.replace("subvt_sky130_", ""), templ="") +
                          "  cell (%s) {\n    area : %.4f;\n    pg_pin (VDD) { pg_type : primary_power; voltage_name : VDD; }\n"
                          "    pg_pin (GND) { pg_type : primary_ground; voltage_name : GND; }\n%s\n"
                          "    pin (%s) { direction : output; function : \"%s\"; }\n  }\n}\n" % (cell, ar, pins, out, fn))


def lctime(A, tmpl, cell, net, tempf, out, loads, ramps, step, wd, nobreak=False):
    if os.path.isdir(wd):
        shutil.rmtree(wd)
    os.makedirs(wd)
    pre = [sys.executable, os.path.join(HERE, "lct.py"), "%g" % A.npts] if A.npts != 1e5 else ["lctime"]
    cmd = pre + ["--simulator", "ngspice-interactive", "-l", tmpl, "--cell", cell, "--spice", net, "-L", "%s %s" % (A.models, A.proc), "-I", tempf,
           "-o", out, "--output-loads", ", ".join("%.6g" % x for x in loads),
           "--slew-times", ", ".join("%.6g" % x for x in ramps), "--time-step", "%.0e" % step,
           "--workingdir", wd, "-j", str(A.jobs)]
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, LCT_NOBREAK="1" if nobreak else "0"))
    open(out + ".log", "w").write(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    return r.returncode == 0 and os.path.isfile(out)


def rows(x):
    return np.array([[float(v) for v in str(r).strip().strip('"').split(",")] for r in x])


def tables(libfile, cell):
    lib = parse_liberty(open(libfile).read())
    c = next(c for c in lib.get_groups("cell") if str(c.args[0]) == cell)
    pins = list(c.get_groups("pin"))
    caps = [float(p["capacitance"]) for p in pins if str(p["direction"]) == "input"]
    out = next(p for p in pins if str(p["direction"]) == "output")
    tr, dl = [], []
    for t in out.get_groups("timing"):
        for n, acc in (("rise_transition", tr), ("fall_transition", tr), ("cell_rise", dl), ("cell_fall", dl)):
            for g in t.get_groups(n):
                acc.append((rows(g["index_1"])[0], rows(g["index_2"])[0], rows(g["values"])))
    return caps, tr, dl


def interp(tab, c, r):
    i1, i2, v = tab
    a = np.array([np.interp(r, i2, row) if i2[0] <= r <= i2[-1] else
                  (row[0] + (row[1] - row[0]) * (r - i2[0]) / (i2[1] - i2[0]) if r < i2[0] else
                   row[-2] + (row[-1] - row[-2]) * (r - i2[-2]) / (i2[-1] - i2[-2])) for row in v])
    return float(a[0] + (a[-1] - a[0]) * (c - i1[0]) / (i1[-1] - i1[0]))


def step_for(window, npts):
    need = 3 * window * 1e-9 / npts
    e = 10 ** math.floor(math.log10(need))
    return next(m * e for m in (1, 2, 5, 10) if m * e >= need)


def comb_cell(A, cell, row, cw, tempf, libname):
    out = os.path.join(cw, "raw", cell + ".lib")
    if os.path.isfile(out):
        log("  %s: raw lib present, skipped" % cell)
        return
    net = A.netfmt % dict(CELL=cell.upper(), cell=cell)
    tmpl = os.path.join(cw, "tmpl_%s.lib" % cell)
    template(tmpl, libname, A.temp, cell, row, area(A.leffmt % dict(CELL=cell.upper(), cell=cell)))
    probe = os.path.join(cw, "probe", cell + ".lib")
    os.makedirs(os.path.dirname(probe), exist_ok=True)
    step = step_for(12000.0, A.npts)
    for _ in range(4):
        if lctime(A, tmpl, cell, net, tempf, probe, [0.002, 0.02], [10, 100, 1000], step, os.path.join(cw, "wd_" + cell)):
            break
        step *= 5
    else:
        sys.exit("probe failed for %s, see %s.log" % (cell, probe))
    caps, tr, dl = tables(probe, cell)
    c4 = 4.0 * float(np.mean(caps))
    r = 100.0
    for _ in range(300):
        rn = float(np.mean([interp(t, c4, r) for t in tr])) / 0.4
        rn = max(rn, 0.1)
        if abs(rn - r) < 1e-6 * r:
            break
        r = rn
    loads, ramps = c4 * GRID, r * GRID
    window = ramps[-1] + max(interp(t, loads[-1], ramps[-1]) for t in dl) + max(interp(t, loads[-1], ramps[-1]) for t in tr) / 0.4
    step = step_for(window, A.npts)
    open(os.path.join(cw, "grids.txt"), "a").write(
        "%s C_FO4 %.6g pF ramp* %.6g ns slew* %.6g ns step %.0e loads %s ramps %s\n" %
        (cell, c4, r, 0.4 * r, step, ", ".join("%.6g" % x for x in loads), ", ".join("%.6g" % x for x in ramps)))
    log("  %s: C_FO4 %.4g fF, FO4 slew %.4g ns, step %.0e" % (cell, c4 * 1e3, 0.4 * r, step))
    tmpout = out + ".tmp"
    for k in range(4):
        if lctime(A, tmpl, cell, net, tempf, tmpout, loads, ramps, step, os.path.join(cw, "wd_" + cell), nobreak=k > 0 and A.npts != 1e5):
            break
        if k > 0:
            step *= 2
    else:
        sys.exit("lctime failed for %s, see %s.log" % (cell, tmpout))
    os.replace(tmpout, out)
    os.replace(tmpout + ".log", out + ".log")
    shutil.rmtree(os.path.join(cw, "wd_" + cell), ignore_errors=True)


def seq_cell(A, cell, cw, libname):
    out = os.path.join(cw, "raw", cell + ".lib")
    if os.path.isfile(out):
        log("  %s: raw lib present, skipped" % cell)
        return
    wd = os.path.join(cw, "wd_" + cell)
    os.makedirs(wd, exist_ok=True)
    cmd = [sys.executable, os.path.join(HERE, "seqchar.py"), "--kind", SEQ[cell], "--cell", cell,
           "--net", A.netfmt % dict(CELL=cell.upper(), cell=cell), "--lef", A.leffmt % dict(CELL=cell.upper(), cell=cell),
           "--models", A.models, "--corner", A.proc, "--temp", str(A.temp), "--libname", libname,
           "--out", out + ".tmp", "--jobs", str(A.jobs), "--workdir", wd]
    with open(out + ".log", "w") as f:
        r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    if r.returncode != 0 or not os.path.isfile(out + ".tmp"):
        sys.exit("seqchar failed for %s, see %s.log" % (cell, out))
    os.replace(out + ".tmp", out)
    shutil.rmtree(wd, ignore_errors=True)
    for l in open(out + ".log"):
        if "C_FO4" in l or "grid" in l:
            open(os.path.join(cw, "grids.txt"), "a").write("%s %s" % (cell, l))


def models(src, proc, dst):
    txt = open(src).read()
    m = re.search(r"(?ms)^\.lib\s+%s\s*$(.*?)^\.endl" % re.escape(proc), txt)
    if not m:
        sys.exit("no .lib %s section in %s" % (proc, src))
    base = os.path.dirname(os.path.abspath(src))
    keep = []
    for l in m.group(1).splitlines():
        l = l.strip()
        if l.lower().startswith(".param"):
            keep.append(l)
        else:
            mm = re.match(r"(?i)\.include\s+\"?(continuous/[^\"\s]+)\"?", l)
            if mm:
                keep.append('.include "%s"' % os.path.join(base, mm.group(1)))
    open(dst, "w").write(".lib %s\n%s\n.endl %s\n" % (proc, "\n".join(keep), proc))


def corner(A, proc, temp, cells, rowsd):
    tag = "%s_%dc" % (proc, temp)
    libname = "subvt_sky130_%s_0p40v_%dc" % (proc, temp)
    cw = os.path.join(A.work, tag)
    os.makedirs(os.path.join(cw, "raw"), exist_ok=True)
    A = argparse.Namespace(**vars(A))
    A.proc, A.temp = proc, temp
    A.models = os.path.join(cw, "models.lib")
    models(A.full_models, proc, A.models)
    final = os.path.join(A.libdir, tag, libname + ".lib")
    if os.path.isfile(final) and not A.force:
        log("%s: library present, skipped" % tag)
        return
    log("corner %s" % tag)
    tempf = os.path.join(cw, "temp.spice")
    open(tempf, "w").write(".option TEMP=%d\n" % temp)
    comb = [c for c in cells if c not in SEQ]
    with ThreadPoolExecutor(max(1, min(A.jobs, len(comb)))) as pool:
        futs = {pool.submit(comb_cell, A, c, rowsd[c], cw, tempf, libname): c for c in comb}
        for f in as_completed(futs):
            f.result()
            log("  %s done" % futs[f])
    for c in cells:
        if c in SEQ:
            seq_cell(A, c, cw, libname)
            log("  %s done" % c)
    blocks = []
    for c in cells:
        t = open(os.path.join(cw, "raw", c + ".lib")).read()
        s, e = cell_blocks(t)[c]
        blocks.append(t[s:e])
    raw_all = os.path.join(cw, "raw_all.lib")
    open(raw_all, "w").write(AP.wrap(libname, temp, tag, blocks))
    meas = os.path.join(cw, "meas")
    if not os.path.isfile(os.path.join(meas, "done")):
        log("  power and leakage")
        r = subprocess.run([sys.executable, os.path.join(HERE, "measure.py"), "--lib", raw_all, "--netfmt", A.netfmt,
                            "--out", meas, "--models", A.models, "--corner", proc, "--temp", str(temp),
                            "--jobs", str(A.jobs), "--cells", ",".join(cells)])
        if r.returncode != 0:
            sys.exit("power measurement reported problems for %s, see %s/measure.log" % (tag, meas))
        open(os.path.join(meas, "done"), "w").write("ok\n")
    cellfmt = os.path.join(A.cells_dir, "%(CELL)s", "characterization", "%(cell)s_" + "%s_0p40v_%dc.lib" % (proc, temp))
    r = subprocess.run([sys.executable, os.path.join(HERE, "apply.py"), "--raw", raw_all, "--meas", meas,
                        "--libname", libname, "--temp", str(temp), "--cellfmt", cellfmt, "--libout", final])
    if r.returncode != 0:
        sys.exit("library assembly failed for %s" % tag)
    log("%s finished" % tag)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cells-dir", required=True)
    p.add_argument("--netfmt", default=None)
    p.add_argument("--leffmt", default=None)
    p.add_argument("--models", required=True)
    p.add_argument("--work", required=True)
    p.add_argument("--libdir", required=True)
    p.add_argument("--corners", default="all")
    p.add_argument("--cells", default="all")
    p.add_argument("--jobs", type=int, default=os.cpu_count())
    p.add_argument("--force", action="store_true")
    A = p.parse_args()
    A.cells_dir = os.path.abspath(A.cells_dir)
    A.full_models = os.path.abspath(A.models)
    A.work = os.path.abspath(A.work)
    A.libdir = os.path.abspath(A.libdir)
    A.netfmt = A.netfmt or os.path.join(A.cells_dir, "%(CELL)s", "verification", "pex", "%(cell)s_pex.spice")
    A.leffmt = A.leffmt or os.path.join(A.cells_dir, "%(CELL)s", "layout", "%(cell)s.lef")
    rowsd = tsv(os.path.join(HERE, "cells.tsv"))
    chk = subprocess.run([sys.executable, "-c", "import lctime.characterization.timing_combinatorial as t, lctime.characterization.input_capacitance as i;"
                          "import sys;sys.exit(0 if 'cfg.time_step * 1e5' in open(t.__file__).read() and 'cfg.time_step * 1e6' in open(i.__file__).read() else 1)"])
    A.npts = 2e4 if chk.returncode == 0 else 1e5
    log("lctime points per transient: %g" % A.npts)
    cells = ORDER if A.cells == "all" else [c.strip().lower() for c in A.cells.split(",")]
    for c in cells:
        for f in (A.netfmt, A.leffmt):
            if not os.path.isfile(f % dict(CELL=c.upper(), cell=c)):
                sys.exit("missing " + f % dict(CELL=c.upper(), cell=c))
    if A.corners == "all":
        cl = ALL_CORNERS
    else:
        cl = [(x.split("_")[0], int(x.split("_")[1].rstrip("c"))) for x in A.corners.split(",")]
    failed = []
    for proc, temp in cl:
        try:
            corner(A, proc, temp, cells, rowsd)
        except SystemExit as e:
            log("corner %s_%dc FAILED: %s" % (proc, temp, e))
            failed.append("%s_%dc" % (proc, temp))
    if failed:
        log("failed corners: %s" % ", ".join(failed))
        sys.exit(1)
    log("all requested corners finished")


if __name__ == "__main__":
    main()
