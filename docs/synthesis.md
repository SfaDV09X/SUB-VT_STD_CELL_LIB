# Synthesis, STA, power and benchmark

Designs: `synthesis/rtl/rca8.v` (8-bit ripple-carry adder), `counter8.v` (8-bit counter with reset and enable) and `demo.v` (uses all 13 cells), with self-checking testbenches in `synthesis/tb/`.
Reference library: sky130_fd_sc_hd, tt 25 °C, 1.80 V, restricted to the 13 equivalent cells: `inv_1`, `nand2_1`, `nor2_1`, `and2_1`, `or2_1`, `xor2_1`, `xnor2_1`, `a21oi_1` (AOI3), `o21ai_1` (OAI3), `a2bb2o_1` (MOAI4), `a2bb2oi_1` (MAOI4), `dfxbp_1` (DFF), `dlxbp_1` (latch).

```
cd /foss/designs/SUB-VT_STD_CELL_LIB
bash scripts/synthesis/run_synth.sh            # all three designs; results in synthesis/out/
```

| Step | Tool | Checks / output |
|---|---|---|
| Switch-level cell check | `scripts/verification/check_cells_switchlevel.py` | each combinational transistor netlist implements its Liberty function |
| Synthesis | Yosys (`abc -liberty`, `dfflibmap`, latch techmap) | gate netlist mapped at tt 27 °C; `demo` forces every cell |
| Equivalence | Yosys `equiv_*` | gate netlist equivalent to the RTL |
| Gate-level simulation | iverilog | gate netlist matches the RTL; VCD switching activity |
| STA | OpenSTA | critical path T_crit, f_max = 1/T_crit, hold slack, at all 15 corners |
| Power | OpenSTA | internal, switching and leakage power at f_max with the simulated activity |

Conditions: zero input/output delay, inputs driven by the library inverter, outputs loaded with 4 inverter inputs. Energy per operation = total power × T_crit. Activity comes from zero-delay simulation, so glitch power is not included for either library.
Scripts: `libs.py` (library cell maps), `models.py` (Verilog models from Liberty), `synth.py`, `sta.py`, `report.py` (CSV and HTML in `synthesis/out/report/`).

## Results

| Design | Library | Cells | Library cells used | Area (µm²) | Equivalence | Gate-level sim |
|---|---|---|---|---|---|---|
| rca8 | X4 (this library) | 70 | 8 / 13 | 2120.78 | PASS | PASS |
| rca8 | sky130_fd_sc_hd | 53 | 7 / 13 | 260.25 | PASS | PASS |
| counter8 | X4 (this library) | 47 | 8 / 13 | 1655.34 | PASS | PASS |
| counter8 | sky130_fd_sc_hd | 49 | 7 / 13 | 362.85 | PASS | PASS |
| demo | X4 (this library) | 109 | 13 / 13 | 4053.89 | PASS | PASS |
| demo | sky130_fd_sc_hd | 102 | 13 / 13 | 783.25 | PASS | PASS |

Cell usage (this library):

| Design | INV1X4 | NAND2X4 | NOR2X4 | AND2X4 | OR2X4 | XOR2X4 | XNOR2X4 | AOI3X4 | OAI3X4 | MOAI4X4 | MAOI4X4 | DFFX4 | DLX4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rca8 | 13 | 10 | 22 | 1 | 2 | 5 | 0 | 9 | 8 | 0 | 0 | 0 | 0 |
| counter8 | 8 | 10 | 7 | 0 | 1 | 1 | 0 | 6 | 6 | 0 | 0 | 8 | 0 |
| demo | 19 | 7 | 23 | 3 | 4 | 9 | 4 | 14 | 9 | 1 | 1 | 11 | 4 |

## Benchmark: this library at 0.40 V vs sky130_fd_sc_hd at 1.80 V

