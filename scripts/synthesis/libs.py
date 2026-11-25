# The two libraries used in the synthesis benchmarks and how their cells line up:
# for each logic function the cell name, input pin mapping and output pin, plus the
# flip-flop and latch. Also helpers to cut a Liberty file down to some cells and to write
# the Yosys techmap files for inverters and latches.

import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from libtools import blocks

CORNERS = [(p, t) for p in ("tt", "ss", "ff", "sf", "fs") for t in (0, 27, 85)]

# Our X4 library: generic pin names a/b/c/d -> cell pins.
SUBVT = dict(
    name="subvt",
    cells={
        "inv1": ("inv1x4", {"a": "A"}, "Y"),
        "nand2": ("nand2x4", {"a": "A", "b": "B"}, "Y"),
        "nor2": ("nor2x4", {"a": "A", "b": "B"}, "Y"),
        "and2": ("and2x4", {"a": "A", "b": "B"}, "Y"),
        "or2": ("or2x4", {"a": "A", "b": "B"}, "Y"),
        "xor2": ("xor2x4", {"a": "A", "b": "B"}, "Y"),
        "xnor2": ("xnor2x4", {"a": "A", "b": "B"}, "Y"),
        "aoi3": ("aoi3x4", {"a": "A", "b": "B", "c": "C"}, "Y"),
        "oai3": ("oai3x4", {"a": "A", "b": "B", "c": "C"}, "Y"),
        "moai4": ("moai4x4", {"a": "A", "b": "B", "c": "C", "d": "D"}, "Y"),
        "maoi4": ("maoi4x4", {"a": "A", "b": "B", "c": "C", "d": "D"}, "Y"),
    },
    dff=("dffx4", "CLK", "D", "Q", "QB"),
    latch=("dlx4", "CLK", "D", "Q", "QB"),
)

# Closest sky130_fd_sc_hd equivalents (drive strength 1), for the 1.8 V reference.
HD = dict(
    name="hd",
    cells={
        "inv1": ("sky130_fd_sc_hd__inv_1", {"a": "A"}, "Y"),
        "nand2": ("sky130_fd_sc_hd__nand2_1", {"a": "A", "b": "B"}, "Y"),
        "nor2": ("sky130_fd_sc_hd__nor2_1", {"a": "A", "b": "B"}, "Y"),
        "and2": ("sky130_fd_sc_hd__and2_1", {"a": "A", "b": "B"}, "X"),
        "or2": ("sky130_fd_sc_hd__or2_1", {"a": "A", "b": "B"}, "X"),
        "xor2": ("sky130_fd_sc_hd__xor2_1", {"a": "A", "b": "B"}, "X"),
        "xnor2": ("sky130_fd_sc_hd__xnor2_1", {"a": "A", "b": "B"}, "Y"),
        "aoi3": ("sky130_fd_sc_hd__a21oi_1", {"a": "A1", "b": "A2", "c": "B1"}, "Y"),
        "oai3": ("sky130_fd_sc_hd__o21ai_1", {"a": "A1", "b": "A2", "c": "B1"}, "Y"),
        "moai4": ("sky130_fd_sc_hd__a2bb2o_1", {"a": "B1", "b": "B2", "c": "A1_N", "d": "A2_N"}, "X"),
        "maoi4": ("sky130_fd_sc_hd__a2bb2oi_1", {"a": "A1_N", "b": "A2_N", "c": "B1", "d": "B2"}, "Y"),
    },
    dff=("sky130_fd_sc_hd__dfxbp_1", "CLK", "D", "Q", "Q_N"),
    latch=("sky130_fd_sc_hd__dlxbp_1", "GATE", "D", "Q", "Q_N"),
)

LIBS = {"subvt": SUBVT, "hd": HD}


def cell_names(L):
    return [c for c, _, _ in L["cells"].values()] + [L["dff"][0], L["latch"][0]]


# {cell name: (start, end)} of every cell block in a Liberty text.
def cell_map(text):
    return {m.group(1): (s, e) for s, e, m in blocks(text, r'(?m)^\s*cell\s*\(\s*"?(\w+)"?\s*\)\s*\{')}


# Copy of a Liberty file with only the cells in `keep`; area_scale makes some cells
# expensive so ABC avoids them.
def subset(src, dst, keep, area_scale=None):
    t = open(src).read()
    cb = cell_map(t)
    missing = [c for c in keep if c not in cb]
    if missing:
        sys.exit("cells missing from %s: %s" % (src, missing))
    first = min(s for s, e in cb.values())
    last = max(e for s, e in cb.values())
    body = []
    for c in keep:
        s, e = cb[c]
        b = t[s:e]
        if area_scale and c in area_scale:
            b = re.sub(r"(\barea\s*:\s*)([0-9.eE+-]+)", lambda x: x.group(1) + repr(float(x.group(2)) * area_scale[c]), b, count=1)
        body.append(b)
    open(dst, "w").write(t[:first] + "\n".join(body) + t[last:])


# inv_map.v maps Yosys $_NOT_ to the library inverter; latch_map.v maps positive latches to
# the latch cell and negative ones to latch + inverter on the enable.
def techmaps(L, out):
    inv, ip, io = L["cells"]["inv1"]
    lc, le, ld, lq, lqn = L["latch"]
    open(os.path.join(out, "inv_map.v"), "w").write(
        "module \\$_NOT_ (input A, output Y);\n  %s _TECHMAP_REPLACE_ (.%s(A), .%s(Y));\nendmodule\n" % (inv, ip["a"], io))
    open(os.path.join(out, "latch_map.v"), "w").write(
        "module \\$_DLATCH_P_ (input E, input D, output Q);\n  %s _TECHMAP_REPLACE_ (.%s(E), .%s(D), .%s(Q), .%s());\nendmodule\n\n"
        "module \\$_DLATCH_N_ (input E, input D, output Q);\n  wire en_p;\n  %s en_inv (.%s(E), .%s(en_p));\n"
        "  %s _TECHMAP_REPLACE_ (.%s(en_p), .%s(D), .%s(Q), .%s());\nendmodule\n" %
        (lc, le, ld, lq, lqn, inv, ip["a"], io, lc, le, ld, lq, lqn))
