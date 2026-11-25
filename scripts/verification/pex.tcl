# Magic: full R+C parasitic extraction of the cell into verification/pex/<cell>_pex.spice
# and a short count report <cell>_pex.rpt. Expects `cell` to be set (and the LEF written,
# which is where the cell width comes from unless `w` is given).

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

# Capacitance including coupling between wires.
extract do local
extract do capacitance
extract do coupling
extract all

# extresist needs the .sim/.nodes files, then adds wire resistance for every net.
ext2sim labels on
ext2sim

extresist threshold 0
extresist minres 0
extresist mindelay 0
extresist extout on
extresist all

# Flat ngspice subcircuit with every R and C kept (thresholds 0).
ext2spice format ngspice
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice rthresh 0
ext2spice extresist on
ext2spice -o $subvt_root/cells/$cellu/verification/pex/${cell}_pex.spice

file delete -force ${cell}.sim ${cell}.nodes ${cell}.res.ext

# Count the R and C elements for the summary.
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