| Design | Metric | X4, 0.4 V, tt 27 °C | hd, 1.8 V, tt 25 °C | X4 / hd |
|---|---|---|---|---|
| rca8 | Area (µm²) | 2120.8 | 260.2 | 8.15 |
| rca8 | Critical delay | 45.7 µs | 1.28 ns | 3.56e+04 |
| rca8 | Max frequency | 21.9 kHz | 779 MHz | 2.81e-05 |
| rca8 | Total power at fmax | 0.533 nW | 61 µW | 8.73e-06 |
| rca8 | Leakage power | 0.0995 nW | 0.173 nW | 0.576 |
| rca8 | Energy per operation (fJ) | 24.3 | 78.3 | 0.311 |
| counter8 | Area (µm²) | 1655.3 | 362.8 | 4.56 |
| counter8 | Critical delay | 48.8 µs | 1.09 ns | 4.49e+04 |
| counter8 | Max frequency | 20.5 kHz | 920 MHz | 2.23e-05 |
| counter8 | Total power at fmax | 1.03 nW | 442 µW | 2.32e-06 |
| counter8 | Leakage power | 0.0815 nW | 0.195 nW | 0.418 |
| counter8 | Energy per operation (fJ) | 50.0 | 480.3 | 0.104 |
| demo | Area (µm²) | 4053.9 | 783.3 | 5.18 |
| demo | Critical delay | 45.8 µs | 0.83 ns | 5.52e+04 |
| demo | Max frequency | 21.8 kHz | 1.21 GHz | 1.81e-05 |
| demo | Total power at fmax | 2.54 nW | 1.09 mW | 2.33e-06 |
| demo | Leakage power | 0.204 nW | 0.443 nW | 0.46 |
| demo | Energy per operation (fJ) | 116.0 | 901.7 | 0.129 |

## This library across corners

| Corner | rca8 Tcrit (µs) | rca8 E/op (fJ) | counter8 Tcrit (µs) | counter8 E/op (fJ) | demo Tcrit (µs) | demo E/op (fJ) | demo hold slack (µs) |
|---|---|---|---|---|---|---|---|
| tt 0 °C | 197.0 | 36.2 | 216.9 | 60.8 | 211.4 | 141.0 | 24.08 |
| tt 27 °C | 45.7 | 24.3 | 48.8 | 50.0 | 45.8 | 116.0 | 7.01 |
| tt 85 °C | 5.5 | 26.7 | 6.0 | 52.7 | 5.7 | 124.6 | 0.85 |
| ss 0 °C | 478.4 | 58.9 | 526.0 | 82.0 | 519.1 | 191.9 | 55.05 |
| ss 27 °C | 96.5 | 28.5 | 104.2 | 53.8 | 98.4 | 124.6 | 14.34 |
| ss 85 °C | 9.8 | 25.2 | 10.6 | 51.7 | 10.1 | 121.5 | 1.41 |
| ff 0 °C | 86.2 | 27.2 | 93.1 | 51.9 | 90.5 | 120.3 | 10.96 |
| ff 27 °C | 22.5 | 22.7 | 24.0 | 48.0 | 22.0 | 111.8 | 3.54 |
| ff 85 °C | 3.2 | 31.5 | 3.4 | 56.2 | 3.3 | 134.3 | 0.47 |
| sf 0 °C | 1160.7 | 116.1 | 1246.7 | 132.0 | 1292.4 | 324.5 | 52.61 |
| sf 27 °C | 174.9 | 36.4 | 181.1 | 59.6 | 191.4 | 142.8 | 10.27 |
| sf 85 °C | 9.1 | 25.0 | 9.1 | 50.4 | 9.7 | 120.2 | 0.88 |
| fs 0 °C | 318.5 | 49.5 | 356.1 | 72.5 | 325.6 | 166.4 | 24.39 |
| fs 27 °C | 87.8 | 36.5 | 94.7 | 59.1 | 87.5 | 139.7 | 6.90 |
| fs 85 °C | 10.6 | 98.4 | 10.7 | 104.0 | 9.9 | 255.7 | 0.84 |
