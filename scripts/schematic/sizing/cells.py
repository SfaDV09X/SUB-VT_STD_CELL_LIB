# Per-cell sizing setup, selected with SUBVT_CELL. For each cell: netlist, inputs and output,
# logic function (for the truth-table check), the input arcs to test with the side-input
# values, devices with fixed sizes, the allowed width levels, the search box
# (Wn, Wp, Ln, Lp) lo/hi and a baseline design.

import os

# Already sized cells, reused for the output inverters of the two-stage cells
# (override with SUBVT_INV_SIZED / SUBVT_NAND2_SIZED / SUBVT_NOR2_SIZED).
INV_SIZED = tuple(float(x) for x in os.environ.get("SUBVT_INV_SIZED", "0.84,1.68,0.29,0.21").split(","))
INV_N = (INV_SIZED[0], INV_SIZED[2])
INV_P = (INV_SIZED[1], INV_SIZED[3])
NAND2_SIZED = tuple(float(x) for x in os.environ.get("SUBVT_NAND2_SIZED", "3.36,5.04,0.26,0.22").split(","))
NOR2_SIZED = tuple(float(x) for x in os.environ.get("SUBVT_NOR2_SIZED", "2.52,4.20,0.26,0.20").split(","))
W_N_WIDE = (0.84, 1.68, 2.52, 3.36, 4.2, 5.04)
W_P_WIDE = (0.42, 0.84, 1.68, 2.52, 3.36, 4.2, 5.04)

