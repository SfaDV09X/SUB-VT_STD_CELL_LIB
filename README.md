# Sub-Threshold Standard Cell Library (SkyWater sky130A)

Open-source, fixed-height digital standard cell library designed for sub-threshold operation at **VDD = 0.40 V**, targeting the SkyWater sky130A 130 nm PDK. The whole flow (schematic, layout, verification, characterization, synthesis check) runs in the [iic-osic-tools](https://github.com/iic-jku/iic-osic-tools) Docker image, pinned to tag **2026.07**.

License: MIT (`LICENSE.md`).

## 1. Status

| Cell | Function | Schematic | Netlist | Layout | LEF | GDS | DRC | LVS | PEX | Liberty |
|---|---|---|---|---|---|---|---|---|---|---|
| INV1X1 | `!A` | yes | yes | yes | yes | yes | 0 errors | match | R=8, C=14 | yes |
| NAND2X1 | `!(A&B)` | yes | yes | yes | yes | yes | 0 errors | match | R=16, C=38 | yes |
| NOR2X1 | `!(A\|B)` | yes | yes | yes | yes | yes | 0 errors | match | R=16, C=31 | yes |
| AND2X1 | `A&B` | yes | yes | yes | yes | yes | 0 errors | match | R=24, C=51 | yes |
| OR2X1 | `A\|B` | yes | yes | yes | yes | yes | 0 errors | match | R=24, C=45 | yes |
| XOR2X1 | `(A&!B)\|(!A&B)` | yes | yes | yes | yes | yes | 0 errors | match | R=48, C=100 | yes |
| XNOR2X1 | `(A&B)\|(!A&!B)` | yes | yes | yes | yes | yes | 0 errors | match | R=48, C=100 | yes |
| AOI3X1 | `!((A&B)\|C)` | yes | yes | yes | yes | yes | 0 errors | match | R=24, C=57 | yes |
| OAI3X1 | `!((A\|B)&C)` | yes | yes | yes | yes | yes | 0 errors | match | R=24, C=62 | yes |
| MAOI4X1 | `(A\|B)&!(C&D)` | yes | yes | yes | yes | yes | 0 errors | match | R=48, C=112 | yes |
| MOAI4X1 | `(A&B)\|(!C&!D)` | yes | yes | yes | yes | yes | 0 errors | match | R=48, C=119 | yes |
| DLX1 | D-latch, active-high CLK | yes | yes | yes | yes | yes | 0 errors | match | R=40, C=67 | yes |
| DFFX1 | D flip-flop, rising edge | yes | yes | yes | yes | yes | 0 errors | match | R=72, C=120 | yes |

Cell names: combinational: `<FUNCTION><FANIN>X<DRIVE>`; sequential: `<FUNCTION>X<DRIVE>`.
DRC, LVS and PEX results are read from `cells/<CELL>/verification/`.

## 2. Repository layout

```
cells/<CELL>/                   one folder per cell
  schematic/                    xschem .sch / .sym
  spice/                        schematic netlist
  layout/                       <cell>.tcl (Magic script), .mag, .lef, .gds
  verification/{drc,lvs,pex}/   DRC report, extracted layout netlist, parasitic netlists
  characterization/             <cell>.lib, <cell>.grids
lib/                            merged Liberty file: subvt_sky130_tt_0p40v_27c.lib
analysis/mep/                   minimum-energy-point analysis using INV1X1
scripts/verification/           drc.tcl, lvs.tcl, lvs.sh, pex.tcl, check_cells_switchlevel.py
scripts/synthesis/              Yosys / iverilog scripts for the synthesis check
scripts/characterization/       helper scripts for lctime / ngspice characterization
synthesis/                      demo RTL and TB for the Yosys synthesis check
docs/                           characterisation, docker, flow, synthesis
pdk/                            PDK and Tool versions
```

## 3. Quick start

1. `git clone git@github.com:SfaDV09X/SUB-VT_STD_CELL_LIB.git` into your DESIGNS folder (`/foss/designs` in the container).
2. Start the container as described in `docs/docker.md` (tag `2026.07`, then `sak-pdk sky130A`).
3. `cd /foss/designs/SUB-VT_STD_CELL_LIB`

Check the transistor netlists against the Liberty functions (plain Python 3):

```
python3 scripts/verification/check_cells_switchlevel.py lib/subvt_sky130_tt_0p40v_27c.lib cells
```

## 4. Using the library

- Liberty: `lib/subvt_sky130_tt_0p40v_27c.lib` (13 cells, TT, 0.40 V, 27 C).
- Physical views: `cells/<CELL>/layout/<cell>.lef` and `.gds`.
- Synthesis with Yosys: `docs/synthesis.md`.
- Devices: `sky130_fd_pr__nfet_01v8` / `pfet_01v8`, L = 0.15 um. Cell height 4.080 um; widths are multiples of 0.46 um. Power pins: `VDD`, `GND`.
