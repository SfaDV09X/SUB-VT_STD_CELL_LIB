#!/bin/bash
# Benchmark stage for the RISC-V cores: Fmax, power, energy per cycle and per instruction for
# every workload with OpenSTA (X4 at tt 27 C, sky130_fd_sc_hd at tt 25 C / 1.8 V), the result
# tables, then the 15-corner PVT sweep for X4. Reads the netlists and activity written by
# synthesis/run_riscv.sh; results in benchmarking/out/.
# Usage: bash run_riscv_benchmark.sh [cores]   (run synthesis/run_riscv.sh with the same cores first)

set -u -o pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
X4_LIB=${X4_LIB:-$ROOT/lib/tt_27c/subvt_sky130_tt_0p40v_27c.lib}
OUT=${OUT:-$ROOT/benchmarking/out}
CORES=${1:-serv,femto,pico,dark}
HD13=$OUT/libs/hd13_tt_025C_1v80.lib
command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }
STA=${STA:-$(command -v sta || command -v openroad)}
[ -n "$STA" ] || { echo "neither sta nor openroad found"; exit 1; }
[ -f "$X4_LIB" ] || { echo "X4 library not found: $X4_LIB"; exit 1; }
[ -f "$HD13" ] || { echo "$HD13 not found: run scripts/synthesis/run_riscv.sh first"; exit 1; }
for c in ${CORES//,/ }; do
  for l in x4 hd; do
    [ -f "$OUT/$l/$c/result.json" ] || { echo "no synthesis result for $l/$c: run scripts/synthesis/run_riscv.sh $CORES"; exit 1; }
  done
done
cd "$HERE" || exit 1
python3 riscv_sta.py --sta "$STA" --out "$OUT" --lib x4 --stalib "$X4_LIB" --cores "$CORES" | tee "$OUT/sta_x4.txt" || exit 1
python3 riscv_sta.py --sta "$STA" --out "$OUT" --lib hd --stalib "$HD13" --cores "$CORES" | tee "$OUT/sta_hd.txt" || exit 1
python3 riscv_report.py --out "$OUT"
# PVT reuses the tt 27 C netlists and activity with the other 14 corner libraries.
LIBDIR=$(dirname "$(dirname "$X4_LIB")")
python3 riscv_pvt.py --sta "$STA" --out "$OUT" --libdir "$LIBDIR" --cores "$CORES" | tee "$OUT/pvt_x4.txt"
