#!/bin/bash
# Export the netlist of every cell from its xschem schematic:
# cells/<CELL>/schematic/<cell>.sch -> cells/<CELL>/spice/<cell>.spice
# The top level is written as a .subckt, then netlist_clean.py reduces each device line to
# W, L and nf so layout generation, LVS and sizing all read the same simple format.
# Usage: bash netlist.sh [CELL ...]   (default: all 13 cells)

set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
RC=${XSCHEMRC:-$PDK_ROOT/${PDK:-sky130A}/libs.tech/xschem/xschemrc}
ALL="INV1X4 NAND2X4 NOR2X4 AND2X4 OR2X4 AOI3X4 OAI3X4 XOR2X4 XNOR2X4 MAOI4X4 MOAI4X4 DLX4 DFFX4"
CELLS=${@:-$ALL}
command -v xschem >/dev/null || { echo "xschem not found"; exit 1; }
[ -f "$RC" ] || { echo "xschemrc not found: $RC (run sak-pdk sky130A first)"; exit 1; }
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0
for C in $CELLS; do
  C=${C^^}; c=${C,,}
  SCH=$ROOT/cells/$C/schematic/$c.sch
  OUT=$ROOT/cells/$C/spice/$c.spice
  [ -f "$SCH" ] || { echo "$C: missing $SCH"; fail=1; continue; }
  # -q quit when done, -x no window, -n netlist, -s spice; lvs_netlist/top_subckt write the top
  # level as a .subckt with *.PININFO, the form netgen and the rest of the flow expect
  xschem -q -x -n -s --rcfile "$RC" --tcl "set lvs_netlist 1; set top_subckt 1" -o "$TMP" -N "$c.spice" "$SCH" > "$TMP/$c.log" 2>&1
  if [ ! -s "$TMP/$c.spice" ]; then
    echo "$C: xschem produced no netlist"; tail -n 5 "$TMP/$c.log"; fail=1; continue
  fi
  mkdir -p "$(dirname "$OUT")"
  python3 "$HERE/netlist_clean.py" "$TMP/$c.spice" "$OUT" || { echo "$C: netlist check failed"; fail=1; continue; }
done
exit $fail
