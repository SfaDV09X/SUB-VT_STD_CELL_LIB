#!/bin/bash
# Full sizing run for one combinational cell, results in sizing_work/<cell>/.
# Usage: bash run_cell.sh <cell>   (WORKERS, NSWEEP, MCN override the defaults)
# Pipeline: random sweep -> dataset -> feasibility -> GPR fit -> Bayesian optimisation
# -> pick designs -> 15-corner PVT and Monte Carlo check -> finalists report.

set -u
CELL="${1:-}"
[ -n "$CELL" ] || { echo "usage: bash run_cell.sh <inv1x4|nand2x4|nor2x4|and2x4|or2x4|and2x4_out|or2x4_out|xor2x4|xnor2x4|aoi3x4|oai3x4|maoi4x4|moai4x4>"; exit 1; }
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
export SUBVT_CELL="$CELL"
NSWEEP="${NSWEEP:-96}"
MCN="${MCN:-50}"
workdir "$CELL"
step sweep python3 "$HERE/subvt_dataset.py" --mode sweep --n "$NSWEEP" --conds critical --workers "$W" --resume --csv sweep.csv
step build python3 "$HERE/build_dataset.py" --dir . --conds critical
step feas python3 "$HERE/check_feasibility.py" --dir .
step fit python3 "$HERE/fit_gpr.py" --dir . --in-box --folds 5
step opt python3 "$HERE/optimize.py" --dir . --seeds 3 --budget 50 --n0 15 --workers "$W"
step pick python3 "$HERE/optimize.py" --dir . --mode verify --n-verify 3
step pvt python3 "$HERE/subvt_dataset.py" --mode pvt --source verify_designs.csv --select all --conds full15 --workers "$W" --resume --csv verify_full.csv
step mc python3 "$HERE/subvt_dataset.py" --mode mc --source verify_designs.csv --select all --conds critical --mc-n "$MCN" --workers "$W" --resume --csv mc_samples.csv
# Rebuild the dataset with the verification runs added, then rank the finalists.
rm -f .done_build
step build2 python3 "$HERE/build_dataset.py" --dir . --conds critical
step final python3 "$HERE/finalists.py" --dir .
date > RUN_DONE.txt
echo "== done: $OUT/finalists_report.csv"