CELLS = {
    # nc = non-controlling value of the other inputs when one input switches.
    "inv1x4": {
        "netlist": "cells/INV1X4/spice/inv1x4.spice",
        "inputs": ["A"],
        "output": "Y",
        "nc": None,
        "func": lambda v: not v[0],
        "n_nmos": 1, "n_pmos": 1,
        "w_levels_n": (0.84, 1.68, 2.52),
        "w_levels_p": (0.42, 0.84, 1.68, 2.52),
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (2.52, 2.52, 0.30, 0.23),
        "baseline": (2.52, 0.42, 0.15, 0.15),
    },
    "nand2x4": {
        "netlist": "cells/NAND2X4/spice/nand2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "nc": 1,
        "func": lambda v: not (v[0] and v[1]),
        "n_nmos": 2, "n_pmos": 2,
        "w_levels_n": (0.84, 1.68, 2.52, 3.36, 4.2, 5.04),
        "w_levels_p": (0.42, 0.84, 1.68, 2.52, 3.36, 4.2, 5.04),
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (5.04, 0.42, 0.15, 0.15),
    },
    "nor2x4": {
        "netlist": "cells/NOR2X4/spice/nor2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "nc": 0,
        "func": lambda v: not (v[0] or v[1]),
        "n_nmos": 2, "n_pmos": 2,
        "w_levels_n": (0.84, 1.68, 2.52, 3.36, 4.2, 5.04),
        "w_levels_p": (0.42, 0.84, 1.68, 2.52, 3.36, 4.2, 5.04),
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (2.52, 0.84, 0.15, 0.15),
    },
    # Two-stage cells: first stage swept, output inverter fixed to the INV1X4 sizing.
    "and2x4": {
        "netlist": "cells/AND2X4/spice/and2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "func": lambda v: bool(v[0] and v[1]),
        "arcs": [
            {"pin": "A", "side": {"B": 1}, "inv": False},
            {"pin": "B", "side": {"A": 1}, "inv": False},
        ],
        "fixed": {"XM5": INV_N, "XM6": INV_P},
        "n_nmos": 2, "n_pmos": 2,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (5.04, 0.42, 0.15, 0.15),
    },
    "or2x4": {
        "netlist": "cells/OR2X4/spice/or2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "func": lambda v: bool(v[0] or v[1]),
        "arcs": [
            {"pin": "A", "side": {"B": 0}, "inv": False},
            {"pin": "B", "side": {"A": 0}, "inv": False},
        ],
        "fixed": {"XM6": INV_N, "XM5": INV_P},
        "n_nmos": 2, "n_pmos": 2,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (2.52, 0.84, 0.15, 0.15),
    },
    # Same cells the other way round: NAND2/NOR2 stage fixed, output inverter swept.
    "and2x4_out": {
        "netlist": "cells/AND2X4/spice/and2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "func": lambda v: bool(v[0] and v[1]),
        "arcs": [
            {"pin": "A", "side": {"B": 1}, "inv": False},
            {"pin": "B", "side": {"A": 1}, "inv": False},
        ],
        "fixed": {"XM1": (NAND2_SIZED[0], NAND2_SIZED[2]), "XM2": (NAND2_SIZED[0], NAND2_SIZED[2]),
                  "XM3": (NAND2_SIZED[1], NAND2_SIZED[3]), "XM4": (NAND2_SIZED[1], NAND2_SIZED[3])},
        "n_nmos": 1, "n_pmos": 1,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.15),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": INV_SIZED,
    },
    "or2x4_out": {
        "netlist": "cells/OR2X4/spice/or2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "func": lambda v: bool(v[0] or v[1]),
        "arcs": [
            {"pin": "A", "side": {"B": 0}, "inv": False},
            {"pin": "B", "side": {"A": 0}, "inv": False},
        ],
        "fixed": {"XM1": (NOR2_SIZED[0], NOR2_SIZED[2]), "XM2": (NOR2_SIZED[0], NOR2_SIZED[2]),
                  "XM3": (NOR2_SIZED[1], NOR2_SIZED[3]), "XM4": (NOR2_SIZED[1], NOR2_SIZED[3])},
        "n_nmos": 1, "n_pmos": 1,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.15),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": INV_SIZED,
    },
    # Cells with input inverters: the inverters are fixed, explicit arcs set the other inputs.
    "xor2x4": {
        "netlist": "cells/XOR2X4/spice/xor2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "func": lambda v: bool(v[0]) != bool(v[1]),
        "arcs": [
            {"pin": "A", "side": {"B": 0}, "inv": False, "label": "A_b0"},
            {"pin": "A", "side": {"B": 1}, "inv": True, "label": "A_b1"},
            {"pin": "B", "side": {"A": 0}, "inv": False, "label": "B_a0"},
            {"pin": "B", "side": {"A": 1}, "inv": True, "label": "B_a1"},
        ],
        "fixed": {"XM9": INV_N, "XM10": INV_P, "XM11": INV_N, "XM12": INV_P},
        "n_nmos": 4, "n_pmos": 4,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (5.04, 0.84, 0.15, 0.15),
    },
    "xnor2x4": {
        "netlist": "cells/XNOR2X4/spice/xnor2x4.spice",
        "inputs": ["A", "B"],
        "output": "Y",
        "func": lambda v: bool(v[0]) == bool(v[1]),
        "arcs": [
            {"pin": "A", "side": {"B": 0}, "inv": True, "label": "A_b0"},
            {"pin": "A", "side": {"B": 1}, "inv": False, "label": "A_b1"},
            {"pin": "B", "side": {"A": 0}, "inv": True, "label": "B_a0"},
            {"pin": "B", "side": {"A": 1}, "inv": False, "label": "B_a1"},
        ],
        "fixed": {"XM9": INV_N, "XM10": INV_P, "XM11": INV_N, "XM12": INV_P},
        "n_nmos": 4, "n_pmos": 4,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (5.04, 0.84, 0.15, 0.15),
    },
    "aoi3x4": {
        "netlist": "cells/AOI3X4/spice/aoi3x4.spice",
        "inputs": ["A", "B", "C"],
        "output": "Y",
        "func": lambda v: not ((v[0] and v[1]) or v[2]),
        "arcs": [
            {"pin": "A", "side": {"B": 1, "C": 0}},
            {"pin": "B", "side": {"A": 1, "C": 0}},
            {"pin": "C", "side": {"A": 1, "B": 0}},
        ],
        "w_scale": {"XM5": 0.5},
        "n_nmos": 3, "n_pmos": 3,
        "w_levels_n": (3.36, 4.2, 5.04), "w_levels_p": (2.52, 3.36, 4.2, 5.04),
        "box_lo": (3.36, 2.52, 0.22, 0.19),
        "box_hi": (5.04, 5.04, 0.30, 0.21),
        "baseline": (5.04, 0.84, 0.15, 0.15),
    },
    "oai3x4": {
        "netlist": "cells/OAI3X4/spice/oai3x4.spice",
        "inputs": ["A", "B", "C"],
        "output": "Y",
        "func": lambda v: not ((v[0] or v[1]) and v[2]),
        "arcs": [
            {"pin": "A", "side": {"B": 0, "C": 1}},
            {"pin": "B", "side": {"A": 0, "C": 1}},
            {"pin": "C", "side": {"A": 1, "B": 0}},
        ],
        "w_scale": {"XM3": 0.5},
        "n_nmos": 3, "n_pmos": 3,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (5.04, 0.84, 0.15, 0.15),
    },
    "maoi4x4": {
        "netlist": "cells/MAOI4X4/spice/maoi4x4.spice",
        "inputs": ["A", "B", "C", "D"],
        "output": "Y",
        "func": lambda v: bool((v[0] or v[1]) and not (v[2] and v[3])),
        "arcs": [
            {"pin": "A", "side": {"B": 0, "C": 0, "D": 1}, "inv": False},
            {"pin": "B", "side": {"A": 0, "C": 0, "D": 1}, "inv": False},
            {"pin": "C", "side": {"A": 1, "B": 0, "D": 1}},
            {"pin": "D", "side": {"A": 1, "B": 0, "C": 1}},
        ],
        "fixed": {"XM9": INV_N, "XM10": INV_P, "XM11": INV_N, "XM12": INV_P},
        "n_nmos": 4, "n_pmos": 4,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (5.04, 0.84, 0.15, 0.15),
    },
    "moai4x4": {
        "netlist": "cells/MOAI4X4/spice/moai4x4.spice",
        "inputs": ["A", "B", "C", "D"],
        "output": "Y",
        "func": lambda v: bool((v[0] and v[1]) or (not v[2] and not v[3])),
        "arcs": [
            {"pin": "A", "side": {"B": 1, "C": 1, "D": 0}, "inv": False},
            {"pin": "B", "side": {"A": 1, "C": 1, "D": 0}, "inv": False},
            {"pin": "C", "side": {"A": 0, "B": 1, "D": 0}},
            {"pin": "D", "side": {"A": 0, "B": 1, "C": 0}},
        ],
        "fixed": {"XM9": INV_N, "XM10": INV_P, "XM11": INV_P, "XM12": INV_N},
        "n_nmos": 4, "n_pmos": 4,
        "w_levels_n": W_N_WIDE, "w_levels_p": W_P_WIDE,
        "box_lo": (0.84, 0.42, 0.15, 0.18),
        "box_hi": (5.04, 5.04, 0.30, 0.23),
        "baseline": (5.04, 0.84, 0.15, 0.15),
    },
}

CELL_NAME = os.environ.get("SUBVT_CELL", "inv1x4").lower()
if CELL_NAME not in CELLS:
    raise SystemExit(f"SUBVT_CELL={CELL_NAME!r} is not defined in cells.py (known: {', '.join(CELLS)})")
CELL = CELLS[CELL_NAME]
