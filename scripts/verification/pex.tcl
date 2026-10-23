set subvt_root /foss/designs/SUB-VT_STD_CELL_LIB
set cellu [string toupper $cell]
cd $subvt_root/cells/$cellu/layout
load $cell
if {![info exists w]} {
    set lf [open $subvt_root/cells/$cellu/layout/${cell}.lef r]
    set lt [read $lf]
    close $lf
    if {![regexp {SIZE\s+([0-9.]+)\s+BY} $lt -> w]} { error "cannot read cell width from ${cell}.lef (or set w)" }
}
box 0um 0um ${w}um 4.08um

extract do local
extract do capacitance
extract do coupling
extract all

ext2sim labels on
ext2sim

extresist threshold 0
extresist minresist 0
extresist extout on
extresist all

ext2spice format ngspice
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice rthresh 0
ext2spice extresist on
ext2spice -o $subvt_root/cells/$cellu/verification/pex/${cell}_pex.spice

file delete -force ${cell}.sim ${cell}.nodes ${cell}.res.ext

catch {clear}
set f [open $subvt_root/cells/$cellu/verification/pex/${cell}_pex.spice r]
set d [read $f]
close $f
set nR 0
set nC 0
foreach l [split $d "\n"] {
    if {[string match "R*" $l]} {incr nR}
    if {[string match "C*" $l]} {incr nC}
}
puts "R elements: $nR"
puts "C elements: $nC"

set f [open $subvt_root/cells/$cellu/verification/pex/${cell}_pex.rpt w]
puts $f "# PEX report (R+C extraction): $cell"
puts $f "width_um: $w"
puts $f "R_elements: $nR"
puts $f "C_elements: $nC"
close $f
