drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/DLX1/layout
load dlx1

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
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_ck w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 0.605um 2.580um 0.605um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_ck w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 2.585um 0.235um 2.585um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_in w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 2.905um 2.580um 2.905um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_in w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 5.345um 0.235um 5.345um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_a w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 5.665um 2.580um 5.665um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_a w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 7.645um 0.235um 7.645um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_b w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 7.965um 2.580um 7.965um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_b w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 9.945um 0.235um 9.945um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_fb w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 10.265um 2.580um 10.265um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_fb w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# layout
rect metal1 0.000 -0.240 12.420 0.240
rect metal1 0.000 3.840 12.420 4.320
rect psubstratepdiff 0.180 -0.145 12.240 0.145
rect psubstratepcontact 0.300 -0.085 12.120 0.085
rect locali 0.210 -0.165 12.210 0.165
rect viali 0.300 -0.085 12.120 0.085
rect nsubstratendiff 0.180 3.935 12.240 4.225
rect nsubstratencontact 0.300 3.995 12.120 4.165
rect locali 0.210 3.915 12.210 4.245
rect viali 0.300 3.995 12.120 4.165
rect nwell -0.230 1.870 12.650 4.410
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
rect metal1 2.615 1.250 2.845 1.690
rect m2contact 3.080 1.070 3.340 1.330
rect metal1 3.020 1.010 3.400 1.390
rect metal2 3.020 1.010 3.400 2.560
rect metal1 3.575 1.250 3.805 1.690
rect m2contact 4.040 1.070 4.300 1.330
rect metal1 3.980 1.010 4.360 1.390
rect metal2 3.980 1.010 4.360 2.560
rect metal2 3.020 2.400 4.360 2.560
rect metal1 2.615 1.540 4.645 1.690
rect metal1 4.425 1.540 4.645 3.200
rect metal1 3.555 3.000 4.645 3.200
rect m2contact 3.100 2.940 3.360 3.200
rect metal1 3.050 2.880 3.410 3.260
rect metal2 3.040 2.400 3.420 3.260
rect polysilicon 2.895 1.440 4.005 1.650
rect polysilicon 2.685 1.650 3.045 2.200
rect pcontact 2.780 1.950 2.950 2.120
rect locali 2.700 1.940 3.030 2.130
rect viali 2.780 1.950 2.950 2.120
rect metal1 2.715 1.870 3.015 2.200
rect polysilicon 3.285 1.870 3.615 2.200
rect polysilicon 3.375 2.200 3.525 2.950
rect pcontact 3.365 1.950 3.535 2.120
rect locali 3.285 1.940 3.615 2.130
rect viali 3.365 1.950 3.535 2.120
rect metal1 3.300 1.870 3.600 2.200
rect metal1 5.375 0.200 5.605 0.600
rect metal1 6.335 0.200 6.565 0.600
rect metal1 6.345 3.250 6.515 3.900
rect polysilicon 5.655 1.440 6.765 1.590
rect polysilicon 6.045 1.590 6.375 1.920
rect polysilicon 6.135 1.920 6.285 2.950
rect pcontact 6.125 1.670 6.295 1.840
rect locali 6.045 1.660 6.375 1.850
rect viali 6.125 1.670 6.295 1.840
rect metal1 6.060 1.600 6.360 1.920
rect m2contact 5.840 1.070 6.100 1.330
rect m2contact 6.800 1.070 7.060 1.330
rect m2contact 5.840 2.270 6.100 2.530
rect m2contact 6.800 2.270 7.060 2.530
rect m2contact 5.850 2.940 6.110 3.200
rect metal1 5.780 1.010 6.160 1.390
rect metal1 6.740 1.010 7.120 1.390
rect metal1 5.780 2.210 7.120 2.590
rect metal1 5.800 2.880 6.160 3.260
rect metal2 5.780 1.010 6.170 3.260
rect metal2 6.740 1.010 7.120 2.590
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
rect metal1 9.975 1.250 10.205 1.690
rect m2contact 10.440 1.070 10.700 1.330
rect metal1 10.380 1.010 10.760 1.390
rect metal2 10.380 1.010 10.760 2.560
rect metal1 10.935 1.250 11.165 1.690
rect m2contact 11.400 1.070 11.660 1.330
rect metal1 11.340 1.010 11.720 1.390
rect metal2 11.340 1.010 11.720 2.560
rect metal2 10.380 2.400 11.720 2.560
rect metal1 9.975 1.540 12.005 1.690
rect metal1 11.785 1.540 12.005 3.200
rect metal1 10.915 3.000 12.005 3.200
rect m2contact 10.460 2.940 10.720 3.200
rect metal1 10.410 2.880 10.770 3.260
rect metal2 10.400 2.400 10.780 3.260
rect polysilicon 10.255 1.440 11.365 1.650
rect polysilicon 10.045 1.650 10.405 2.200
rect pcontact 10.140 1.950 10.310 2.120
rect locali 10.060 1.940 10.390 2.130
rect viali 10.140 1.950 10.310 2.120
rect metal1 10.075 1.870 10.375 2.200
rect polysilicon 10.645 1.870 10.975 2.200
rect polysilicon 10.735 2.200 10.885 2.950
rect pcontact 10.725 1.950 10.895 2.120
rect locali 10.645 1.940 10.975 2.130
rect viali 10.725 1.950 10.895 2.120
rect metal1 10.660 1.870 10.960 2.200
rect metal1 1.190 1.820 1.330 2.030
rect metal1 1.190 1.890 2.800 2.030
rect metal1 2.590 2.100 2.800 2.240
rect metal2 2.590 2.100 2.730 3.570
rect metal1 2.590 3.430 2.730 3.640
rect metal1 2.590 3.500 5.460 3.640
rect metal1 5.320 3.430 5.460 3.640
rect metal2 5.320 3.430 9.310 3.570
rect metal2 9.170 2.870 9.310 3.570
rect metal1 9.170 2.870 10.220 3.010
rect metal1 10.080 2.380 10.220 3.010
rect metal1 10.080 2.380 10.780 2.520
rect metal1 10.640 2.100 10.780 2.520
rect m2contact 2.530 2.040 2.790 2.300
rect metal1 2.470 1.980 2.850 2.360
rect metal2 2.470 1.980 2.850 2.360
rect m2contact 2.530 3.370 2.790 3.630
rect metal1 2.470 3.310 2.850 3.690
rect metal2 2.470 3.310 2.850 3.690
rect m2contact 5.260 3.370 5.520 3.630
rect metal1 5.200 3.310 5.580 3.690
rect metal2 5.200 3.310 5.580 3.690
rect m2contact 9.110 2.810 9.370 3.070
rect metal1 9.050 2.750 9.430 3.130
rect metal2 9.050 2.750 9.430 3.130
rect metal1 1.960 2.520 3.430 2.660
rect metal1 3.290 2.100 3.430 2.660
rect metal2 1.960 0.700 2.100 1.120
rect metal2 1.960 0.700 9.870 0.840
rect metal2 9.730 0.700 9.870 2.100
rect metal1 9.730 1.960 10.150 2.100
rect m2contact 9.670 1.900 9.930 2.160
rect metal1 9.610 1.840 9.990 2.220
rect metal2 9.610 1.840 9.990 2.220
rect metal1 4.550 1.540 6.160 1.680
rect metal1 4.550 2.870 5.040 3.010
rect metal2 4.900 2.870 5.040 3.990
rect metal2 4.900 3.850 9.730 3.990
rect metal2 9.590 3.430 9.730 3.990
rect metal1 9.590 3.430 9.730 3.640
rect metal1 9.590 3.500 11.060 3.640
rect metal1 10.920 3.220 11.060 3.640
rect m2contact 4.840 2.810 5.100 3.070
rect metal1 4.780 2.750 5.160 3.130
rect metal2 4.780 2.750 5.160 3.130
rect m2contact 9.530 3.370 9.790 3.630
rect metal1 9.470 3.310 9.850 3.690
rect metal2 9.470 3.310 9.850 3.690
rect metal2 7.000 1.540 7.140 1.680
rect metal1 7.000 1.540 8.470 1.680
rect m2contact 6.940 1.480 7.200 1.740
rect metal1 6.880 1.420 7.260 1.800
rect metal2 6.880 1.420 7.260 1.800
rect metal2 9.310 2.380 10.500 2.520
rect metal1 9.990 2.100 10.075 2.200
rect metal1 9.990 1.870 10.075 1.960
rect metal1 4.645 3.010 4.780 3.130
rect metal1 4.645 2.750 4.780 2.870
rect metal1 6.880 1.390 7.120 1.420
rect metal1 10.780 2.200 10.800 2.240
rect metal1 1.160 1.920 1.190 1.960
rect metal1 1.920 2.590 1.960 2.660
rect metal2 2.060 1.120 2.100 1.150
rect metal1 3.430 2.200 3.440 2.240
rect metal1 6.020 1.680 6.060 1.740
rect metal1 8.330 1.680 8.360 1.740

# pins
pin CLK 1.000 1.600 1.300 1.920
pin D 3.050 2.880 3.410 3.260
pin QB 5.800 2.880 6.160 3.260
pin Q 8.100 2.880 8.460 3.260
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 1242 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
