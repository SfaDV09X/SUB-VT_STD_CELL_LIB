# Characterization (13 cells, 15 PVT corners, 0.40 V)

Results:
- Libraries: `lib/<proc>_<T>c/subvt_sky130_<proc>_0p40v_<T>c.lib` (15 corners: tt, ss, ff, sf, fs at 0, 27 and 85 °C).
- Per cell: `cells/<CELL>/characterization/<cell>_<proc>_0p40v_<T>c.lib`; the slew/load grid of every corner is in `<cell>.grids`.
- Datasheets: `datasheets/index.html` (one page per cell, corner selector).

Thresholds: delay 50/50, slew 30/70.

## Method
- **Netlists:** R+C parasitic netlists from PEX, `cells/<CELL>/verification/pex/<cell>_pex.spice`.
- **Models:** sky130A combined models, FET section of each process corner.
- **Grid:** 5x5 per cell and corner, centred on FO4. C_FO4 = 4 × mean input-pin capacitance; slew* = steady-state FO4 slew (fixed point of output slew at C_FO4); loads = C_FO4 × [0.25, 0.5, 1, 2, 4]; slews = slew* × [0.25, 0.5, 1, 2, 4].
- **Combinational cells:** lctime 0.0.26 (interactive ngspice, 2×10^4 points per transient), probe grid first, then the FO4 grid.
- **Sequential cells:** `seqchar.py` with ngspice: CLK→Q (and D→Q for DLX4) tables; setup and hold by bisection, 10 % CLK→Q push-out criterion.
- **Power and leakage:** `measure.py` with ngspice: internal energy per arc and grid point (supply energy minus load energy), leakage per input state; `apply.py` writes them into the libraries.

## Scripts (`scripts/characterization/`)
| File | Purpose |
|---|---|
| `run_char.sh [corners] [cells]` | Whole flow: all corners, libraries, datasheets, grids. Resumes after an interruption. |
| `charflow.py` | Per corner: templates, probe, FO4 grid, lctime, seqchar, power/leakage, libraries. |
| `lct.py` | lctime launcher with the reduced transient point count. |
| `seqchar.py` | ngspice characterization of DLX4 and DFFX4. |
| `measure.py`, `apply.py`, `libtools.py` | Internal power and leakage measurement and Liberty patching. |
| `datasheet.py` | HTML datasheets. |
| `grids.py` | `<cell>.grids` files. |
| `cells.tsv` | Inputs, output and Liberty function of each combinational cell. |

## Checks
- All 15 libraries parse with 13 cells each; no NaN; every cell has leakage data.
- All delay and transition tables are positive and increase with load, except at fs 27 °C and fs 85 °C (negative delays at the slowest input slews: the output switches before the input reaches 50 %) and a few tables whose slowest-slew column decreases slightly with load (the output follows the slow input).
- Recharacterizing INV1X4 at tt 27 °C with the repository scripts reproduces the committed library byte for byte.

## Cells at tt 27 °C
FO4 point: load C_FO4, input slew slew*; delays and slews are the mean over all arcs.

