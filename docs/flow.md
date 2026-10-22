# Design flow

Run everything inside the container (`docs/docker.md`) after `sak-pdk sky130A`.
`ROOT=/foss/designs/SUB-VT_STD_CELL_LIB`.

| Stage | Tool | Output |
|---|---|---|
| 1 Schematic | xschem | `cells/<CELL>/schematic/`, `spice/<cell>.spice` |
| 2 Layout | Magic | `layout/<cell>.mag` |
| 3 DRC | Magic | `verification/drc/<cell>_drc.rpt` |
| 4 LEF + GDS | Magic | `layout/<cell>.lef`, `.gds` |
| 5 LVS | Magic + Netgen | `verification/lvs/<cell>_lvs.rpt`, `_comp.out` |
| 6 PEX (R+C) | Magic | `verification/pex/<cell>_pex.spice`, `_pex.rpt` |
| 7 Characterization | lctime, ngspice | `characterization/<cell>.lib` |
| 8 Synthesis check | Yosys, iverilog | see `docs/synthesis.md` |

## 1. Schematic: xschem
```
xschem $ROOT/cells/<CELL>/schematic/<cell>.sch
```
Draw with `sky130_fd_pr__nfet_01v8` / `pfet_01v8` (L = 0.15 um). Export the netlist to `spice/<cell>.spice`.

## 2. Layout: Magic
In the Magic console:
```
source $ROOT/cells/<CELL>/layout/<cell>.tcl
```
Builds the layout, saves `<cell>.mag` and prints port errors.

## 3. DRC: Magic
```
set cell <cell>
source $ROOT/scripts/verification/drc.tcl
```
Target: 0 error boxes in `<cell>_drc.rpt`.

## 4. LEF and GDS: Magic
With the cell loaded: `lef write`, then `gds write`.

## 5. LVS: Magic, then Netgen
In Magic (extracts `<cell>_layout.spice`):
```
set cell <cell>
source $ROOT/scripts/verification/lvs.tcl
```
In a shell (compares it with `spice/<cell>.spice`):
```
bash $ROOT/scripts/verification/lvs.sh <cell>
```
Target: `Circuits match uniquely`; LEF `SIZE W BY 4.080` with W a multiple of 0.46.

## 6. PEX: Magic
```
set cell <cell>
source $ROOT/scripts/verification/pex.tcl
```
The cell width is read from the LEF unless you `set w <um>` first.

## 7. Characterization: lctime, ngspice
Combinational cells use lctime and the sequential cells use `seqchar.py` with ngspice. See `docs/characterization.md`.

## 8. Synthesis check: Yosys, iverilog
```
bash $ROOT/scripts/synthesis/run_synth.sh
bash $ROOT/scripts/synthesis/run_verify.sh
```
