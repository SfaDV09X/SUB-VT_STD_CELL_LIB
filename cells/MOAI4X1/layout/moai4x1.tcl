drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/MOAI4X1/layout
load moai4x1

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
box 17.185um 0.235um 17.185um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xnib w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 17.505um 2.580um 17.505um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpib w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 2.585um 0.235um 2.585um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn4 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 2.905um 2.370um 2.905um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp7 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 6.205um 0.235um 6.205um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn3 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 6.525um 2.370um 6.525um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp8 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 9.825um 0.235um 9.825um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn5 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 10.145um 2.370um 10.145um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp2 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 13.445um 0.235um 13.445um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn6 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 13.765um 2.370um 13.765um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp1 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

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
rect metal1 17.215 0.200 17.445 0.600
rect metal1 18.175 0.200 18.405 0.600
rect metal1 18.185 3.250 18.355 3.900
rect polysilicon 17.495 1.440 18.605 1.590
rect polysilicon 17.885 1.590 18.215 1.920
rect polysilicon 17.975 1.920 18.125 2.950
rect pcontact 17.965 1.670 18.135 1.840
rect locali 17.885 1.660 18.215 1.850
rect viali 17.965 1.670 18.135 1.840
rect metal1 17.900 1.600 18.200 1.920
rect m2contact 17.680 1.070 17.940 1.330
rect m2contact 18.640 1.070 18.900 1.330
rect m2contact 17.680 2.270 17.940 2.530
rect m2contact 18.640 2.270 18.900 2.530
rect m2contact 17.690 2.940 17.950 3.200
rect metal1 17.620 1.010 18.000 1.390
rect metal1 18.580 1.010 18.960 1.390
rect metal1 17.620 2.210 18.960 2.590
rect metal1 17.640 2.880 18.000 3.260
rect metal2 17.620 1.010 18.010 3.260
rect metal2 18.580 1.010 18.960 2.590
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
rect metal1 6.765 3.400 6.935 3.900
rect metal1 9.855 1.250 10.085 1.690
rect metal1 10.335 0.200 10.565 0.600
rect metal1 10.815 1.250 11.045 1.690
rect metal1 11.295 0.200 11.525 0.600
rect metal1 11.775 1.250 12.005 1.690
rect metal1 12.255 0.200 12.485 0.600
rect metal1 12.735 1.250 12.965 1.690
rect polysilicon 10.135 1.440 12.685 1.650
rect polysilicon 10.525 1.650 10.855 2.190
rect polysilicon 10.615 2.190 10.765 2.800
rect pcontact 10.605 1.940 10.775 2.110
rect locali 10.525 1.930 10.855 2.120
rect viali 10.605 1.940 10.775 2.110
rect metal1 10.540 1.870 10.840 2.190
rect m2contact 10.780 2.940 11.040 3.200
rect metal1 10.730 2.880 11.090 3.260
rect metal2 10.720 2.880 11.100 3.720
rect metal1 13.475 1.250 13.705 1.690
rect m2contact 13.940 1.070 14.200 1.330
rect metal1 13.880 1.010 14.260 1.390
rect metal2 13.880 1.010 14.260 2.560
rect metal1 14.435 1.250 14.665 1.690
rect m2contact 14.900 1.070 15.160 1.330
rect metal1 14.840 1.010 15.220 1.390
rect metal2 14.840 1.010 15.220 2.560
rect metal1 15.395 1.250 15.625 1.690
rect m2contact 15.860 1.070 16.120 1.330
rect metal1 15.800 1.010 16.180 1.390
rect metal2 15.800 1.010 16.180 2.560
rect metal1 16.355 1.250 16.585 1.690
rect metal2 13.880 2.300 16.180 2.560
rect polysilicon 13.755 1.440 16.305 1.650
rect polysilicon 14.145 1.650 14.475 2.190
rect polysilicon 14.235 2.190 14.385 2.800
rect pcontact 14.225 1.940 14.395 2.110
rect locali 14.145 1.930 14.475 2.120
rect viali 14.225 1.940 14.395 2.110
rect metal1 14.160 1.870 14.460 2.190
rect m2contact 14.400 2.940 14.660 3.200
rect metal1 14.350 2.880 14.710 3.260
rect metal2 14.340 2.300 14.720 3.720
rect metal1 2.615 1.540 16.585 1.690
rect metal1 7.175 3.000 10.585 3.200
rect metal1 3.555 3.000 6.095 3.200
rect metal1 5.790 2.910 6.170 3.290
rect m2contact 5.850 2.970 6.110 3.230
rect metal2 5.790 0.540 6.170 3.230
rect metal1 13.105 3.000 14.205 3.200
rect metal1 13.030 2.910 13.410 3.290
rect m2contact 13.090 2.970 13.350 3.230
rect metal2 13.030 0.540 13.410 3.230
rect metal2 5.790 0.540 13.410 0.800
rect metal2 4.940 2.300 5.320 3.720
rect metal2 4.940 3.460 14.720 3.720
rect metal1 2.060 2.140 3.600 2.520
rect metal1 3.300 2.140 3.600 2.520
rect metal1 14.160 2.140 17.740 2.520

# pins
pin A 1.000 1.600 1.300 1.920
pin B 17.900 1.600 18.200 1.920
pin C 6.920 1.870 7.220 2.190
pin D 10.540 1.870 10.840 2.190
pin Y 14.350 2.880 14.710 3.260
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