| Cell | Area (µm²) | Input cap (fF) | C_FO4 (fF) | FO4 slew (ns) | FO4 delay rise / fall (ns) | Output slew rise / fall (ns) | Leakage (pW) |
|---|---|---|---|---|---|---|---|
| INV1X4 | 9.38 | A 3.12 | 12.5 | 1427 | 3271 / 3022 | 1580 / 1273 | 0.26 |
| NAND2X4 | 30.03 | A 11.86, B 11.81 | 47.3 | 3100 | 6584 / 7202 | 2920 / 3276 | 1.19 |
| NOR2X4 | 26.28 | A 9.66, B 9.64 | 38.6 | 2178 | 5226 / 4408 | 2592 / 1761 | 1.21 |
| AND2X4 | 43.17 | A 11.52, B 11.61 | 46.3 | 1660 | 6335 / 5710 | 1893 / 1549 | 2.12 |
| OR2X4 | 39.41 | A 9.48, B 9.28 | 37.5 | 1424 | 4775 / 5059 | 1582 / 1306 | 1.87 |
| XOR2X4 | 61.93 | A 16.02, B 16.53 | 65.2 | 3065 | 8409 / 8448 | 3292 / 2949 | 3.56 |
| XNOR2X4 | 61.93 | A 16.34, B 17.38 | 67.5 | 3203 | 8697 / 8750 | 3381 / 3020 | 3.56 |
| AOI3X4 | 43.17 | A 12.48, B 12.79, C 8.59 | 45.1 | 2521 | 5690 / 5724 | 2559 / 2471 | 1.57 |
| OAI3X4 | 37.54 | A 13.46, B 13.06, C 8.35 | 46.5 | 2844 | 6298 / 6266 | 2970 / 2710 | 2.33 |
| MAOI4X4 | 61.93 | A 3.12, B 3.14, C 10.95, D 10.81 | 28.0 | 2179 | 6375 / 6384 | 2256 / 2100 | 2.77 |
| MOAI4X4 | 60.06 | A 3.12, B 3.15, C 10.85, D 11.05 | 28.2 | 2196 | 6514 / 6287 | 2459 / 1933 | 2.83 |
| DLX4 | 50.67 | CLK 10.46, D 5.15 | 31.2 | 1998 | 8263 / 8426 | 2201 / 1794 | 2.58 |
| DFFX4 | 63.81 | CLK 13.77, D 3.49 | 34.5 | 2175 | 12103 / 12273 | 2398 / 1952 | 3.61 |

Setup and hold at the FO4 slew (ns):
- DLX4 (vs CLK falling): setup 1492 (D↑) / 5845 (D↓), hold −4648 (D↑) / −995 (D↓).
- DFFX4 (vs CLK rising): setup 5010 (D↑) / 4281 (D↓), hold −1564 (D↑) / −4215 (D↓).

## Corners
Values at each cell's FO4 point.

| Corner | INV1X4 FO4 slew (ns) | INV1X4 FO4 delay rise/fall (ns) | DFFX4 CLK→Q rise/fall (ns) | DFFX4 setup D↑/D↓ (ns) | Library leakage, mean of 13 cells (pW) |
|---|---|---|---|---|---|
| tt 0 °C | 5871 | 15561 / 10533 | 55643 / 64061 | 21736 / 18149 | 1.99 |
| tt 27 °C | 1427 | 3271 / 3022 | 13573 / 15883 | 5010 / 4281 | 2.27 |
| tt 85 °C | 186 | 301 / 476 | 1863 / 2055 | 588 / 488 | 24.48 |
| ss 0 °C | 13977 | 38710 / 23572 | 135300 / 154483 | 54305 / 47038 | 1.94 |
| ss 27 °C | 2967 | 7126 / 6031 | 28619 / 34036 | 10872 / 9642 | 2.09 |
| ss 85 °C | 319 | 544 / 820 | 3109 / 3601 | 1048 / 914 | 10.41 |
| ff 0 °C | 2600 | 6556 / 4919 | 24229 / 27542 | 9204 / 7382 | 2.07 |
| ff 27 °C | 710 | 1548 / 1560 | 6676 / 7580 | 2393 / 1963 | 2.91 |
| ff 85 °C | 111 | 168 / 283 | 1123 / 1179 | 342 / 270 | 76.76 |
| sf 0 °C | 39772 | 131547 / 31718 | 307926 / 270868 | 156669 / 107052 | 1.97 |
| sf 27 °C | 5458 | 17996 / 5369 | 45076 / 42113 | 21966 / 14218 | 2.25 |
| sf 85 °C | 280 | 817 / 371 | 2477 / 2449 | 1047 / 701 | 10.89 |
| fs 0 °C | 8708 | 9431 / 28416 | 82539 / 119881 | 26922 / 31355 | 2.15 |
| fs 27 °C | 2645 | 2515 / 8643 | 24090 / 30523 | 7081 / 6563 | 4.25 |
| fs 85 °C | 443 | 262 / 1333 | 3621 / 3954 | 753 / 286 | 162.69 |

