drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/OAI3X1/layout
load oai3x1

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
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn4 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 0.605um 2.370um 0.605um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp2 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 3.905um 0.235um 3.905um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn5 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 4.225um 2.370um 4.225um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp1 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 7.525um 0.235um 7.525um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn6 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 7.845um 2.580um 7.845um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp3 w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# layout
rect metal1 0.000 -0.240 11.040 0.240
rect metal1 0.000 3.840 11.040 4.320
rect psubstratepdiff 0.180 -0.145 10.860 0.145
rect psubstratepcontact 0.300 -0.085 10.740 0.085
rect locali 0.210 -0.165 10.830 0.165
rect viali 0.300 -0.085 10.740 0.085
rect nsubstratendiff 0.180 3.935 10.860 4.225
rect nsubstratencontact 0.300 3.995 10.740 4.165
rect locali 0.210 3.915 10.830 4.245
rect viali 0.300 3.995 10.740 4.165
rect nwell -0.230 1.870 11.270 4.410
rect metal1 0.315 1.250 0.545 1.690
rect m2contact 0.780 1.070 1.040 1.330
rect metal1 0.720 1.010 1.100 1.390
rect metal2 0.720 1.010 1.100 2.560
rect metal1 1.275 1.250 1.505 1.690
rect m2contact 1.740 1.070 2.000 1.330
rect metal1 1.680 1.010 2.060 1.390
rect metal2 1.680 1.010 2.060 2.560
rect metal1 2.235 1.250 2.465 1.690
rect m2contact 2.700 1.070 2.960 1.330
rect metal1 2.640 1.010 3.020 1.390
rect metal2 2.640 1.010 3.020 2.560
rect metal1 3.195 1.250 3.425 1.690
rect metal2 0.720 2.300 3.020 2.560
rect polysilicon 0.595 1.440 3.145 1.650
rect polysilicon 0.985 1.650 1.315 2.190
rect polysilicon 1.075 2.190 1.225 2.800
rect pcontact 1.065 1.940 1.235 2.110
rect locali 0.985 1.930 1.315 2.120
rect viali 1.065 1.940 1.235 2.110
rect metal1 1.000 1.870 1.300 2.190
rect metal1 0.845 3.400 1.015 3.900
rect metal1 3.935 1.250 4.165 1.690
rect m2contact 4.400 1.070 4.660 1.330
rect metal1 4.340 1.010 4.720 1.390
rect metal2 4.340 1.010 4.720 2.560
rect metal1 4.895 1.250 5.125 1.690
rect m2contact 5.360 1.070 5.620 1.330
rect metal1 5.300 1.010 5.680 1.390
rect metal2 5.300 1.010 5.680 2.560
rect metal1 5.855 1.250 6.085 1.690
rect m2contact 6.320 1.070 6.580 1.330
rect metal1 6.260 1.010 6.640 1.390
rect metal2 6.260 1.010 6.640 2.560
rect metal1 6.815 1.250 7.045 1.690
rect metal2 4.340 2.300 6.640 2.560
rect polysilicon 4.215 1.440 6.765 1.650
rect polysilicon 4.605 1.650 4.935 2.190
rect polysilicon 4.695 2.190 4.845 2.800
rect pcontact 4.685 1.940 4.855 2.110
rect locali 4.605 1.930 4.935 2.120
rect viali 4.685 1.940 4.855 2.110
rect metal1 4.620 1.870 4.920 2.190
rect m2contact 4.860 2.940 5.120 3.200
rect metal1 4.810 2.880 5.170 3.260
rect metal2 4.800 2.300 5.180 3.260
rect metal1 7.555 1.250 7.785 1.690
rect metal1 8.035 0.200 8.265 0.600
rect metal1 8.515 1.250 8.745 1.690
rect metal1 8.995 0.200 9.225 0.600
rect metal1 9.475 1.250 9.705 1.690
rect metal1 9.955 0.200 10.185 0.600
rect metal1 10.435 1.250 10.665 1.690
rect polysilicon 7.835 1.440 10.385 1.650
rect polysilicon 8.225 1.650 8.555 2.190
rect polysilicon 8.315 2.190 8.465 2.950
rect pcontact 8.305 1.940 8.475 2.110
rect locali 8.225 1.930 8.555 2.120
rect viali 8.305 1.940 8.475 2.110
rect metal1 8.240 1.870 8.540 2.190
rect m2contact 8.040 2.940 8.300 3.200
rect metal1 7.990 2.880 8.350 3.260
rect metal2 7.980 2.300 8.360 3.260
rect metal1 8.525 3.250 8.695 3.900
rect metal1 0.315 1.540 10.665 1.690
rect metal1 1.255 3.000 4.665 3.200
rect metal2 0.720 2.300 8.360 2.560

# pins
pin A 1.000 1.870 1.300 2.190
pin B 4.620 1.870 4.920 2.190
pin C 8.240 1.870 8.540 2.190
pin Y 4.810 2.880 5.170 3.260
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 1104 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
