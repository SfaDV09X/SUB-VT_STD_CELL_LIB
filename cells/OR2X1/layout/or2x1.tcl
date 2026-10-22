drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/OR2X1/layout
load or2x1

set portErrors {}
set dx 4.60

proc rect {layer x1 y1 x2 y2} {
    box [format %.3f $x1]um [format %.3f $y1]um [format %.3f $x2]um [format %.3f $y2]um
    paint $layer
}
proc rectd {layer x1 y1 x2 y2} {
    global dx
    rect $layer [expr {$x1+$dx}] $y1 [expr {$x2+$dx}] $y2
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
box 4.885um 0.235um 4.885um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xni w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 5.205um 2.58um 5.205um 2.58um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpi w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# rails
rect metal1 0 -0.24 6.90 0.24
rect metal1 0 3.84 6.90 4.32

# taps
rect psubstratepdiff    0.18 -0.145 6.72 0.145
rect psubstratepcontact 0.30 -0.085 6.60 0.085
rect locali             0.21 -0.165 6.69 0.165
rect viali              0.30 -0.085 6.60 0.085
rect nsubstratendiff    0.18 3.935 6.72 4.225
rect nsubstratencontact 0.30 3.995 6.60 4.165
rect locali             0.21 3.915 6.69 4.245
rect viali              0.30 3.995 6.60 4.165

# nwell
rect nwell -0.23 1.87 7.13 4.41

# nor gnd
foreach xc {0.43 1.39 2.73 3.69} {
    rect metal1 [expr {$xc-0.115}] 0.20 [expr {$xc+0.115}] 0.60
}

# nor vdd
rect metal1 3.585 3.40 3.755 3.90

# nor net2
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

# net1
foreach xc {0.91 1.87 3.21 4.17} {
    rect m2contact [expr {$xc-0.13}] 1.07 [expr {$xc+0.13}] 1.33
    rect m2contact [expr {$xc-0.13}] 2.20 [expr {$xc+0.13}] 2.46
    rect metal1 [expr {$xc-0.19}] 1.01 [expr {$xc+0.19}] 1.39
    rect metal2 [expr {$xc-0.19}] 1.01 [expr {$xc+0.19}] 2.52
}
rect metal1 0.72 2.14 4.36 2.52
rect metal1 0.815 2.40 1.045 2.80

# net1 to inverter
rect metal1 4.36 2.14 5.14 2.52
rect metal1 4.84 1.70 5.14 2.52
rect metal1 4.84 1.70 5.90 1.92

# inverter gnd
rectd metal1 0.315 0.20 0.545 0.60
rectd metal1 1.275 0.20 1.505 0.60

# inverter vdd
rectd metal1 1.285 3.25 1.455 3.90

# inverter gate
rectd polysilicon 0.595 1.44 1.705 1.59
rectd polysilicon 0.985 1.59 1.315 1.92
rectd polysilicon 1.075 1.92 1.225 2.95
rectd pcontact    1.065 1.67 1.235 1.84
rectd locali      0.985 1.66 1.315 1.85
rectd viali       1.065 1.67 1.235 1.84
rectd metal1      1.00  1.60 1.30  1.92

# y
rectd m2contact 0.78 1.07 1.04 1.33
rectd m2contact 1.74 1.07 2.00 1.33
rectd m2contact 0.78 2.27 1.04 2.53
rectd m2contact 1.74 2.27 2.00 2.53
rectd m2contact 0.79 2.94 1.05 3.20
rectd metal1 0.72 1.01 1.10 1.39
rectd metal1 1.68 1.01 2.06 1.39
rectd metal1 0.72 2.21 2.06 2.59
rectd metal1 0.74 2.88 1.10 3.26
rectd metal2 0.72 1.01 1.11 3.26
rectd metal2 1.68 1.01 2.06 2.59

# pins
pin B   1.00 1.60 1.30 1.92
pin A   3.30 1.60 3.60 1.92
pin Y   5.80 2.30 6.20 2.50
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 690 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
