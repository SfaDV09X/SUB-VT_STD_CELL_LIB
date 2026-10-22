v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 190 1060 {}
P 4 1 180 1320 {}
N 240 1020 270 1020 {lab=A}
N 240 1100 270 1100 {lab=A}
N 240 1060 240 1100 {lab=A}
N 310 1060 310 1070 {lab=Abar}
N 310 1060 390 1060 {lab=Abar}
N 200 1060 240 1060 {lab=A}
N 310 1050 310 1060 {lab=Abar}
N 240 1020 240 1060 {lab=A}
N 310 1020 380 1020 {lab=VDD}
N 380 990 380 1020 {lab=VDD}
N 310 990 380 990 {lab=VDD}
N 310 1100 380 1100 {lab=GND}
N 380 1100 380 1130 {lab=GND}
N 310 1130 380 1130 {lab=GND}
N 310 970 310 990 {lab=VDD}
N 310 1130 310 1150 {lab=GND}
N 230 1280 260 1280 {lab=B}
N 230 1360 260 1360 {lab=B}
N 230 1320 230 1360 {lab=B}
N 300 1320 300 1330 {lab=Bbar}
N 300 1320 380 1320 {lab=Bbar}
N 190 1320 230 1320 {lab=B}
N 300 1310 300 1320 {lab=Bbar}
N 230 1280 230 1320 {lab=B}
N 300 1280 370 1280 {lab=VDD}
N 370 1250 370 1280 {lab=VDD}
N 300 1250 370 1250 {lab=VDD}
N 300 1360 370 1360 {lab=GND}
N 370 1360 370 1390 {lab=GND}
N 300 1390 370 1390 {lab=GND}
N 300 1230 300 1250 {lab=VDD}
N 300 1390 300 1410 {lab=GND}
N 570 1270 570 1320 {lab=#net1}
N 570 1380 570 1420 {lab=GND}
N 570 1420 800 1420 {lab=GND}
N 800 1380 800 1420 {lab=GND}
N 800 1270 800 1320 {lab=#net2}
N 570 1180 570 1210 {lab=Y}
N 570 1180 800 1180 {lab=Y}
N 800 1180 800 1210 {lab=Y}
N 570 950 570 960 {lab=#net3}
N 570 960 800 960 {lab=#net3}
N 800 950 800 960 {lab=#net3}
N 570 1010 570 1030 {lab=#net3}
N 570 1010 800 1010 {lab=#net3}
N 800 1010 800 1030 {lab=#net3}
N 690 960 690 1010 {lab=#net3}
N 570 1090 570 1120 {lab=Y}
N 570 1120 800 1120 {lab=Y}
N 800 1090 800 1120 {lab=Y}
N 690 1120 690 1180 {lab=Y}
N 570 850 570 880 {lab=VDD}
N 570 840 800 840 {lab=VDD}
N 800 840 800 890 {lab=VDD}
N 570 840 570 850 {lab=VDD}
N 570 880 570 890 {lab=VDD}
N 570 1350 600 1350 {lab=GND}
N 600 1350 600 1420 {lab=GND}
N 570 1240 610 1240 {lab=GND}
N 610 1240 610 1420 {lab=GND}
N 800 1350 820 1350 {lab=GND}
N 820 1350 820 1420 {lab=GND}
N 800 1420 820 1420 {lab=GND}
N 800 1240 860 1240 {lab=GND}
N 860 1240 860 1420 {lab=GND}
N 820 1420 860 1420 {lab=GND}
N 800 920 810 920 {lab=VDD}
N 810 840 810 920 {lab=VDD}
N 800 840 810 840 {lab=VDD}
N 800 1060 830 1060 {lab=VDD}
N 830 840 830 1050 {lab=VDD}
N 810 840 830 840 {lab=VDD}
N 830 1050 830 1060 {lab=VDD}
N 570 920 580 920 {lab=VDD}
N 580 840 580 920 {lab=VDD}
N 570 1060 600 1060 {lab=VDD}
N 600 840 600 1060 {lab=VDD}
N 490 920 530 920 {lab=A}
N 480 1060 530 1060 {lab=B}
N 490 1240 530 1240 {lab=A}
N 490 1350 530 1350 {lab=Bbar}
N 740 1240 760 1240 {lab=B}
N 730 1350 760 1350 {lab=Abar}
N 740 1060 760 1060 {lab=Abar}
N 740 920 760 920 {lab=Bbar}
N 740 1240 760 1240 {lab=B}
N 690 1140 700 1140 {lab=Y}
N 690 810 690 840 {lab=VDD}
N 700 1420 700 1460 {lab=GND}
N 700 1140 770 1140 {lab=Y}
C {sky130_fd_pr/nfet_01v8.sym} 290 1100 0 0 {name=M9
W=2.52
L=0.15
nf=3 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 290 1020 0 0 {name=M10
W=0.42
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {ipin.sym} 200 1060 0 0 {name=p1 lab=A}
C {ipin.sym} 190 1320 0 0 {name=p8 lab=B}
C {sky130_fd_pr/nfet_01v8.sym} 550 1240 0 0 {name=M2
W=5.04
L=0.15
nf=6 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 550 920 0 0 {name=M5
W=0.84
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {opin.sym} 770 1140 0 0 {name=p2 lab=Y}
C {iopin.sym} 690 810 0 0 {name=p5 lab=VDD}
C {iopin.sym} 700 1460 0 0 {name=p6 lab=GND}
C {lab_wire.sym} 310 970 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 390 1060 0 0 {name=p4 sig_type=std_logic lab=Abar}
C {lab_wire.sym} 310 1150 0 0 {name=p7 sig_type=std_logic lab=GND}
C {lab_wire.sym} 300 1230 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 380 1320 0 0 {name=p10 sig_type=std_logic lab=Bbar}
C {lab_wire.sym} 300 1410 0 0 {name=p11 sig_type=std_logic lab=GND}
C {lab_wire.sym} 490 920 0 0 {name=p12 sig_type=std_logic lab=A}
C {lab_wire.sym} 740 920 0 0 {name=p13 sig_type=std_logic lab=Bbar}
C {lab_wire.sym} 480 1060 0 0 {name=p14 sig_type=std_logic lab=B}
C {lab_wire.sym} 740 1060 0 0 {name=p15 sig_type=std_logic lab=Abar}
C {lab_wire.sym} 490 1240 0 0 {name=p16 sig_type=std_logic lab=A}
C {lab_wire.sym} 490 1350 0 0 {name=p17 sig_type=std_logic lab=Bbar}
C {lab_wire.sym} 740 1240 0 0 {name=p18 sig_type=std_logic lab=B}
C {lab_wire.sym} 730 1350 0 0 {name=p19 sig_type=std_logic lab=Abar}
C {sky130_fd_pr/pfet_01v8.sym} 280 1280 0 0 {name=M12
W=0.42
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 280 1360 0 0 {name=M11
W=2.52
L=0.15
nf=3 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 550 1350 0 0 {name=M1
W=5.04
L=0.15
nf=6 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 780 1350 0 0 {name=M3
W=5.04
L=0.15
nf=6 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 780 1240 0 0 {name=M4
W=5.04
L=0.15
nf=6 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 550 1060 0 0 {name=M6
W=0.84
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 780 1060 0 0 {name=M8
W=0.84
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 780 920 0 0 {name=M7
W=0.84
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
