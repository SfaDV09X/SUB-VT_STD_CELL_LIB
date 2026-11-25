# Shared setup sourced by the run_*/verify_* sizing scripts: repo paths, worker count,
# ngspice settings for the sky130 models, missing Python packages, and two helpers.

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
export SUBVT_BASE_DIR="${SUBVT_BASE_DIR:-$ROOT}"
W="${WORKERS:-8}"
command -v ngspice >/dev/null || { echo "ngspice not found"; exit 1; }
# ngspice needs these options to read the sky130 model files; add them once.
grep -q ngbehavior ~/.spiceinit 2>/dev/null || printf 'set ngbehavior=hsa\nset ng_nomodcheck\nset skywaterpdk\nset num_threads=1\n' >> ~/.spiceinit
python3 - <<'P' || exit 1
import importlib.util, subprocess, sys
need = {"numpy": "numpy", "pandas": "pandas", "scipy": "scipy", "sklearn": "scikit-learn", "matplotlib": "matplotlib", "pymoo": "pymoo"}
miss = [p for m, p in need.items() if importlib.util.find_spec(m) is None]
if miss:
    print("installing", miss)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-q"] + miss)
P
# step NAME CMD...: run one pipeline step with its output in log_NAME.txt.
# A finished step leaves .done_NAME, so rerunning the pipeline resumes where it stopped.
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
# workdir NAME: create and enter sizing_work/NAME, send simulator files to sim/ and
# copy everything printed to pipeline.log.
workdir() {
  OUT="$ROOT/sizing_work/$1"
  mkdir -p "$OUT/sim"
  cd "$OUT" || exit 1
  export SUBVT_OUT_DIR="$OUT/sim"
  exec > >(tee -a "$OUT/pipeline.log") 2>&1
  rm -f FAILED.txt RUN_DONE.txt
  echo "== $(date) $1 workers=$W"
}
