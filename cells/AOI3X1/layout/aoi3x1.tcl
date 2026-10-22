drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/AOI3X1/layout
load aoi3x1

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
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn6 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 0.605um 2.370um 0.605um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp3 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 3.905um 0.235um 3.905um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn4 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 4.225um 2.370um 4.225um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp2 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 7.645um 0.235um 7.645um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn5 w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 7.965um 2.370um 7.965um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp1 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# layout
rect metal1 0.000 -0.240 9.660 0.240
rect metal1 0.000 3.840 9.660 4.320
rect psubstratepdiff 0.180 -0.145 9.480 0.145
rect psubstratepcontact 0.300 -0.085 9.360 0.085
rect locali 0.210 -0.165 9.450 0.165
rect viali 0.300 -0.085 9.360 0.085
rect nsubstratendiff 0.180 3.935 9.480 4.225
rect nsubstratencontact 0.300 3.995 9.360 4.165
rect locali 0.210 3.915 9.450 4.245
rect viali 0.300 3.995 9.360 4.165
rect nwell -0.230 1.870 9.890 4.410
rect metal1 0.315 1.250 0.545 1.690
rect metal1 0.795 0.200 1.025 0.600
rect metal1 1.275 1.250 1.505 1.690
rect metal1 1.755 0.200 1.985 0.600
rect metal1 2.235 1.250 2.465 1.690
rect metal1 2.715 0.200 2.945 0.600
rect metal1 3.195 1.250 3.425 1.690
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
rect metal1 4.905 3.400 5.075 3.900
rect metal1 7.675 0.200 7.905 0.600
rect m2contact 8.140 1.070 8.400 1.330
rect metal1 8.080 1.010 8.460 1.390
rect metal2 8.080 1.010 8.460 2.560
rect metal1 8.635 0.200 8.865 0.600
rect m2contact 9.100 1.070 9.360 1.330
rect metal1 9.040 1.010 9.420 1.390
rect metal2 9.040 1.010 9.420 2.560
rect metal2 8.080 2.300 9.420 2.560
rect polysilicon 7.955 1.440 9.065 1.590
rect polysilicon 8.345 1.590 8.675 1.920
rect polysilicon 8.435 1.920 8.585 2.800
rect pcontact 8.425 1.670 8.595 1.840
rect locali 8.345 1.660 8.675 1.850
rect viali 8.425 1.670 8.595 1.840
rect metal1 8.360 1.600 8.660 1.920
rect m2contact 8.160 2.940 8.420 3.200
rect metal1 8.110 2.880 8.470 3.260
rect metal2 8.100 2.300 8.480 3.260
rect metal1 0.315 1.540 7.045 1.690
rect metal1 1.255 3.000 4.665 3.200
rect metal1 2.710 2.910 3.090 3.290
rect m2contact 2.770 2.970 3.030 3.230
rect metal2 2.710 2.970 3.090 3.720
rect metal1 8.615 3.000 9.440 3.200
rect metal1 9.060 2.910 9.440 3.290
rect m2contact 9.120 2.970 9.380 3.230
rect metal2 9.060 2.970 9.440 3.720
rect metal2 2.710 3.460 9.440 3.720
rect metal2 4.340 2.300 9.420 2.560

# pins
pin B 1.000 1.870 1.300 2.190
pin A 4.620 1.870 4.920 2.190
pin C 8.360 1.600 8.660 1.920
pin Y 8.110 2.880 8.470 3.260
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 966 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
