#!/bin/bash
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
fmt() { local s=$1; printf "%dh%02dm" $((s / 3600)) $(((s % 3600) / 60)); }
now=$(date +%s)
for d in "$ROOT"/sizing_work/*/; do
  [ -d "$d" ] || continue
  d="${d%/}"
  echo "=== $(basename "$d")"
  [ -f "$d/RUN_DONE.txt" ] && echo "finished: $(cat "$d/RUN_DONE.txt")"
  [ -f "$d/FAILED.txt" ] && echo "FAILED step: $(cat "$d/FAILED.txt")  (see log_$(cat "$d/FAILED.txt").txt)"
  echo "steps done: $(ls -a "$d" | sed -n 's/^\.done_//p' | tr '\n' ' ')"
  for pair in sweep:sweep.csv pvt:verify_full.csv mc:mc_samples.csv; do
    step="${pair%%:*}"; csv="$d/${pair#*:}"; log="$d/log_$step.txt"
    [ -f "$log" ] || continue
    total=$(grep -m1 -oE '^[0-9]+ (Monte Carlo runs )?requested' "$log" | grep -oE '^[0-9]+')
    [ -z "$total" ] && total=$(grep -oE '\[[0-9]+/[0-9]+\]' "$log" | tail -n 1 | grep -oE '/[0-9]+' | tr -d /)
    rows=0
    [ -f "$csv" ] && rows=$(( $(wc -l < "$csv") - 1 ))
    [ "$rows" -lt 0 ] && rows=0
    if [ -f "$d/.done_$step" ]; then
      echo "  $step: done ($rows rows)"
      continue
    fi
    [ -z "$total" ] && { echo "  $step: starting"; continue; }
    done_n=$rows; [ "$done_n" -gt "$total" ] && done_n=$total
    pct=$(( 100 * done_n / total ))
    line="  $step: $done_n / $total ($pct %), $((total - done_n)) left"
    st="$d/.status_$step"
    if [ -f "$st" ]; then
      read t0 n0 < "$st"
      dt=$((now - t0)); dn=$((done_n - n0))
      if [ "$dt" -gt 0 ] && [ "$dn" -gt 0 ]; then
        eta=$(( (total - done_n) * dt / dn ))
        line="$line, rate $(( dn * 3600 / dt ))/h since $(fmt $dt) ago, about $(fmt $eta) to go"
        echo "$now $done_n" > "$st"
      elif [ "$dt" -gt 0 ]; then
        line="$line, no new rows in the last $(fmt $dt)"
      fi
    else
      echo "$now $done_n" > "$st"
      line="$line (run status.sh again later for rate and time left)"
    fi
    echo "$line"
    last=$(grep -E '^\[[0-9]+/[0-9]+\]' "$log" | tail -n 1)
    [ -n "$last" ] && echo "    last: ${last:0:110}"
  done
  if [ -f "$d/sweep.csv" ]; then
    python3 - "$d/sweep.csv" <<'P'
import sys, pandas as pd
try:
    t = pd.read_csv(sys.argv[1])
    print("  sweep status:", t.status.value_counts().to_dict())
except Exception:
    pass
P
  fi
  echo "  last log write: $(date -r "$d/pipeline.log" '+%H:%M:%S' 2>/dev/null)   now: $(date '+%H:%M:%S')"
done
