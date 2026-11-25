# Sizing targets and limits shared by all sizing scripts. Cell specific data
# (width levels, search box, baseline, device counts) comes from cells.py.

import math

from cells import CELL

# Supply, +-10 % supply check, minimum L, widest single finger, width step and L step (um),
# and the load used everywhere: 4 copies of the cell's own input (FO4).
VDD_NOM = 0.4
VDD_TOL = 0.10
L_MIN = 0.15
FINGER_MAX = 0.84
W_STEP = 0.42
L_STEP = 0.01
FANOUT = 4

# The four design variables: nmos/pmos width and length.
FEATURES = ["Wn_um", "Wp_um", "Ln_um", "Lp_um"]
W_LEVELS_N = CELL["w_levels_n"]
W_LEVELS_P = CELL["w_levels_p"]
BOX_LO = CELL["box_lo"]
BOX_HI = CELL["box_hi"]
BASELINE = CELL["baseline"]
N_NMOS = CELL["n_nmos"]
N_PMOS = CELL["n_pmos"]
KEY = FEATURES

# 15 PVT conditions, and the 5 hardest ones used during optimisation.
PVT_CORNERS = ["tt", "ss", "ff", "sf", "fs"]
PVT_TEMPS = [0.0, 27.0, 85.0]
CRITICAL = [("tt", 27.0), ("sf", 0.0), ("fs", 85.0), ("ss", 85.0), ("ff", 85.0)]
NOMINAL = ("tt", 27.0)

# Pass criteria: noise margin >= 40 mV, rise/fall asymmetry <= 25 %, output must reach
# within 10 % of the rails. AVT_*: Pelgrom mismatch coefficients (V*um) for Monte Carlo,
# MC_SIGMA_K: mean - 3 sigma of the noise margin must stay >= 0.
MIN_NM_MV = 40.0
MAX_ASYM = 0.25
SWING = 0.1
AVT_N = 3.356e-3
AVT_P = 7.356e-3
MC_SIGMA_K = 3.0
VDD_NM_FRAC = MIN_NM_MV / VDD_NOM / 1e3


def snap(x, step):
    return round(round(float(x) / step) * step, 6)


# Nearest allowed width level (compared on a log scale).
def snap_level(x, levels):
    return min(levels, key=lambda v: abs(math.log(max(float(x), 1e-9)) - math.log(v)))


def snap_design(wn, wp, ln, lp):
    return (snap_level(wn, W_LEVELS_N), snap_level(wp, W_LEVELS_P), snap(ln, L_STEP), snap(lp, L_STEP))


# Split a total width into full 0.84 um fingers plus one remainder finger.
def split_fingers(w):
    n_full = int(w / FINGER_MAX + 1e-9)
    rem = round(w - n_full * FINGER_MAX, 6)
    parts = []
    if n_full:
        parts.append((FINGER_MAX, n_full))
    if rem > 1e-6:
        if rem < W_STEP - 1e-6:
            raise ValueError(f"W={w:g} leaves a {rem:g} um finger, below the {W_STEP:g} um minimum")
        parts.append((rem, 1))
    return parts


# Active gate area estimate: sum of W*L over all devices.
def area_um2(wn, wp, ln, lp):
    return N_NMOS * wn * ln + N_PMOS * wp * lp


def tag(corner, temp):
    return f"{corner}@{float(temp):g}C"


def nm_col(corner, temp):
    return f"NM_{corner}_{float(temp):g}C"


# Turn "critical", "full15" or "corner@tempC" tokens into a list of (corner, temp).
def parse_conds(tokens):
    out = []
    for tok in tokens:
        low = tok.lower()
        if low == "critical":
            out += list(CRITICAL)
        elif low == "full15":
            out += [(c, t) for c in PVT_CORNERS for t in PVT_TEMPS]
        else:
            c, t = low.rstrip("c").split("@")[:2]
            out.append((c, float(t)))
    seen, res = set(), []
    for c in out:
        if c not in seen:
            seen.add(c)
            res.append(c)
    return res
