#!/bin/bash
# One entry point for every stage of the flow. Run inside the iic-osic-tools container after
# sak-pdk sky130A, from anywhere:  bash flow.sh <stage> [arguments]
#
#   sizing <cell> | sizing seq <dlx4|dffx4>   transistor sizing (part of the schematic stage)
#   schematic [CELL ...]                      export netlists from the xschem schematics
#   layout [CELL ...]                         generate the Magic layout scripts
#   verify [CELL ...]                         layout, DRC, LEF/GDS, LVS, PEX
#   char [corners|all] [cells|all]            characterisation, libraries, datasheets
#   synth [designs]                           synthesis + checks of rca8, counter8, demo
#   bench [designs]                           timing, power and report for those designs
#   riscv-synth [cores]                       synthesis + checks of the four RISC-V cores
#   riscv-bench [cores]                       timing, power, energy and PVT of the cores

set -u
ROOT=$(cd "$(dirname "$0")" && pwd)
S=$ROOT/scripts
stage=${1:-}
[ $# -gt 0 ] && shift
case "$stage" in
  sizing)
    if [ "${1:-}" = seq ]; then shift; exec bash "$S/schematic/sizing/run_seq.sh" "$@"; fi
    exec bash "$S/schematic/sizing/run_cell.sh" "$@" ;;
  schematic)   exec bash "$S/schematic/netlist.sh" "$@" ;;
  layout)      exec python3 "$S/layout/gen_layouts.py" "$ROOT/cells" "$@" ;;
  verify)      exec bash "$S/verification/verify_layouts.sh" "$@" ;;
  char)        exec bash "$S/characterization/run_char.sh" "$@" ;;
  synth)       exec bash "$S/synthesis/run_synth.sh" "$@" ;;
  bench)       exec bash "$S/benchmark/run_benchmark.sh" "$@" ;;
  riscv-synth) exec bash "$S/synthesis/run_riscv.sh" "$@" ;;
  riscv-bench) exec bash "$S/benchmark/run_riscv_benchmark.sh" "$@" ;;
  *)
    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
    [ -z "$stage" ] && exit 0 || exit 1 ;;
esac
