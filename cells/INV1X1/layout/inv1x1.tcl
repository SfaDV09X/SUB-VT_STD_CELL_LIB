drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/INV1X1/layout
load inv1x1

set portErrors {}

proc rect {layer x1 y1 x2 y2} {
    box ${x1}um ${y1}um ${x2}um ${y2}um
    paint $layer
}
proc pin {name x1 y1 x2 y2} {
    global portErrors
    box ${x1}um ${y1}um ${x2}um ${y2}um
    label $name c metal1
    select area labels
    if {[catch {port make} msg]} { lappend portErrors "$name: $msg" }
    select clear
}

# devices
box 0.285um 0.235um 0.285um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 0.605um 2.58um 0.605um 2.58um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# rails
rect metal1 0 -0.24 2.30 0.24
rect metal1 0 3.84 2.30 4.32

# taps
rect psubstratepdiff    0.18 -0.145 2.12 0.145
rect psubstratepcontact 0.30 -0.085 2.00 0.085
rect locali             0.21 -0.165 2.09 0.165
rect viali              0.30 -0.085 2.00 0.085
rect nsubstratendiff    0.18 3.935 2.12 4.225
rect nsubstratencontact 0.30 3.995 2.00 4.165
rect locali             0.21 3.915 2.09 4.245
rect viali              0.30 3.995 2.00 4.165

# nwell
rect nwell -0.23 1.87 2.53 4.41

# gnd
rect metal1 0.315 0.20 0.545 0.60
rect metal1 1.275 0.20 1.505 0.60

# vdd
rect metal1 1.285 3.25 1.455 3.90

# a
rect polysilicon 0.595 1.44 1.705 1.59
rect polysilicon 0.985 1.59 1.315 1.92
rect polysilicon 1.075 1.92 1.225 2.95
rect pcontact    1.065 1.67 1.235 1.84
rect locali      0.985 1.66 1.315 1.85
rect viali       1.065 1.67 1.235 1.84
rect metal1      1.00  1.60 1.30  1.92

# y
rect m2contact 0.78 1.07 1.04 1.33
rect m2contact 1.74 1.07 2.00 1.33
rect m2contact 0.78 2.27 1.04 2.53
rect m2contact 1.74 2.27 2.00 2.53
rect m2contact 0.79 2.94 1.05 3.20
rect metal1 0.72 1.01 1.10 1.39
rect metal1 1.68 1.01 2.06 1.39
rect metal1 0.72 2.21 2.06 2.59
rect metal1 0.74 2.88 1.10 3.26
rect metal2 0.72 1.01 1.11 3.26
rect metal2 1.68 1.01 2.06 2.59

# pins
pin A   1.00 1.60 1.30 1.92
pin Y   1.20 2.30 1.60 2.50
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 230 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
