#!/bin/bash
set -u
CELL="${1:-}"
shift || true
if [ -z "$CELL" ] || [ $# -lt 4 ] || [ $(( $# % 4 )) -ne 0 ]; then
  echo "usage: bash verify_cell.sh <cell> Wn Wp Ln Lp [Wn Wp Ln Lp ...]"
  exit 1
fi
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
export SUBVT_CELL="$CELL"
MCN="${MCN:-50}"
workdir "verify_$CELL"
echo "method,Wn_um,Wp_um,Ln_um,Lp_um" > verify_designs.csv
while [ $# -ge 4 ]; do echo "given,$1,$2,$3,$4" >> verify_designs.csv; shift 4; done
rm -f .done_*
step pvt python3 "$HERE/subvt_dataset.py" --mode pvt --source verify_designs.csv --select all --conds full15 --workers "$W" --resume --csv verify_full.csv
step mc python3 "$HERE/subvt_dataset.py" --mode mc --source verify_designs.csv --select all --conds critical --mc-n "$MCN" --workers "$W" --resume --csv mc_samples.csv
step build python3 "$HERE/build_dataset.py" --dir . --conds critical
step final python3 "$HERE/finalists.py" --dir .
date > RUN_DONE.txt
echo "== done: $OUT/finalists_report.csv"
