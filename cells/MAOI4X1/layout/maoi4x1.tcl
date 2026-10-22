drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/MAOI4X1/layout
load maoi4x1

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
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xnia w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 0.605um 2.580um 0.605um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpia w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 9.945um 0.235um 9.945um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xnib w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 10.265um 2.580um 10.265um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpib w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 2.585um 0.235um 2.585um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn2 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 2.905um 2.370um 2.905um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp5 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 6.205um 0.235um 6.205um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn1 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 6.525um 2.370um 6.525um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp7 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 12.245um 0.235um 12.245um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn4 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 12.565um 2.370um 12.565um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp6 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 15.865um 0.235um 15.865um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn3 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 16.185um 2.370um 16.185um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp8 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# layout
rect metal1 0.000 -0.240 19.320 0.240
rect metal1 0.000 3.840 19.320 4.320
rect psubstratepdiff 0.180 -0.145 19.140 0.145
rect psubstratepcontact 0.300 -0.085 19.020 0.085
rect locali 0.210 -0.165 19.110 0.165
rect viali 0.300 -0.085 19.020 0.085
rect nsubstratendiff 0.180 3.935 19.140 4.225
rect nsubstratencontact 0.300 3.995 19.020 4.165
rect locali 0.210 3.915 19.110 4.245
rect viali 0.300 3.995 19.020 4.165
rect nwell -0.230 1.870 19.550 4.410
rect metal1 0.315 0.200 0.545 0.600
rect metal1 1.275 0.200 1.505 0.600
rect metal1 1.285 3.250 1.455 3.900
rect polysilicon 0.595 1.440 1.705 1.590
rect polysilicon 0.985 1.590 1.315 1.920
rect polysilicon 1.075 1.920 1.225 2.950
rect pcontact 1.065 1.670 1.235 1.840
rect locali 0.985 1.660 1.315 1.850
rect viali 1.065 1.670 1.235 1.840
rect metal1 1.000 1.600 1.300 1.920
rect m2contact 0.780 1.070 1.040 1.330
rect m2contact 1.740 1.070 2.000 1.330
rect m2contact 0.780 2.270 1.040 2.530
rect m2contact 1.740 2.270 2.000 2.530
rect m2contact 0.790 2.940 1.050 3.200
rect metal1 0.720 1.010 1.100 1.390
rect metal1 1.680 1.010 2.060 1.390
rect metal1 0.720 2.210 2.060 2.590
rect metal1 0.740 2.880 1.100 3.260
rect metal2 0.720 1.010 1.110 3.260
rect metal2 1.680 1.010 2.060 2.590
rect metal1 9.975 0.200 10.205 0.600
rect metal1 10.935 0.200 11.165 0.600
rect metal1 10.945 3.250 11.115 3.900
rect polysilicon 10.255 1.440 11.365 1.590
rect polysilicon 10.645 1.590 10.975 1.920
rect polysilicon 10.735 1.920 10.885 2.950
rect pcontact 10.725 1.670 10.895 1.840
rect locali 10.645 1.660 10.975 1.850
rect viali 10.725 1.670 10.895 1.840
rect metal1 10.660 1.600 10.960 1.920
rect m2contact 10.440 1.070 10.700 1.330
rect m2contact 11.400 1.070 11.660 1.330
rect m2contact 10.440 2.270 10.700 2.530
rect m2contact 11.400 2.270 11.660 2.530
rect m2contact 10.450 2.940 10.710 3.200
rect metal1 10.380 1.010 10.760 1.390
rect metal1 11.340 1.010 11.720 1.390
rect metal1 10.380 2.210 11.720 2.590
rect metal1 10.400 2.880 10.760 3.260
rect metal2 10.380 1.010 10.770 3.260
rect metal2 11.340 1.010 11.720 2.590
rect metal1 2.615 1.250 2.845 1.690
rect m2contact 3.080 1.070 3.340 1.330
rect metal1 3.020 1.010 3.400 1.390
rect metal2 3.020 1.010 3.400 2.560
rect metal1 3.575 1.250 3.805 1.690
rect m2contact 4.040 1.070 4.300 1.330
rect metal1 3.980 1.010 4.360 1.390
rect metal2 3.980 1.010 4.360 2.560
rect metal1 4.535 1.250 4.765 1.690
rect m2contact 5.000 1.070 5.260 1.330
rect metal1 4.940 1.010 5.320 1.390
rect metal2 4.940 1.010 5.320 2.560
rect metal1 5.495 1.250 5.725 1.690
rect metal2 3.020 2.300 5.320 2.560
rect polysilicon 2.895 1.440 5.445 1.650
rect polysilicon 3.285 1.650 3.615 2.190
rect polysilicon 3.375 2.190 3.525 2.800
rect pcontact 3.365 1.940 3.535 2.110
rect locali 3.285 1.930 3.615 2.120
rect viali 3.365 1.940 3.535 2.110
rect metal1 3.300 1.870 3.600 2.190
rect metal1 3.145 3.400 3.315 3.900
rect metal1 6.235 1.250 6.465 1.690
rect metal1 6.715 0.200 6.945 0.600
rect metal1 7.195 1.250 7.425 1.690
rect metal1 7.675 0.200 7.905 0.600
rect metal1 8.155 1.250 8.385 1.690
rect metal1 8.635 0.200 8.865 0.600
rect metal1 9.115 1.250 9.345 1.690
rect polysilicon 6.515 1.440 9.065 1.650
rect polysilicon 6.905 1.650 7.235 2.190
rect polysilicon 6.995 2.190 7.145 2.800
rect pcontact 6.985 1.940 7.155 2.110
rect locali 6.905 1.930 7.235 2.120
rect viali 6.985 1.940 7.155 2.110
rect metal1 6.920 1.870 7.220 2.190
rect metal1 7.205 3.400 7.375 3.900
rect metal1 12.275 1.250 12.505 1.690
rect m2contact 12.740 1.070 13.000 1.330
rect metal1 12.680 1.010 13.060 1.390
rect metal2 12.680 1.010 13.060 2.560
rect metal1 13.235 1.250 13.465 1.690
rect m2contact 13.700 1.070 13.960 1.330
rect metal1 13.640 1.010 14.020 1.390
rect metal2 13.640 1.010 14.020 2.560
rect metal1 14.195 1.250 14.425 1.690
rect m2contact 14.660 1.070 14.920 1.330
rect metal1 14.600 1.010 14.980 1.390
rect metal2 14.600 1.010 14.980 2.560
rect metal1 15.155 1.250 15.385 1.690
rect metal2 12.680 2.300 14.980 2.560
rect polysilicon 12.555 1.440 15.105 1.650
rect polysilicon 12.945 1.650 13.275 2.190
rect polysilicon 13.035 2.190 13.185 2.800
rect pcontact 13.025 1.940 13.195 2.110
rect locali 12.945 1.930 13.275 2.120
rect viali 13.025 1.940 13.195 2.110
rect metal1 12.960 1.870 13.260 2.190
rect m2contact 12.760 2.940 13.020 3.200
rect metal1 12.710 2.880 13.070 3.260
rect metal2 12.700 2.300 13.080 3.720
rect metal1 15.895 1.250 16.125 1.690
rect metal1 16.375 0.200 16.605 0.600
rect metal1 16.855 1.250 17.085 1.690
rect metal1 17.335 0.200 17.565 0.600
rect metal1 17.815 1.250 18.045 1.690
rect metal1 18.295 0.200 18.525 0.600
rect metal1 18.775 1.250 19.005 1.690
rect polysilicon 16.175 1.440 18.725 1.650
rect polysilicon 16.565 1.650 16.895 2.190
rect polysilicon 16.655 2.190 16.805 2.800
rect pcontact 16.645 1.940 16.815 2.110
rect locali 16.565 1.930 16.895 2.120
rect viali 16.645 1.940 16.815 2.110
rect metal1 16.580 1.870 16.880 2.190
rect m2contact 16.820 2.940 17.080 3.200
rect metal1 16.770 2.880 17.130 3.260
rect metal2 16.760 2.880 17.140 3.720
rect metal1 2.615 1.540 9.345 1.690
rect metal1 12.275 1.540 19.005 1.690
rect metal1 3.555 3.000 6.965 3.200
rect metal1 5.790 2.910 6.170 3.290
rect m2contact 5.850 2.970 6.110 3.230
rect metal2 5.790 0.540 6.170 3.230
rect metal1 13.215 3.000 16.625 3.200
rect metal1 15.450 2.910 15.830 3.290
rect m2contact 15.510 2.970 15.770 3.230
rect metal2 15.450 0.540 15.830 3.230
rect metal2 5.790 0.540 15.830 0.800
rect metal2 4.940 2.300 5.320 3.720
rect metal2 4.940 3.460 17.140 3.720
rect metal1 2.060 2.140 3.600 2.520
rect metal1 3.300 2.140 3.600 2.520
rect metal1 6.920 2.140 10.500 2.520

# pins
pin A 1.000 1.600 1.300 1.920
pin B 10.660 1.600 10.960 1.920
pin C 12.960 1.870 13.260 2.190
pin D 16.580 1.870 16.880 2.190
pin Y 16.770 2.880 17.130 3.260
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 1932 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
