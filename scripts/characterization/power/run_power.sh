#!/bin/bash
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
OUT=${OUT:-$REPO/../power_out}
MODEL=$PDK_ROOT/$PDK/libs.tech/ngspice/sky130.lib.spice
[ -f "$MODEL" ] || { echo "missing $MODEL"; exit 1; }
command -v ngspice >/dev/null || { echo "ngspice not found"; exit 1; }
cd "$HERE" || exit 1
case "${1:-}" in
  cell)
    [ -n "${2:-}" ] || { echo "usage: run_power.sh cell <name>"; exit 1; }
    rm -rf "$OUT/meas/$2"
    python3 measure.py --repo "$REPO" --out "$OUT/meas/$2" --models "$MODEL" --cells "$2" ;;
  build)
    rm -rf "$OUT/patched"
    python3 apply.py --repo "$REPO" --meas "$OUT/meas" --out "$OUT/patched" | tee "$OUT/patched_summary.txt" ;;
  *) echo "usage: run_power.sh cell <name>|build"; exit 1 ;;
esac
