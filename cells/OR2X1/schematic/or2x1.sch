v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 280 1290 280 1320 {lab=#net1}
N 280 1290 470 1290 {lab=#net1}
N 470 1290 470 1320 {lab=#net1}
N 370 1190 370 1290 {lab=#net1}
N 370 1060 370 1130 {lab=#net2}
N 270 1030 330 1030 {lab=A}
N 280 1160 330 1160 {lab=#net3}
N 370 900 370 1000 {lab=VDD}
N 370 1030 400 1030 {lab=VDD}
N 400 990 400 1030 {lab=VDD}
N 370 990 400 990 {lab=VDD}
N 370 1160 440 1160 {lab=VDD}
N 440 960 440 1160 {lab=VDD}
N 370 960 440 960 {lab=VDD}
N 400 1350 430 1350 {lab=B}
N 210 1350 240 1350 {lab=A}
N 280 1380 280 1400 {lab=GND}
N 280 1400 470 1400 {lab=GND}
N 470 1380 470 1400 {lab=GND}
N 280 1350 320 1350 {lab=GND}
N 320 1350 320 1400 {lab=GND}
N 470 1350 520 1350 {lab=GND}
N 520 1350 520 1400 {lab=GND}
N 470 1400 520 1400 {lab=GND}
N 370 1400 370 1460 {lab=GND}
N 370 1230 490 1230 {lab=#net1}
N 490 1230 530 1230 {lab=#net1}
N 530 1230 530 1300 {lab=#net1}
N 530 1300 590 1300 {lab=#net1}
N 530 1110 530 1230 {lab=#net1}
N 530 1110 590 1110 {lab=#net1}
N 630 1140 630 1270 {lab=Y}
N 630 1330 630 1410 {lab=GND}
N 370 1410 630 1410 {lab=GND}
N 630 1300 650 1300 {lab=GND}
N 650 1300 650 1430 {lab=GND}
N 370 1430 650 1430 {lab=GND}
N 630 950 630 1080 {lab=VDD}
N 370 950 630 950 {lab=VDD}
N 630 1110 660 1110 {lab=VDD}
N 660 1100 660 1110 {lab=VDD}
N 660 940 660 1100 {lab=VDD}
N 370 940 660 940 {lab=VDD}
N 630 1230 830 1230 {lab=Y}
C {sky130_fd_pr/nfet_01v8.sym} 260 1350 0 0 {name=M1
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 450 1350 0 0 {name=M2
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 350 1030 0 0 {name=M3
W=2.52
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
C {sky130_fd_pr/pfet_01v8.sym} 350 1160 0 0 {name=M4
W=2.52
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
C {ipin.sym} 210 1350 0 0 {name=p3 lab=A}
C {ipin.sym} 400 1350 0 0 {name=p4 lab=B}
C {iopin.sym} 370 900 0 0 {name=p5 lab=VDD}
C {iopin.sym} 370 1460 0 0 {name=p6 lab=GND}
C {opin.sym} 830 1230 0 0 {name=p7 lab=Y}
C {sky130_fd_pr/pfet_01v8.sym} 610 1110 0 0 {name=M5
W=1.26
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
C {sky130_fd_pr/nfet_01v8.sym} 610 1300 0 0 {name=M6
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
model=nfet_01v8
spiceprefix=X
}
C {lab_wire.sym} 270 1030 0 0 {name=p1 sig_type=std_logic lab=A}
C {lab_wire.sym} 280 1160 0 0 {name=p2 sig_type=std_logic lab=B}
