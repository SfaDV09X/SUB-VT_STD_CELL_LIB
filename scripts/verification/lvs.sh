#!/bin/bash
# Netgen LVS of one cell: extracted layout netlist vs schematic netlist.
# usage: scripts/verification/lvs.sh <cell>      (lowercase, e.g. inv1x1)
# Run scripts/verification/lvs.tcl in Magic first (writes cells/<CELL>/verification/lvs/<cell>_layout.spice).
cell=${1:?usage: lvs.sh <cell>}
ROOT=${ROOT:-/foss/designs/SUB-VT_STD_CELL_LIB}
CELLDIR=$ROOT/cells/${cell^^}
cd "$CELLDIR/verification/lvs" || exit 1
netgen -batch lvs "${cell}_layout.spice ${cell}" "$CELLDIR/spice/${cell}.spice ${cell}" $PDK_ROOT/sky130A/libs.tech/netgen/sky130A_setup.tcl ${cell}_comp.out > /dev/null
{ echo "# LVS report: ${cell} (summary lines of ${cell}_comp.out; full netgen output in ${cell}_comp.out)"; grep -iE "final result|mismatch|do not match|property" ${cell}_comp.out; } | tee ${cell}_lvs.rpt
