# DRC of one cell -> cells/<CELL>/verification/drc/<cell>_drc.rpt
# usage (Magic):  set cell inv1x1 ; source /foss/designs/SUB-VT_STD_CELL_LIB/scripts/verification/drc.tcl
set subvt_root /foss/designs/SUB-VT_STD_CELL_LIB
set cellu [string toupper $cell]
cd $subvt_root/cells/$cellu/layout
load $cell
drc on
drc catchup
set errs [drc listall why]
set body ""
set nboxes 0
foreach {rule boxes} $errs {
    append body "$rule\n"
    foreach b $boxes {
        lassign $b x1 y1 x2 y2
        append body [format "  %.3f %.3f %.3f %.3f\n" [expr {$x1*0.005}] [expr {$y1*0.005}] [expr {$x2*0.005}] [expr {$y2*0.005}]]
        incr nboxes
    }
}
if {$body eq ""} { set body "none\n" }
set out "# DRC report: $cell\n# total error boxes: $nboxes\n# coordinates in um: llx lly urx ury\n$body"
set f [open $subvt_root/cells/$cellu/verification/drc/${cell}_drc.rpt w]
puts -nonewline $f $out
close $f

# console report
catch {clear}
drc count total
puts "DRC errors (um: llx lly urx ury):"
puts -nonewline $body
