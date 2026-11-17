# Sub-Threshold Standard Cell Library (SkyWater sky130A)

Open-source, fixed-height digital standard cell library designed for sub-threshold operation at **VDD = 0.40 V**, targeting the SkyWater sky130A 130 nm PDK. The whole flow (sizing, schematic, layout, verification, characterization, synthesis and benchmark) runs in the [iic-osic-tools](https://github.com/iic-jku/iic-osic-tools) Docker image, pinned to tag **2026.07**.

License: MIT (`LICENSE.md`).

## 1. Status

| Cell | Function | Width (µm) | Schematic | Netlist | Layout | LEF | GDS | DRC | LVS | PEX | Liberty |
|---|---|---|---|---|---|---|---|---|---|---|---|
| INV1X4 | `!A` | 2.30 | yes | yes | yes | yes | yes | 0 errors | match | R=20, C=23 | 15 corners |
| NAND2X4 | `!(A&B)` | 7.36 | yes | yes | yes | yes | yes | 0 errors | match | R=130, C=125 | 15 corners |
| NOR2X4 | `!(A\|B)` | 6.44 | yes | yes | yes | yes | yes | 0 errors | match | R=103, C=96 | 15 corners |
| AND2X4 | `A&B` | 10.58 | yes | yes | yes | yes | yes | 0 errors | match | R=190, C=177 | 15 corners |
| OR2X4 | `A\|B` | 9.66 | yes | yes | yes | yes | yes | 0 errors | match | R=162, C=147 | 15 corners |
| XOR2X4 | `(A&!B)\|(!A&B)` | 15.18 | yes | yes | yes | yes | yes | 0 errors | match | R=301, C=270 | 15 corners |
| XNOR2X4 | `(A&B)\|(!A&!B)` | 15.18 | yes | yes | yes | yes | yes | 0 errors | match | R=303, C=272 | 15 corners |
| AOI3X4 | `!((A&B)\|C)` | 10.58 | yes | yes | yes | yes | yes | 0 errors | match | R=203, C=191 | 15 corners |
| OAI3X4 | `!((A\|B)&C)` | 9.20 | yes | yes | yes | yes | yes | 0 errors | match | R=196, C=187 | 15 corners |
| MAOI4X4 | `(A\|B)&!(C&D)` | 15.18 | yes | yes | yes | yes | yes | 0 errors | match | R=270, C=253 | 15 corners |
| MOAI4X4 | `(A&B)\|(!C&!D)` | 14.72 | yes | yes | yes | yes | yes | 0 errors | match | R=271, C=255 | 15 corners |
| DLX4 | D-latch, active-high CLK | 12.42 | yes | yes | yes | yes | yes | 0 errors | match | R=167, C=163 | 15 corners |
| DFFX4 | D flip-flop, rising edge | 15.64 | yes | yes | yes | yes | yes | 0 errors | match | R=213, C=203 | 15 corners |

Cell names: combinational: `<FUNCTION><FANIN>X<DRIVE>`; sequential: `<FUNCTION>X<DRIVE>`.
DRC, LVS and PEX results are read from `cells/<CELL>/verification/` (summary: `cells/verification_summary.txt`).
Corners: tt, ss, ff, sf, fs at 0, 27 and 85 °C, all at 0.40 V.

## 2. Repository layout

```
cells/<CELL>/                   one folder per cell
  schematic/                    xschem .sch / .sym
  spice/                        schematic netlist
  layout/                       <cell>.tcl (Magic script, flat devices), .mag, .lef, .gds
  verification/{drc,lvs,pex}/   DRC report, LVS report, R+C parasitic netlist
  characterization/             <cell>_<proc>_0p40v_<T>c.lib (15 corners), <cell>.grids
lib/<proc>_<T>c/                library per corner: subvt_sky130_<proc>_0p40v_<T>c.lib
datasheets/                     HTML datasheets: index.html, one page per cell, all 15 corners
scripts/sizing/                 transistor sizing (GPR surrogate + Bayesian optimization)
scripts/verification/           drc.tcl, lvs.tcl, lvs.sh, pex.tcl, verify_layouts.sh, check_cells_switchlevel.py
scripts/characterization/       lctime / ngspice characterization flow
scripts/synthesis/              Yosys / iverilog / OpenSTA synthesis, STA, power and benchmark flow
synthesis/                      benchmark RTL and testbenches
docs/                           sizing, flow, characterization, synthesis, docker
pdk/                            PDK and tool versions
```

## 3. Quick start

1. `git clone git@github.com:SfaDV09X/SUB-VT_STD_CELL_LIB.git` into your DESIGNS folder (`/foss/designs` in the container).
2. Start the container as described in `docs/docker.md` (tag `2026.07`, then `sak-pdk sky130A`).
3. `cd /foss/designs/SUB-VT_STD_CELL_LIB`

| Step | Command |
|---|---|
| Layout, DRC, LEF/GDS, LVS, PEX for all cells | `bash scripts/verification/verify_layouts.sh` |
| Characterization, all corners, libraries and datasheets | `bash scripts/characterization/run_char.sh` |
| Synthesis, STA, power and benchmark | `bash scripts/synthesis/run_synth.sh` |

## 4. Using the library

- Liberty: `lib/<proc>_<T>c/subvt_sky130_<proc>_0p40v_<T>c.lib` (13 cells per corner); typical corner `lib/tt_27c/`.
- Physical views: `cells/<CELL>/layout/<cell>.lef` and `.gds`.
- Datasheets: open `datasheets/index.html`.
- Devices: `sky130_fd_pr__nfet_01v8` / `pfet_01v8`, sizing in `docs/sizing.md`. Cell height 4.080 µm; widths are multiples of 0.46 µm. Power pins: `VDD`, `GND`.
