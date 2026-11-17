#!/usr/bin/env python3
import itertools, os, sys
from libtools import blocks, cell_blocks, get_index

CELLS = ["inv1x4", "nand2x4", "nor2x4", "and2x4", "or2x4", "xor2x4", "xnor2x4", "aoi3x4", "oai3x4",
         "maoi4x4", "moai4x4", "dlx4", "dffx4"]


def main(cells_dir):
    for c in CELLS:
        rows = []
        for p, t in itertools.product(["tt", "ss", "ff", "sf", "fs"], [0, 27, 85]):
            f = os.path.join(cells_dir, c.upper(), "characterization", "%s_%s_0p40v_%dc.lib" % (c, p, t))
            if not os.path.isfile(f):
                continue
            txt = open(f).read()
            s, e = cell_blocks(txt)[c]
            ct = txt[s:e]
            b = [ct[x:y] for x, y, m in blocks(ct, r"(?m)^\s*cell_rise \(\w+\) \{")][0]
            L, S = get_index(b, 1), get_index(b, 2)
            rows.append("%s_%dc  C_FO4 %.6g pF  slew* %.6g ns  loads(pF) %s  slews(ns) %s" %
                        (p, t, L[2], S[2], ", ".join("%.6g" % x for x in L), ", ".join("%.6g" % x for x in S)))
        if rows:
            open(os.path.join(cells_dir, c.upper(), "characterization", c + ".grids"), "w").write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
