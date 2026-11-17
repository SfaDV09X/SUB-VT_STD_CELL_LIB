# Design flow

Run everything inside the container (`docs/docker.md`) after `sak-pdk sky130A`.
`ROOT=/foss/designs/SUB-VT_STD_CELL_LIB`.

| Stage | Tool | Output |
|---|---|---|
| 0 Sizing | ngspice, Python | `docs/sizing.md` |
| 1 Schematic | xschem | `cells/<CELL>/schematic/`, `spice/<cell>.spice` |
| 2 Layout | Magic | `layout/<cell>.mag` |
| 3 DRC | Magic | `verification/drc/<cell>_drc.rpt` |
| 4 LEF + GDS | Magic | `layout/<cell>.lef`, `.gds` |
| 5 LVS | Magic + Netgen | `verification/lvs/<cell>_lvs.rpt`, `_comp.out` |
| 6 PEX (R+C) | Magic | `verification/pex/<cell>_pex.spice`, `_pex.rpt` |
| 7 Characterization | lctime, ngspice | `characterization/`, `lib/`, `datasheets/` |
| 8 Synthesis, STA, power | Yosys, iverilog, OpenSTA | `docs/synthesis.md` |

## 0. Sizing
See `docs/sizing.md` and `scripts/sizing/`.

## 1. Schematic: xschem
```
xschem $ROOT/cells/<CELL>/schematic/<cell>.sch
```
Draw with `sky130_fd_pr__nfet_01v8` / `pfet_01v8` at the sizes in `docs/sizing.md`. Export the netlist to `spice/<cell>.spice`.

## 2–6. Layout, DRC, LEF/GDS, LVS, PEX: one command
```
bash $ROOT/scripts/verification/verify_layouts.sh [CELL ...]
```
For each cell: runs `layout/<cell>.tcl` in Magic (flat devices, no device subcells), DRC, `lef write`, `gds write`, LVS extraction, Netgen LVS and R+C PEX, then prints a summary to `cells/verification_summary.txt`.
Targets: 0 DRC error boxes, `Circuits match uniquely`, LEF `SIZE W BY 4.080` with W a multiple of 0.46.

Single steps in the Magic console:
```
set cell <cell>
source $ROOT/cells/<CELL>/layout/<cell>.tcl
source $ROOT/scripts/verification/drc.tcl
source $ROOT/scripts/verification/lvs.tcl
source $ROOT/scripts/verification/pex.tcl
```
and in a shell: `bash $ROOT/scripts/verification/lvs.sh <cell>`.

## 7. Characterization: lctime, ngspice
```
bash $ROOT/scripts/characterization/run_char.sh [corners] [cells]
```
See `docs/characterization.md`.

## 8. Synthesis, STA, power: Yosys, iverilog, OpenSTA
```
bash $ROOT/scripts/synthesis/run_synth.sh
```
See `docs/synthesis.md`.
