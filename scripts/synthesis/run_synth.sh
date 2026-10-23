#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
RTL=${1:-$ROOT/synthesis/rtl/demo.v}
TOP=${2:-demo}
LIB=${LIB:-$ROOT/lib/subvt_sky130_tt_0p40v_27c.lib}
YOSYS=${YOSYS:-yosys}
OUT=/tmp/subvt_synth; rm -rf "$OUT"; mkdir -p "$OUT/lib"
[ -f "$LIB" ] || { echo "ERROR: liberty not found: $LIB   (set LIB=...)"; exit 2; }

printf 'strash\ndch -f\nmap\n' > "$OUT/map.script"
printf 'strash\ndch -f\nmap -a\n' > "$OUT/map_area.script"

python3 "$HERE/gen_models.py" "$LIB" "$OUT/subvt_cells.v"

COV=$(grep -oE 'module cov_[a-z0-9]+' "$RTL" | sed 's/module cov_//' || true)
for c in $COV; do
  if [ "$c" = nand2x1 ]; then H="inv1x1 nor2x1"; else H="inv1x1 nand2x1"; fi
  python3 "$HERE/sublib.py" "$LIB" "$OUT/lib/only_$c.lib" "$c" $H
done

{
echo "read_verilog -sv $RTL"
echo "read_liberty -overwrite -setattr liberty_cell -lib $LIB"
echo "hierarchy -check -top $TOP"
echo "synth -top $TOP -flatten"
echo "dfflegalize -cell \$_DFF_P_ x -cell \$_DLATCH_P_ x -cell \$_DLATCH_N_ x"
echo "techmap -map $HERE/techmap/latch_map.v"
echo "dfflibmap -liberty $LIB"
for c in $COV; do
  echo "cd cov_$c"
  if [ "$c" = inv1x1 ]; then echo "techmap -map $HERE/techmap/inv_map.v"
  else echo "abc -liberty $OUT/lib/only_$c.lib -script $OUT/map_area.script"; fi
  echo "cd .."
done
echo "cd $TOP";   echo "abc -liberty $LIB -script $OUT/map.script"; echo "cd .."
echo "setattr -mod -unset keep_hierarchy *"
echo "flatten"
echo "opt_clean -purge"
echo "hierarchy -top $TOP"
echo "rename $TOP ${TOP}_gate"
echo "check -assert"
echo "tee -o $OUT/stat.txt stat -liberty $LIB"
echo "write_verilog -noattr -noexpr $OUT/${TOP}_gate.v"
} > "$OUT/synth.ys"

$YOSYS -q -l "$OUT/synth.log" -s "$OUT/synth.ys"
python3 "$HERE/coverage_report.py" "$LIB" "$OUT/${TOP}_gate.v"
