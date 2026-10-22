drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/DFFX1/layout
load dffx1

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
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_mf w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 5.665um 2.580um 5.665um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_mf w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 8.105um 0.235um 8.105um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_7 w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 8.425um 2.580um 8.425um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_7 w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 10.405um 0.235um 10.405um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_17 w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 10.725um 2.580um 10.725um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_17 w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 12.705um 0.235um 12.705um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_ps w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 13.025um 2.580um 13.025um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_ps w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 15.465um 0.235um 15.465um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_sf w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 15.785um 2.580um 15.785um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_sf w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 18.225um 0.235um 18.225um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_9 w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 18.545um 2.580um 18.545um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_9 w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0
box 20.525um 0.235um 20.525um 0.235um
magic::gencell sky130::sky130_fd_pr__nfet_01v8 xn_11 w 0.84 l 0.15 nf 3 m 1 guard 0 topc 0 botc 0
box 20.845um 2.580um 20.845um 2.580um
magic::gencell sky130::sky130_fd_pr__pfet_01v8 xp_11 w 0.42 l 0.15 nf 1 m 1 guard 0 topc 0 botc 0

# layout
rect metal1 0.000 -0.240 22.540 0.240
rect metal1 0.000 3.840 22.540 4.320
rect psubstratepdiff 0.180 -0.145 22.360 0.145
rect psubstratepcontact 0.300 -0.085 22.240 0.085
rect locali 0.210 -0.165 22.330 0.165
rect viali 0.300 -0.085 22.240 0.085
rect nsubstratendiff 0.180 3.935 22.360 4.225
rect nsubstratencontact 0.300 3.995 22.240 4.165
rect locali 0.210 3.915 22.330 4.245
rect viali 0.300 3.995 22.240 4.165
rect nwell -0.230 1.870 22.770 4.410
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
rect metal1 5.375 1.250 5.605 1.690
rect m2contact 5.840 1.070 6.100 1.330
rect metal1 5.780 1.010 6.160 1.390
rect metal2 5.780 1.010 6.160 2.560
rect metal1 6.335 1.250 6.565 1.690
rect m2contact 6.800 1.070 7.060 1.330
rect metal1 6.740 1.010 7.120 1.390
rect metal2 6.740 1.010 7.120 2.560
rect metal2 5.780 2.400 7.120 2.560
rect metal1 5.375 1.540 7.405 1.690
rect metal1 7.185 1.540 7.405 3.200
rect metal1 6.315 3.000 7.405 3.200
rect m2contact 5.860 2.940 6.120 3.200
rect metal1 5.810 2.880 6.170 3.260
rect metal2 5.800 2.400 6.180 3.260
rect polysilicon 5.655 1.440 6.765 1.650
rect polysilicon 5.445 1.650 5.805 2.200
rect pcontact 5.540 1.950 5.710 2.120
rect locali 5.460 1.940 5.790 2.130
rect viali 5.540 1.950 5.710 2.120
rect metal1 5.475 1.870 5.775 2.200
rect polysilicon 6.045 1.870 6.375 2.200
rect polysilicon 6.135 2.200 6.285 2.950
rect pcontact 6.125 1.950 6.295 2.120
rect locali 6.045 1.940 6.375 2.130
rect viali 6.125 1.950 6.295 2.120
rect metal1 6.060 1.870 6.360 2.200
rect metal1 8.135 0.200 8.365 0.600
rect metal1 9.095 0.200 9.325 0.600
rect metal1 9.105 3.250 9.275 3.900
rect polysilicon 8.415 1.440 9.525 1.590
rect polysilicon 8.805 1.590 9.135 1.920
rect polysilicon 8.895 1.920 9.045 2.950
rect pcontact 8.885 1.670 9.055 1.840
rect locali 8.805 1.660 9.135 1.850
rect viali 8.885 1.670 9.055 1.840
rect metal1 8.820 1.600 9.120 1.920
rect m2contact 8.600 1.070 8.860 1.330
rect m2contact 9.560 1.070 9.820 1.330
rect m2contact 8.600 2.270 8.860 2.530
rect m2contact 9.560 2.270 9.820 2.530
rect m2contact 8.610 2.940 8.870 3.200
rect metal1 8.540 1.010 8.920 1.390
rect metal1 9.500 1.010 9.880 1.390
rect metal1 8.540 2.210 9.880 2.590
rect metal1 8.560 2.880 8.920 3.260
rect metal2 8.540 1.010 8.930 3.260
rect metal2 9.500 1.010 9.880 2.590
rect metal1 10.435 0.200 10.665 0.600
rect metal1 11.395 0.200 11.625 0.600
rect metal1 11.405 3.250 11.575 3.900
rect polysilicon 10.715 1.440 11.825 1.590
rect polysilicon 11.105 1.590 11.435 1.920
rect polysilicon 11.195 1.920 11.345 2.950
rect pcontact 11.185 1.670 11.355 1.840
rect locali 11.105 1.660 11.435 1.850
rect viali 11.185 1.670 11.355 1.840
rect metal1 11.120 1.600 11.420 1.920
rect m2contact 10.900 1.070 11.160 1.330
rect m2contact 11.860 1.070 12.120 1.330
rect m2contact 10.900 2.270 11.160 2.530
rect m2contact 11.860 2.270 12.120 2.530
rect m2contact 10.910 2.940 11.170 3.200
rect metal1 10.840 1.010 11.220 1.390
rect metal1 11.800 1.010 12.180 1.390
rect metal1 10.840 2.210 12.180 2.590
rect metal1 10.860 2.880 11.220 3.260
rect metal2 10.840 1.010 11.230 3.260
rect metal2 11.800 1.010 12.180 2.590
rect metal1 12.735 1.250 12.965 1.690
rect m2contact 13.200 1.070 13.460 1.330
rect metal1 13.140 1.010 13.520 1.390
rect metal2 13.140 1.010 13.520 2.560
rect metal1 13.695 1.250 13.925 1.690
rect m2contact 14.160 1.070 14.420 1.330
rect metal1 14.100 1.010 14.480 1.390
rect metal2 14.100 1.010 14.480 2.560
rect metal2 13.140 2.400 14.480 2.560
rect metal1 12.735 1.540 14.765 1.690
rect metal1 14.545 1.540 14.765 3.200
rect metal1 13.675 3.000 14.765 3.200
rect m2contact 13.220 2.940 13.480 3.200
rect metal1 13.170 2.880 13.530 3.260
rect metal2 13.160 2.400 13.540 3.260
rect polysilicon 13.015 1.440 14.125 1.650
rect polysilicon 12.805 1.650 13.165 2.200
rect pcontact 12.900 1.950 13.070 2.120
rect locali 12.820 1.940 13.150 2.130
rect viali 12.900 1.950 13.070 2.120
rect metal1 12.835 1.870 13.135 2.200
rect polysilicon 13.405 1.870 13.735 2.200
rect polysilicon 13.495 2.200 13.645 2.950
rect pcontact 13.485 1.950 13.655 2.120
rect locali 13.405 1.940 13.735 2.130
rect viali 13.485 1.950 13.655 2.120
rect metal1 13.420 1.870 13.720 2.200
rect metal1 15.495 1.250 15.725 1.690
rect m2contact 15.960 1.070 16.220 1.330
rect metal1 15.900 1.010 16.280 1.390
rect metal2 15.900 1.010 16.280 2.560
rect metal1 16.455 1.250 16.685 1.690
rect m2contact 16.920 1.070 17.180 1.330
rect metal1 16.860 1.010 17.240 1.390
rect metal2 16.860 1.010 17.240 2.560
rect metal2 15.900 2.400 17.240 2.560
rect metal1 15.495 1.540 17.525 1.690
rect metal1 17.305 1.540 17.525 3.200
rect metal1 16.435 3.000 17.525 3.200
rect m2contact 15.980 2.940 16.240 3.200
rect metal1 15.930 2.880 16.290 3.260
rect metal2 15.920 2.400 16.300 3.260
rect polysilicon 15.775 1.440 16.885 1.650
rect polysilicon 15.565 1.650 15.925 2.200
rect pcontact 15.660 1.950 15.830 2.120
rect locali 15.580 1.940 15.910 2.130
rect viali 15.660 1.950 15.830 2.120
rect metal1 15.595 1.870 15.895 2.200
rect polysilicon 16.165 1.870 16.495 2.200
rect polysilicon 16.255 2.200 16.405 2.950
rect pcontact 16.245 1.950 16.415 2.120
rect locali 16.165 1.940 16.495 2.130
rect viali 16.245 1.950 16.415 2.120
rect metal1 16.180 1.870 16.480 2.200
rect metal1 18.255 0.200 18.485 0.600
rect metal1 19.215 0.200 19.445 0.600
rect metal1 19.225 3.250 19.395 3.900
rect polysilicon 18.535 1.440 19.645 1.590
rect polysilicon 18.925 1.590 19.255 1.920
rect polysilicon 19.015 1.920 19.165 2.950
rect pcontact 19.005 1.670 19.175 1.840
rect locali 18.925 1.660 19.255 1.850
rect viali 19.005 1.670 19.175 1.840
rect metal1 18.940 1.600 19.240 1.920
rect m2contact 18.720 1.070 18.980 1.330
rect m2contact 19.680 1.070 19.940 1.330
rect m2contact 18.720 2.270 18.980 2.530
rect m2contact 19.680 2.270 19.940 2.530
rect m2contact 18.730 2.940 18.990 3.200
rect metal1 18.660 1.010 19.040 1.390
rect metal1 19.620 1.010 20.000 1.390
rect metal1 18.660 2.210 20.000 2.590
rect metal1 18.680 2.880 19.040 3.260
rect metal2 18.660 1.010 19.050 3.260
rect metal2 19.620 1.010 20.000 2.590
rect metal1 20.555 0.200 20.785 0.600
rect metal1 21.515 0.200 21.745 0.600
rect metal1 21.525 3.250 21.695 3.900
rect polysilicon 20.835 1.440 21.945 1.590
rect polysilicon 21.225 1.590 21.555 1.920
rect polysilicon 21.315 1.920 21.465 2.950
rect pcontact 21.305 1.670 21.475 1.840
rect locali 21.225 1.660 21.555 1.850
rect viali 21.305 1.670 21.475 1.840
rect metal1 21.240 1.600 21.540 1.920
rect m2contact 21.020 1.070 21.280 1.330
rect m2contact 21.980 1.070 22.240 1.330
rect m2contact 21.020 2.270 21.280 2.530
rect m2contact 21.980 2.270 22.240 2.530
rect m2contact 21.030 2.940 21.290 3.200
rect metal1 20.960 1.010 21.340 1.390
rect metal1 21.920 1.010 22.300 1.390
rect metal1 20.960 2.210 22.300 2.590
rect metal1 20.980 2.880 21.340 3.260
rect metal2 20.960 1.010 21.350 3.260
rect metal2 21.920 1.010 22.300 2.590
rect metal1 1.960 2.100 2.100 2.310
rect metal1 1.960 2.100 2.800 2.240
rect metal2 1.960 2.520 2.100 3.570
rect metal1 1.960 3.430 2.100 3.640
rect metal1 1.960 3.500 5.110 3.640
rect metal1 4.970 3.430 5.110 3.640
rect metal2 4.970 2.380 5.110 3.570
rect metal1 4.970 2.380 6.160 2.520
rect metal1 6.020 2.100 6.160 2.520
rect m2contact 1.900 3.370 2.160 3.630
rect metal1 1.840 3.310 2.220 3.690
rect metal2 1.840 3.310 2.220 3.690
rect m2contact 4.910 3.370 5.170 3.630
rect metal1 4.850 3.310 5.230 3.690
rect metal2 4.850 3.310 5.230 3.690
rect m2contact 4.910 2.320 5.170 2.580
rect metal1 4.850 2.260 5.230 2.640
rect metal2 4.850 2.260 5.230 2.640
rect metal1 6.020 2.100 6.160 2.730
rect metal1 5.530 2.590 6.160 2.730
rect metal1 5.530 2.590 5.670 3.640
rect metal1 5.530 3.500 8.260 3.640
rect metal1 8.120 3.430 8.260 3.640
rect metal2 8.120 3.430 12.040 3.570
rect metal2 11.900 2.870 12.040 3.570
rect metal1 11.900 2.870 13.020 3.010
rect metal1 12.880 2.380 13.020 3.010
rect metal1 12.880 2.380 13.510 2.520
rect metal1 13.370 2.100 13.510 2.520
rect m2contact 8.060 3.370 8.320 3.630
rect metal1 8.000 3.310 8.380 3.690
rect metal2 8.000 3.310 8.380 3.690
rect m2contact 11.840 2.810 12.100 3.070
rect metal1 11.780 2.750 12.160 3.130
rect metal2 11.780 2.750 12.160 3.130
rect metal1 13.370 2.100 13.510 2.730
rect metal1 12.880 2.590 13.510 2.730
rect metal1 12.880 2.590 13.020 3.640
rect metal1 12.880 3.500 15.190 3.640
rect metal1 15.050 3.430 15.190 3.640
rect metal2 15.050 2.100 15.190 3.570
rect metal1 15.050 2.100 15.680 2.240
rect m2contact 14.990 3.370 15.250 3.630
rect metal1 14.930 3.310 15.310 3.690
rect metal2 14.930 3.310 15.310 3.690
rect m2contact 14.990 2.040 15.250 2.300
rect metal1 14.930 1.980 15.310 2.360
rect metal2 14.930 1.980 15.310 2.360
rect metal2 9.800 1.540 9.940 1.680
rect metal1 9.800 1.540 11.200 1.680
rect m2contact 9.740 1.480 10.000 1.740
rect metal1 9.680 1.420 10.060 1.800
rect metal2 9.680 1.420 10.060 1.800
rect metal2 19.880 1.540 20.020 1.680
rect metal1 19.880 1.540 21.350 1.680
rect m2contact 19.820 1.480 20.080 1.740
rect metal1 19.760 1.420 20.140 1.800
rect metal2 19.760 1.420 20.140 1.800
rect metal1 14.630 1.470 15.610 1.610
rect metal1 17.430 1.540 19.040 1.680
rect metal1 6.930 0.700 7.840 0.840
rect metal2 7.700 0.700 10.920 0.840
rect metal2 10.780 0.700 10.920 1.120
rect m2contact 7.640 0.640 7.900 0.900
rect metal1 7.580 0.580 7.960 0.960
rect metal2 7.580 0.580 7.960 0.960
rect metal2 12.110 0.980 13.230 1.120
rect metal1 0.280 1.610 1.120 1.750
rect metal2 0.280 0.700 0.420 1.750
rect metal2 0.280 0.700 2.520 0.840
rect metal2 2.380 0.700 2.520 2.660
rect metal1 2.380 2.520 3.430 2.660
rect metal1 3.290 2.100 3.430 2.660
rect m2contact 0.220 1.550 0.480 1.810
rect metal1 0.160 1.490 0.540 1.870
rect metal2 0.160 1.490 0.540 1.870
rect m2contact 2.320 2.460 2.580 2.720
rect metal1 2.260 2.400 2.640 2.780
rect metal2 2.260 2.400 2.640 2.780
rect metal1 3.290 2.100 3.430 2.730
rect metal1 2.590 2.590 3.430 2.730
rect metal1 2.590 2.590 2.730 3.010
rect metal2 2.590 2.870 2.730 3.570
rect metal2 2.590 3.430 4.690 3.570
rect metal2 4.550 1.820 4.690 3.570
rect metal2 4.550 1.820 5.110 1.960
rect metal1 4.970 1.820 5.110 2.030
rect metal1 4.970 1.890 5.600 2.030
rect m2contact 2.530 2.810 2.790 3.070
rect metal1 2.470 2.750 2.850 3.130
rect metal2 2.470 2.750 2.850 3.130
rect m2contact 4.910 1.760 5.170 2.020
rect metal1 4.850 1.700 5.230 2.080
rect metal2 4.850 1.700 5.230 2.080
rect metal1 4.970 1.890 5.600 2.030
rect metal1 4.970 1.820 5.110 2.030
rect metal2 4.970 1.820 5.600 1.960
rect metal2 5.460 1.820 5.600 3.990
rect metal2 5.460 3.850 12.600 3.990
rect metal2 12.460 2.100 12.600 3.990
rect metal1 12.460 2.100 12.950 2.240
rect m2contact 4.910 1.760 5.170 2.020
rect metal1 4.850 1.700 5.230 2.080
rect metal2 4.850 1.700 5.230 2.080
rect m2contact 12.400 2.040 12.660 2.300
rect metal1 12.340 1.980 12.720 2.360
rect metal2 12.340 1.980 12.720 2.360
rect metal1 12.460 2.100 12.950 2.240
rect metal2 12.460 2.100 12.600 3.990
rect metal2 12.460 3.850 15.610 3.990
rect metal2 15.470 2.660 15.610 3.990
rect metal1 15.470 2.380 15.610 2.800
rect metal1 15.470 2.380 16.310 2.520
rect metal1 16.170 2.100 16.310 2.520
rect m2contact 12.400 2.040 12.660 2.300
rect metal1 12.340 1.980 12.720 2.360
rect metal2 12.340 1.980 12.720 2.360
rect m2contact 15.410 2.600 15.670 2.860
rect metal1 15.350 2.540 15.730 2.920
rect metal2 15.350 2.540 15.730 2.920
rect metal1 4.550 1.400 4.690 1.610
rect metal1 4.550 1.400 5.460 1.540
rect metal1 7.280 1.540 8.890 1.680
rect metal1 17.080 0.700 17.990 0.840
rect metal2 17.850 0.700 21.070 0.840
rect metal2 20.930 0.700 21.070 1.120
rect m2contact 17.790 0.640 18.050 0.900
rect metal1 17.730 0.580 18.110 0.960
rect metal2 17.730 0.580 18.110 0.960
rect metal1 5.530 2.520 6.020 2.590
rect metal1 13.020 2.520 13.370 2.590
rect metal1 15.610 2.520 15.730 2.540
rect metal1 12.720 1.980 12.835 2.100
rect metal1 2.730 2.730 2.850 2.750
rect metal1 9.680 1.390 9.880 1.420
rect metal1 19.760 1.390 20.000 1.420
rect metal2 10.780 1.120 10.840 1.150
rect metal1 11.060 1.680 11.120 1.740
rect metal2 12.180 1.120 12.250 1.150
rect metal2 13.090 1.120 13.140 1.150
rect metal1 13.510 2.200 13.560 2.240
rect metal1 15.680 2.200 15.740 2.240
rect metal1 16.310 2.200 16.320 2.240
rect metal1 18.900 1.680 18.940 1.740
rect metal2 1.920 2.590 1.960 2.660
rect metal1 2.060 2.310 2.100 2.350
rect metal2 20.930 1.120 20.960 1.150
rect metal1 21.210 1.680 21.240 1.740
rect metal1 2.800 2.200 2.860 2.240
rect metal1 3.430 2.200 3.440 2.240
rect metal1 4.645 1.610 4.690 1.680
rect metal1 6.160 2.200 6.200 2.240
rect metal1 8.750 1.680 8.820 1.740

# pins
pin CLK 1.000 1.600 1.300 1.920
pin D 3.050 2.880 3.410 3.260
pin QB 18.680 2.880 19.040 3.260
pin Q 20.980 2.880 21.340 3.260
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

# boundary
property FIXED_BBOX {0 0 2254 408}

# save
writeall force

# report
if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
