#!/usr/bin/env bash
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
LIB=${LIB:-$ROOT/lib/subvt_sky130_tt_0p40v_27c.lib}
OUT=${OUT:-/tmp/subvt_examples/synth}
[ -f "$LIB" ] || { echo "ERROR: liberty not found: $LIB   (set LIB=...)"; exit 2; }
rm -rf "$OUT"; mkdir -p "$OUT"
rc=0
for t in rca8 counter8 demo; do
  mkdir -p "$OUT/$t"
  if LIB="$LIB" bash "$HERE/run_synth.sh" "$ROOT/synthesis/rtl/$t.v" "$t" > "$OUT/$t/coverage.txt" 2>&1; then
    cp /tmp/subvt_synth/stat.txt "/tmp/subvt_synth/${t}_gate.v" /tmp/subvt_synth/synth.log "$OUT/$t/"
    echo "=== $t"
    grep -E "cells|Chip area" "$OUT/$t/stat.txt"
    tail -n 3 "$OUT/$t/coverage.txt"
  else
    echo "=== $t FAILED"; tail -n 15 "$OUT/$t/coverage.txt"; rc=1
  fi
done
echo; echo "Results in $OUT"
exit $rc
