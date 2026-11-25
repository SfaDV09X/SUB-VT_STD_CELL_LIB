#!/bin/bash
# Benchmark stage for the small designs: OpenSTA timing and power of the netlists from
# synthesis/run_synth.sh, at all 15 corners for our library and tt 25 C / 1.8 V for
# sky130_fd_sc_hd, then the HTML/csv report in synthesis/out/report.
# Usage: bash run_benchmark.sh [designs]   (run synthesis/run_synth.sh with the same designs first)

set -u -o pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
LIBDIR=${LIBDIR:-$ROOT/lib}
OUT=${OUT:-$ROOT/synthesis/out}
DESIGNS=${1:-rca8,counter8,demo}
HD13=$OUT/libs/hd13_tt_025C_1v80.lib
command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }
STA=${STA:-$(command -v sta || command -v openroad)}
[ -n "$STA" ] || { echo "neither sta nor openroad found"; exit 1; }
[ -f "$HD13" ] || { echo "$HD13 not found: run scripts/synthesis/run_synth.sh first"; exit 1; }
for d in ${DESIGNS//,/ }; do
  for l in subvt hd; do
    [ -f "$OUT/$l/$d/result.json" ] || { echo "no synthesis result for $l/$d: run scripts/synthesis/run_synth.sh $DESIGNS"; exit 1; }
  done
done
cd "$HERE" || exit 1
python3 sta.py --sta "$STA" --out "$OUT" --lib subvt --libdir "$LIBDIR" --designs "$DESIGNS" > "$OUT/sta_subvt.txt" || exit 1
python3 sta.py --sta "$STA" --out "$OUT" --lib hd --hdlib "$HD13" --designs "$DESIGNS" > "$OUT/sta_hd.txt" || exit 1
python3 report.py --out "$OUT" --designs "$DESIGNS"
