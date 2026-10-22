#!/usr/bin/env bash
# Verify the synthesized netlist: (1) cells vs transistor netlists, (2) formal equivalence, (3) simulation.
# usage: scripts/synthesis/run_verify.sh [rtl.v] [top]   (run after run_synth.sh; same defaults)
# env:   LIB=<liberty>  CELLS=<cells folder>  YOSYS  TB=<testbench>
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
RTL=${1:-$ROOT/synthesis/rtl/demo.v}; TOP=${2:-demo}
LIB=${LIB:-$ROOT/lib/subvt_sky130_tt_0p40v_27c.lib}
CELLS=${CELLS:-$ROOT/cells}
YOSYS=${YOSYS:-yosys}
TB=${TB:-$ROOT/synthesis/tb/tb_demo.v}
OUT=/tmp/subvt_synth; NET=$OUT/${TOP}_gate.v
[ -f "$NET" ] || { echo "ERROR: $NET missing - run ./run_synth.sh first"; exit 2; }
fail=0

echo "== 1/3 switch-level check: transistor netlists vs liberty functions"
python3 "$ROOT/scripts/verification/check_cells_switchlevel.py" "$LIB" "$CELLS" || fail=1

echo; echo "== 2/3 formal equivalence: RTL vs gate netlist (Yosys equiv)"
cat > "$OUT/equiv.ys" <<YS
read_verilog -sv $RTL
setattr -mod -unset keep_hierarchy *
prep -top $TOP -flatten
design -stash gold
read_verilog $OUT/subvt_cells.v
read_verilog $NET
prep -top ${TOP}_gate -flatten
design -stash gate
design -copy-from gold -as gold $TOP
design -copy-from gate -as gate ${TOP}_gate
async2sync
equiv_make gold gate equiv
hierarchy -top equiv
equiv_simple -seq 2
equiv_induct -seq 2
tee -o $OUT/equiv_status.txt equiv_status
equiv_status -assert
YS
if $YOSYS -q -l "$OUT/equiv.log" -s "$OUT/equiv.ys"; then echo "equivalent: PASS"; else echo "equivalent: FAIL (see $OUT/equiv.log)"; fail=1; fi
grep -h 'Equivalence successfully' "$OUT/equiv_status.txt" 2>/dev/null

echo; echo "== 3/3 gate-level simulation vs RTL (iverilog)"
iverilog -g2005 -o "$OUT/sim.vvp" "$TB" "$RTL" "$OUT/subvt_cells.v" "$NET" && vvp -n "$OUT/sim.vvp" | tee "$OUT/sim.log" | tail -12
grep -q '^PASS' "$OUT/sim.log" || fail=1

echo; [ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit $fail
