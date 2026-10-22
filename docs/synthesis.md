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
