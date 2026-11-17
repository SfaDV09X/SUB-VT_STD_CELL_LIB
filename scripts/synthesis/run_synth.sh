#!/bin/bash
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
SYN=$ROOT/synthesis
LIBDIR=${LIBDIR:-$ROOT/lib}
TT=$LIBDIR/tt_27c/subvt_sky130_tt_0p40v_27c.lib
HD_LIB=${HD_LIB:-${PDK_ROOT:-/foss/pdks}/${PDK:-sky130A}/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib}
OUT=${OUT:-$SYN/out}
DESIGNS=${1:-rca8,counter8,demo}
for t in yosys iverilog vvp python3; do command -v $t >/dev/null || { echo "$t not found"; exit 1; }; done
STA=${STA:-$(command -v sta || command -v openroad)}
[ -n "$STA" ] || { echo "neither sta nor openroad found"; exit 1; }
[ -f "$TT" ] || { echo "corner libraries not found in $LIBDIR"; exit 1; }
[ -f "$HD_LIB" ] || { echo "sky130_fd_sc_hd liberty not found: $HD_LIB"; exit 1; }
mkdir -p "$OUT/libs"
cd "$HERE" || exit 1
python3 -c "import libs; libs.subset('$HD_LIB', '$OUT/libs/hd13_tt_025C_1v80.lib', libs.cell_names(libs.HD))" || exit 1
python3 "$ROOT/scripts/verification/check_cells_switchlevel.py" "$TT" "$ROOT/cells" | tee "$OUT/switchlevel.txt" | tail -1
python3 synth.py --root "$SYN" --out "$OUT" --lib subvt --synlib "$TT" --designs "$DESIGNS" || exit 1
python3 synth.py --root "$SYN" --out "$OUT" --lib hd --synlib "$OUT/libs/hd13_tt_025C_1v80.lib" --designs "$DESIGNS" || exit 1
python3 sta.py --sta "$STA" --out "$OUT" --lib subvt --libdir "$LIBDIR" --designs "$DESIGNS" > "$OUT/sta_subvt.txt" || exit 1
python3 sta.py --sta "$STA" --out "$OUT" --lib hd --hdlib "$OUT/libs/hd13_tt_025C_1v80.lib" --designs "$DESIGNS" > "$OUT/sta_hd.txt" || exit 1
python3 report.py --out "$OUT" --designs "$DESIGNS"
