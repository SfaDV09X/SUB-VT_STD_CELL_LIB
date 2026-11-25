#!/bin/bash
# Synthesis stage for the RISC-V benchmark: SERV, FemtoRV32 Quark, PicoRV32 and DarkRISCV
# synthesised on the X4 library (0.40 V) and on the matching sky130_fd_sc_hd cells (1.8 V),
# fanout-buffered, and verified on 5 workloads (RTL and gate level against the ISS).
# Netlists and switching activity go to benchmarking/out/<lib>/<core>/;
# benchmark/run_riscv_benchmark.sh does timing, power, energy and PVT from there.
# Usage: bash run_riscv.sh [cores]   e.g. bash run_riscv.sh serv,pico

set -u -o pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
SRC=$ROOT/benchmarking
X4_LIB=${X4_LIB:-$ROOT/lib/tt_27c/subvt_sky130_tt_0p40v_27c.lib}
HD_LIB=${HD_LIB:-${PDK_ROOT:-/foss/pdks}/${PDK:-sky130A}/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib}
OUT=${OUT:-$ROOT/benchmarking/out}
CORES=${1:-serv,femto,pico,dark}
for t in yosys iverilog vvp python3; do command -v $t >/dev/null || { echo "$t not found"; exit 1; }; done
[ -f "$X4_LIB" ] || { echo "X4 library not found: $X4_LIB"; exit 1; }
[ -f "$HD_LIB" ] || { echo "sky130_fd_sc_hd liberty not found: $HD_LIB"; exit 1; }
mkdir -p "$OUT/libs"
cd "$HERE" || exit 1
python3 -c "import libs; libs.subset('$HD_LIB', '$OUT/libs/hd13_tt_025C_1v80.lib', libs.cell_names(libs.HD))" || exit 1
python3 riscv.py --root "$SRC" --out "$OUT" --lib x4 --synlib "$X4_LIB" --cores "$CORES" | tee "$OUT/flow_x4.txt" || exit 1
python3 riscv.py --root "$SRC" --out "$OUT" --lib hd --synlib "$OUT/libs/hd13_tt_025C_1v80.lib" --cores "$CORES" | tee "$OUT/flow_hd.txt" || exit 1
