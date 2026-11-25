#!/bin/bash
# Physical verification of the cells in one go: for each cell build the layout from
# layout/<cell>.tcl in Magic, run DRC, write LEF and GDS, extract for LVS and PEX,
# run netgen LVS, then collect one summary line per cell in cells/verification_summary.txt.
# Usage: bash verify_layouts.sh [CELL ...]   (default: all 13 cells)

ROOT=${ROOT:-/foss/designs/SUB-VT_STD_CELL_LIB}
VS=$ROOT/scripts/verification
RC=${MAGICRC:-$PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc}
ALL="INV1X4 NAND2X4 NOR2X4 AND2X4 OR2X4 AOI3X4 OAI3X4 XOR2X4 XNOR2X4 MAOI4X4 MOAI4X4 DLX4 DFFX4"
CELLS=${@:-$ALL}
SUM=$ROOT/cells/verification_summary.txt
printf "%-9s %-8s %-6s %-26s %-6s %-6s %s\n" CELL WIDTH DRC LVS R C PORTS > $SUM
for C in $CELLS; do
  C=${C^^}; c=${C,,}
  L=$ROOT/cells/$C/layout
  V=$ROOT/cells/$C/verification
  mkdir -p $V/drc $V/lvs $V/pex
  [ -f $L/$c.tcl ] || { echo "missing $L/$c.tcl"; continue; }
  # Start from scratch so stale views never survive a failed run.
  rm -f $L/$c.mag $L/$c.ext $L/$c.lef $L/$c.gds
  echo "=== $C"
  # One Magic batch script per cell, deleted again after the run.
  cat > $L/run_all.tcl <<TCL
set cell $c
source $L/$c.tcl
source $VS/drc.tcl
load $c
lef write
gds write $c
source $VS/lvs.tcl
source $VS/pex.tcl
quit -noprompt
TCL
  (cd $L && magic -dnull -noconsole -rcfile $RC $L/run_all.tcl > $L/run_all.log 2>&1)
  rm -f $L/run_all.tcl
  bash $VS/lvs.sh $c > /dev/null 2>&1
  # Pull the numbers for the summary out of the reports and the Magic log.
  W=$(grep -oP 'SIZE\s+\K[0-9.]+' $L/$c.lef 2>/dev/null)
  D=$(grep -oP 'total error boxes: \K[0-9]+' $V/drc/${c}_drc.rpt 2>/dev/null)
  LV=$(grep -m1 "Final result" $V/lvs/${c}_comp.out 2>/dev/null | sed 's/Final result: //')
  R=$(grep -oP 'R_elements: \K[0-9]+' $V/pex/${c}_pex.rpt 2>/dev/null)
  CC=$(grep -oP 'C_elements: \K[0-9]+' $V/pex/${c}_pex.rpt 2>/dev/null)
  P=$(grep -q "PORT ERROR" $L/run_all.log && echo ERR || echo ok)
  printf "%-9s %-8s %-6s %-26s %-6s %-6s %s\n" "$C" "${W:-?}" "${D:-?}" "${LV:-?}" "${R:-?}" "${CC:-?}" "$P" | tee -a $SUM
done
echo "summary: $SUM"
