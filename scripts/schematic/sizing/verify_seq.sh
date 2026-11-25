#!/bin/bash
# Check one sizing of DLX4/DFFX4: 15-corner PVT, Monte Carlo, and setup/hold times.
# Usage: bash verify_seq.sh <dlx4|dffx4> Win Lin Wfb Lfb kclk kout kqb
# Win/Lin: input transmission gate, Wfb/Lfb: feedback gate, kclk/kout/kqb: clock, Q and QB
# inverters as multiples of the reference inverter.

set -u
CELL="${1:-}"
shift || true
case "$CELL" in dlx4|dffx4) ;; *) CELL="" ;; esac
if [ -z "$CELL" ] || [ $# -ne 7 ]; then
  echo "usage: bash verify_seq.sh <dlx4|dffx4> Win Lin Wfb Lfb kclk kout kqb"
  exit 1
fi
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
export SUBVT_SEQ_CELL="$CELL" SUBVT_SEQ_LOAD="${SUBVT_SEQ_LOAD:-inv}"
MCN="${MCN:-50}"
workdir "verify_$CELL"
echo "Win_um,Lin_um,Wfb_um,Lfb_um,kclk,kout,kqb" > design.csv
echo "$1,$2,$3,$4,$5,$6,$7" >> design.csv
rm -f .done_*
step pvt python3 "$HERE/subvt_seq.py" --mode pvt --source design.csv --conds full15 --cycles 5 --workers "$W" --csv verify15.csv
step mc python3 "$HERE/subvt_seq.py" --mode mc --source design.csv --conds critical --mc-n "$MCN" --workers "$W" --csv mc.csv
step report python3 "$HERE/seq_report.py" verify15.csv --mc mc.csv --out final_summary.csv
step sh python3 "$HERE/subvt_seq.py" --mode setup-hold --source design.csv --conds critical --workers "$W" --csv setup_hold.csv
date > RUN_DONE.txt
echo "== done: $OUT/final_summary.csv, $OUT/setup_hold.csv"
