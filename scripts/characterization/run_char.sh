#!/bin/bash
# Characterise the whole library: every cell at every corner with lctime/ngspice on the PEX
# netlists, then build lib/<corner>/*.lib, the HTML datasheets and the per-cell grid files.
# Usage: bash run_char.sh [corners|all] [cells|all]   e.g. bash run_char.sh tt_27c inv1x4,nand2x4
# Rerunning skips corners whose library already exists. Work files: characterization_work/.

set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
MODELS=${MODELS:-$PDK_ROOT/${PDK:-sky130A}/libs.tech/combined/sky130.lib.spice}
JOBS=${JOBS:-$(nproc)}
CORNERS=${1:-all}
CELLS=${2:-all}
[ -f "$MODELS" ] || { echo "model library not found: $MODELS"; exit 1; }
command -v ngspice >/dev/null || { echo "ngspice not found"; exit 1; }
command -v lctime >/dev/null || pip install --user lctime || { echo "lctime not found"; exit 1; }
python3 -c "import numpy, liberty" || { echo "python packages numpy and liberty-parser are required"; exit 1; }
# ngspice compatibility options for the sky130 models, added once.
grep -q ngbehavior ~/.spiceinit 2>/dev/null || printf 'set ngbehavior=hsa\nset ng_nomodcheck\nset num_threads=1\n' >> ~/.spiceinit
mkdir -p "$ROOT/characterization_work"
python3 "$HERE/charflow.py" --cells-dir "$ROOT/cells" --models "$MODELS" --work "$ROOT/characterization_work" \
  --libdir "$ROOT/lib" --corners "$CORNERS" --cells "$CELLS" --jobs "$JOBS" 2>&1 | tee -a "$ROOT/characterization_work/run.log"
[ "${PIPESTATUS[0]}" -eq 0 ] || exit 1
python3 "$HERE/datasheet.py" --libdir "$ROOT/lib" --out "$ROOT/datasheets"
python3 "$HERE/grids.py" "$ROOT/cells"
