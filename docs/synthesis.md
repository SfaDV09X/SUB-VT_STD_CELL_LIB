# Synthesis check

`synthesis/rtl/demo.v` is synthesized with Yosys onto `lib/subvt_sky130_tt_0p40v_27c.lib`; the netlist is then checked against the RTL.
`synthesis/tb/tb_demo.v` is the testbench. The scripts are in `scripts/synthesis/`.

```
cd /foss/designs/SUB-VT_STD_CELL_LIB
bash scripts/synthesis/run_synth.sh     # prints cell usage (13/13 expected)
bash scripts/synthesis/run_verify.sh    # ends with ALL CHECKS PASSED
```

| Step | Checks |
|---|---|
| switch-level (`scripts/verification/check_cells_switchlevel.py`) | each combinational transistor netlist implements the function in the `.lib` |
| `equiv_*` in Yosys | synthesized netlist is equivalent to the RTL |
| iverilog | gate netlist built from `.lib`-derived models matches the RTL for all data vectors and random reset/set/load/latch-enable |

## Larger designs: rca8 and counter8

Two further designs use the same flow: `synthesis/rtl/rca8.v` (8-bit ripple-carry adder) and `synthesis/rtl/counter8.v` (8-bit counter with reset and enable). Testbenches are `synthesis/tb/tb_rca8.v` and `synthesis/tb/tb_counter8.v`.

```
bash scripts/synthesis/run_synth.sh synthesis/rtl/rca8.v rca8
bash scripts/synthesis/run_synth.sh synthesis/rtl/counter8.v counter8
```

Results with the library as committed (0.40 V, TT, 27 C):

| Design | Cells | Library cells used | Area (um2) | Critical path (us) | Leakage (pW) |
|---|---|---|---|---|---|
| rca8 | 90 | 6 of 13 | 1492.06 | 15.88 | 121.3 |
| counter8 | 50 | 7 of 13 | 1582.14 | 15.90 | 106.2 |
