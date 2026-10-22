# Characterization (TT, 0.40 V, 27 C)

Result: `lib/subvt_sky130_tt_0p40v_27c.lib` (13 cells: 11 combinational and 2 sequential). Per-cell files: `cells/<CELL>/characterization/<cell>.lib`; the slew/load grid used for each combinational cell is in `<cell>.grids`.
Thresholds: delay 50/50, slew 30/70.

## Method
- **Netlists:** the schematic netlists `cells/<CELL>/spice/<cell>.spice` (no parasitics; input capacitance is gate capacitance only).
- **Fingers:** `nf=N` devices are expanded into N parallel devices of W/N (`scripts/characterization/expand.py`).
- **Models:** raw SkyWater PDK TT models.
- **Combinational cells:** lctime 0.0.26, 5x5 tables. Per cell: C_FO1 = mean input-pin capacitance; slews = s* x [0.25, 0.5, 1, 2, 4]; loads = C_FO1 x [0.5, 1, 2, 4, 8]; s* = steady-state slew of a chain of the cell, each stage loaded with one C_FO1.
- **Sequential cells:** `scripts/characterization/seqchar.py` with ngspice, 3x3 tables. Setup/hold use a 10% clk-to-Q push-out criterion.

## Scripts (`scripts/characterization/`)
| File | Purpose |
|---|---|
| `expand.py` | Expands `nf=N` devices into N parallel devices of W/N; writes `l`/`w` in metres. |
| `cells.tsv` | Inputs, output and Liberty function of each combinational cell. |
| `gen_template.py` | Writes the lctime Liberty template for one cell. |
| `make_grids.py` | Derives the FO1 slew/load grid for one cell from a 2x2 probe `.lib`. |
| `temp27.spice` | `.option TEMP=27`, passed to lctime with `-I`. |
| `seqchar.py` | ngspice characterization of DFFX1 and DLX1. Arguments: `--kind --cell --net --lef --models --corner --out`. |

## Checks
- All 13 cells parse (liberty-parser); combinational tables are finite, positive and within the simulation window.
- The synthesis check (`docs/synthesis.md`) maps and verifies the library.

## FO1 summary
Load index 2, slew index 2 of the 5x5 grid.

```
cell      C_FO1(fF)  FO1 delay rise/fall (ns, mean over arcs)  FO1 slew rise/fall (ns)  [load idx 2, slew idx 2 of 5x5]
inv1x1      2.22          274 /      419                       135 /      264
nand2x1     3.99          575 /     1153                       272 /      615
nor2x1      2.58          412 /      613                       220 /      400
and2x1      4.06         1751 /     1253                       290 /      438
or2x1       2.61         1254 /     1078                       230 /      331
xor2x1      6.71         1509 /     2128                       559 /     1129
xnor2x1     6.56         1505 /     2177                       555 /     1123
aoi3x1      3.78          662 /     1188                       331 /      686
oai3x1      4.34          791 /     1517                       407 /      870
maoi4x1     3.36         1333 /     1774                       397 /      835
moai4x1     3.52         1361 /     1797                       459 /      797
dffx1      D 1.76 / CLK 6.61 -> C_FO1 = 4.2 fF, 3x3 grid (slews 263/526/1052 ns, loads 2.1/4.2/8.4 fF)
dlx1       D 1.75 / CLK 4.69 -> C_FO1 = 3.2 fF, 3x3 grid (slews 211/422/845 ns, loads 1.6/3.2/6.4 fF)
```
