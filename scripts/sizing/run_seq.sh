#!/bin/bash
set -u
CELL="${1:-}"
case "$CELL" in dlx4|dffx4) ;; *) echo "usage: bash run_seq.sh <dlx4|dffx4>"; exit 1 ;; esac
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
export SUBVT_SEQ_CELL="$CELL" SUBVT_SEQ_LOAD="${SUBVT_SEQ_LOAD:-inv}"
NA="${NA:-48}"
NB="${NB:-16}"
workdir "$CELL"
step stage_a python3 "$HERE/subvt_seq.py" --mode stage-a --n "$NA" --conds critical --workers "$W" --csv stage_a.csv
step sum_a python3 "$HERE/seq_report.py" stage_a.csv --out stage_a_summary.csv
step loops python3 -c "import pandas as pd; s = pd.read_csv('stage_a_summary.csv'); s = s[s['pass']]; s.to_csv('loops.csv', index=False); print(len(s), 'loop designs pass'); raise SystemExit(0 if len(s) else 1)"
step stage_b python3 "$HERE/subvt_seq.py" --mode stage-b --source loops.csv --n "$NB" --conds critical --cycles 3 --workers "$W" --csv stage_b.csv
step sum_b python3 "$HERE/seq_report.py" stage_b.csv --out stage_b_summary.csv
date > RUN_DONE.txt
echo "== done: $OUT/stage_b_summary.csv; verify a pick with verify_seq.sh $CELL Win Lin Wfb Lfb kclk kout kqb"
