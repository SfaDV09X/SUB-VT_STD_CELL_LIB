HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
export SUBVT_BASE_DIR="${SUBVT_BASE_DIR:-$ROOT}"
W="${WORKERS:-8}"
command -v ngspice >/dev/null || { echo "ngspice not found"; exit 1; }
grep -q ngbehavior ~/.spiceinit 2>/dev/null || printf 'set ngbehavior=hsa\nset ng_nomodcheck\nset skywaterpdk\nset num_threads=1\n' >> ~/.spiceinit
python3 - <<'P' || exit 1
import importlib.util, subprocess, sys
need = {"numpy": "numpy", "pandas": "pandas", "scipy": "scipy", "sklearn": "scikit-learn", "matplotlib": "matplotlib", "pymoo": "pymoo"}
miss = [p for m, p in need.items() if importlib.util.find_spec(m) is None]
if miss:
    print("installing", miss)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-q"] + miss)
P
step() {
  name="$1"; shift
  if [ -f ".done_$name" ]; then echo "-- skip $name"; return 0; fi
  echo "-- $name: $*"
  "$@" > "log_$name.txt" 2>&1
  rc=$?
  tail -n 3 "log_$name.txt"
  if [ $rc -ne 0 ]; then echo "FAILED: $name (see $PWD/log_$name.txt)"; echo "$name" > FAILED.txt; exit $rc; fi
  touch ".done_$name"
}
workdir() {
  OUT="$ROOT/sizing_work/$1"
  mkdir -p "$OUT/sim"
  cd "$OUT" || exit 1
  export SUBVT_OUT_DIR="$OUT/sim"
  exec > >(tee -a "$OUT/pipeline.log") 2>&1
  rm -f FAILED.txt RUN_DONE.txt
  echo "== $(date) $1 workers=$W"
}
