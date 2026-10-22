drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/NAND2X1/layout
load nand2x1

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
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xna w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 3.905um 0.235um 3.905um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xnb w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 0.605um 2.58um 0.605um 2.58um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpa w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 4.225um 2.58um 4.225um 2.58um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpb w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# rails
rect metal1 0 -0.24 7.36 0.24
rect metal1 0 3.84 7.36 4.32

# taps
rect psubstratepdiff    0.18 -0.145 7.18 0.145
rect psubstratepcontact 0.30 -0.085 7.06 0.085
rect locali             0.21 -0.165 7.15 0.165
rect viali              0.30 -0.085 7.06 0.085
rect nsubstratendiff    0.18 3.935 7.18 4.225
rect nsubstratencontact 0.30 3.995 7.06 4.165
rect locali             0.21 3.915 7.15 4.245
rect viali              0.30 3.995 7.06 4.165

# nwell
rect nwell -0.23 1.87 7.59 4.41

# gnd
foreach xc {4.53 5.49 6.45} {
    rect metal1 [expr {$xc-0.115}] 0.20 [expr {$xc+0.115}] 0.60
}

# net1
foreach xc {0.43 1.39 2.35 3.31 4.05 5.01 5.97 6.93} {
    rect metal1 [expr {$xc-0.115}] 1.25 [expr {$xc+0.115}] 1.69
}
rect metal1 0.315 1.54 7.045 1.69

# vdd
rect metal1 1.285 3.25 1.455 3.90
rect metal1 4.905 3.25 5.075 3.90

# a
rect polysilicon 0.595 1.44 3.145 1.65
rect polysilicon 0.985 1.65 1.315 2.19
rect polysilicon 1.075 2.19 1.225 2.95
rect pcontact    1.065 1.94 1.235 2.11
rect locali      0.985 1.93 1.315 2.12
rect viali       1.065 1.94 1.235 2.11
rect metal1      1.00  1.87 1.30  2.19

# b
rect polysilicon 4.215 1.44 6.765 1.65
rect polysilicon 4.605 1.65 4.935 2.19
rect polysilicon 4.695 2.19 4.845 2.95
rect pcontact    4.685 1.94 4.855 2.11
rect locali      4.605 1.93 4.935 2.12
rect viali       4.685 1.94 4.855 2.11
rect metal1      4.62  1.87 4.92  2.19

# y
foreach xc {0.91 1.87 2.83} {
    rect m2contact [expr {$xc-0.13}] 1.07 [expr {$xc+0.13}] 1.33
    rect m2contact [expr {$xc-0.13}] 2.40 [expr {$xc+0.13}] 2.66
    rect metal1 [expr {$xc-0.19}] 1.01 [expr {$xc+0.19}] 1.39
    rect metal2 [expr {$xc-0.19}] 1.01 [expr {$xc+0.19}] 2.74
}
rect metal2 0.72 1.01 1.11 3.26
rect metal1 0.72 2.34 4.73 2.72
rect m2contact 0.79 2.94 1.05 3.20
rect metal1 0.74 2.88 1.10 3.26
rect m2contact 4.41 2.40 4.67 2.66
rect m2contact 4.41 2.94 4.67 3.20
rect metal1 4.36 2.88 4.72 3.26
rect metal2 4.34 2.34 4.73 3.26

# pins
pin A   1.00 1.87 1.30 2.19
pin B   4.62 1.87 4.92 2.19
pin Y   1.20 2.42 1.60 2.66
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 736 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
