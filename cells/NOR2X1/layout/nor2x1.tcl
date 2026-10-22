drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/NOR2X1/layout
load nor2x1

set portErrors {}

proc rect {layer x1 y1 x2 y2} {
    box [format %.3f $x1]um [format %.3f $y1]um [format %.3f $x2]um [format %.3f $y2]um
    paint $layer
}
proc pin {name x1 y1 x2 y2} {
    global portErrors
    box [format %.3f $x1]um [format %.3f $y1]um [format %.3f $x2]um [format %.3f $y2]um
    label $name c metal1
    select area labels
    if {[catch {port make} msg]} { lappend portErrors "$name: $msg" }
    select clear
}

# devices
box 0.285um 0.235um 0.285um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xnb w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 2.585um 0.235um 2.585um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xna w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 0.605um 2.37um 0.605um 2.37um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpb w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 2.905um 2.37um 2.905um 2.37um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpa w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# rails
rect metal1 0 -0.24 4.60 0.24
rect metal1 0 3.84 4.60 4.32

# taps
rect psubstratepdiff    0.18 -0.145 4.42 0.145
rect psubstratepcontact 0.30 -0.085 4.30 0.085
rect locali             0.21 -0.165 4.39 0.165
rect viali              0.30 -0.085 4.30 0.085
rect nsubstratendiff    0.18 3.935 4.42 4.225
rect nsubstratencontact 0.30 3.995 4.30 4.165
rect locali             0.21 3.915 4.39 4.245
rect viali              0.30 3.995 4.30 4.165

# nwell
rect nwell -0.23 1.87 4.83 4.41

# gnd
foreach xc {0.43 1.39 2.73 3.69} {
    rect metal1 [expr {$xc-0.115}] 0.20 [expr {$xc+0.115}] 0.60
}

# vdd
rect metal1 3.585 3.40 3.755 3.90

# net1
rect metal1 1.255 3.00 3.345 3.20

# b
rect polysilicon 0.595 1.44 1.705 1.59
rect polysilicon 0.985 1.59 1.315 1.92
rect polysilicon 1.075 1.92 1.225 2.80
rect pcontact    1.065 1.67 1.235 1.84
rect locali      0.985 1.66 1.315 1.85
rect viali       1.065 1.67 1.235 1.84
rect metal1      1.00  1.60 1.30  1.92

# a
rect polysilicon 2.895 1.44 4.005 1.59
rect polysilicon 3.285 1.59 3.615 1.92
rect polysilicon 3.375 1.92 3.525 2.80
rect pcontact    3.365 1.67 3.535 1.84
rect locali      3.285 1.66 3.615 1.85
rect viali       3.365 1.67 3.535 1.84
rect metal1      3.30  1.60 3.60  1.92

# y
foreach xc {0.91 1.87 3.21 4.17} {
    rect m2contact [expr {$xc-0.13}] 1.07 [expr {$xc+0.13}] 1.33
    rect m2contact [expr {$xc-0.13}] 2.20 [expr {$xc+0.13}] 2.46
    rect metal1 [expr {$xc-0.19}] 1.01 [expr {$xc+0.19}] 1.39
    rect metal2 [expr {$xc-0.19}] 1.01 [expr {$xc+0.19}] 2.52
}
rect metal1 0.72 2.14 4.36 2.52
rect metal1 0.815 2.40 1.045 2.80

# pins
pin B   1.00 1.60 1.30 1.92
pin A   3.30 1.60 3.60 1.92
pin Y   2.20 2.20 2.60 2.46
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 460 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
