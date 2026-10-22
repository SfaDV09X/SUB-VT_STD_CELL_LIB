drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/XNOR2X1/layout
load xnor2x1

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
box 7.645um 0.235um 7.645um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xnia w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 7.965um 2.580um 7.965um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpia w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 17.305um 0.235um 17.305um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xnib w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 17.625um 2.580um 17.625um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xpib w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 0.285um 0.235um 0.285um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn1 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 0.605um 2.370um 0.605um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp7 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 3.905um 0.235um 3.905um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn2 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 4.225um 2.370um 4.225um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp5 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 9.945um 0.235um 9.945um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn3 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 10.265um 2.370um 10.265um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp8 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 13.565um 0.235um 13.565um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn4 w 0.84 l 0.15 nf 6 m 1 guard 0 topc 0 botc 0
box 13.885um 2.370um 13.885um 2.370um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp6 w 0.84 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

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
rect metal1 7.675 0.200 7.905 0.600
rect metal1 8.635 0.200 8.865 0.600
rect metal1 8.645 3.250 8.815 3.900
rect polysilicon 7.955 1.440 9.065 1.590
rect polysilicon 8.345 1.590 8.675 1.920
rect polysilicon 8.435 1.920 8.585 2.950
rect pcontact 8.425 1.670 8.595 1.840
rect locali 8.345 1.660 8.675 1.850
rect viali 8.425 1.670 8.595 1.840
rect metal1 8.360 1.600 8.660 1.920
rect m2contact 8.140 1.070 8.400 1.330
rect m2contact 9.100 1.070 9.360 1.330
rect m2contact 8.140 2.270 8.400 2.530
rect m2contact 9.100 2.270 9.360 2.530
rect m2contact 8.150 2.940 8.410 3.200
rect metal1 8.080 1.010 8.460 1.390
rect metal1 9.040 1.010 9.420 1.390
rect metal1 8.080 2.210 9.420 2.590
rect metal1 8.100 2.880 8.460 3.260
rect metal2 8.080 1.010 8.470 3.260
rect metal2 9.040 1.010 9.420 2.590
rect metal1 17.335 0.200 17.565 0.600
rect metal1 18.295 0.200 18.525 0.600
rect metal1 18.305 3.250 18.475 3.900
rect polysilicon 17.615 1.440 18.725 1.590
rect polysilicon 18.005 1.590 18.335 1.920
rect polysilicon 18.095 1.920 18.245 2.950
rect pcontact 18.085 1.670 18.255 1.840
rect locali 18.005 1.660 18.335 1.850
rect viali 18.085 1.670 18.255 1.840
rect metal1 18.020 1.600 18.320 1.920
rect m2contact 17.800 1.070 18.060 1.330
rect m2contact 18.760 1.070 19.020 1.330
rect m2contact 17.800 2.270 18.060 2.530
rect m2contact 18.760 2.270 19.020 2.530
rect m2contact 17.810 2.940 18.070 3.200
rect metal1 17.740 1.010 18.120 1.390
rect metal1 18.700 1.010 19.080 1.390
rect metal1 17.740 2.210 19.080 2.590
rect metal1 17.760 2.880 18.120 3.260
rect metal2 17.740 1.010 18.130 3.260
rect metal2 18.700 1.010 19.080 2.590
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
rect metal1 9.975 1.250 10.205 1.690
rect metal1 10.455 0.200 10.685 0.600
rect metal1 10.935 1.250 11.165 1.690
rect metal1 11.415 0.200 11.645 0.600
rect metal1 11.895 1.250 12.125 1.690
rect metal1 12.375 0.200 12.605 0.600
rect metal1 12.855 1.250 13.085 1.690
rect polysilicon 10.255 1.440 12.805 1.650
rect polysilicon 10.645 1.650 10.975 2.190
rect polysilicon 10.735 2.190 10.885 2.800
rect pcontact 10.725 1.940 10.895 2.110
rect locali 10.645 1.930 10.975 2.120
rect viali 10.725 1.940 10.895 2.110
rect metal1 10.660 1.870 10.960 2.190
rect m2contact 10.460 2.940 10.720 3.200
rect metal1 10.410 2.880 10.770 3.260
rect metal2 10.400 2.880 10.780 3.720
rect metal1 13.595 1.250 13.825 1.690
rect m2contact 14.060 1.070 14.320 1.330
rect metal1 14.000 1.010 14.380 1.390
rect metal2 14.000 1.010 14.380 2.560
rect metal1 14.555 1.250 14.785 1.690
rect m2contact 15.020 1.070 15.280 1.330
rect metal1 14.960 1.010 15.340 1.390
rect metal2 14.960 1.010 15.340 2.560
rect metal1 15.515 1.250 15.745 1.690
rect m2contact 15.980 1.070 16.240 1.330
rect metal1 15.920 1.010 16.300 1.390
rect metal2 15.920 1.010 16.300 2.560
rect metal1 16.475 1.250 16.705 1.690
rect metal2 14.000 2.300 16.300 2.560
rect polysilicon 13.875 1.440 16.425 1.650
rect polysilicon 14.265 1.650 14.595 2.190
rect polysilicon 14.355 2.190 14.505 2.800
rect pcontact 14.345 1.940 14.515 2.110
rect locali 14.265 1.930 14.595 2.120
rect viali 14.345 1.940 14.515 2.110
rect metal1 14.280 1.870 14.580 2.190
rect m2contact 14.520 2.940 14.780 3.200
rect metal1 14.470 2.880 14.830 3.260
rect metal2 14.460 2.880 14.840 3.720
rect metal1 0.315 1.540 7.045 1.690
rect metal1 9.975 1.540 16.705 1.690
rect metal1 1.255 3.000 4.665 3.200
rect metal1 2.710 2.910 3.090 3.290
rect m2contact 2.770 2.970 3.030 3.230
rect metal2 2.710 0.540 3.090 3.230
rect metal1 10.915 3.000 14.325 3.200
rect metal1 12.450 2.910 12.830 3.290
rect m2contact 12.510 2.970 12.770 3.230
rect metal2 12.450 0.540 12.830 3.230
rect metal2 2.710 0.540 12.830 0.800
rect metal2 6.260 2.300 6.640 3.720
rect metal2 15.920 2.300 16.300 3.720
rect metal2 6.260 3.460 16.300 3.720
rect metal1 4.620 1.830 8.660 2.070
rect metal1 14.280 1.830 18.320 2.070
rect metal1 9.420 2.140 10.960 2.520
rect metal1 10.660 2.140 10.960 2.520
rect metal2 18.700 0.140 19.080 1.200
rect metal2 0.070 0.140 19.080 0.400
rect metal2 0.070 0.140 0.450 2.150
rect metal1 0.070 1.830 0.450 2.210
rect m2contact 0.130 1.890 0.390 2.150
rect metal1 0.260 1.830 1.300 2.070

# pins
pin A 4.620 1.870 4.920 2.190
pin B 14.280 1.870 14.580 2.190
pin Y 10.410 2.880 10.770 3.260
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
