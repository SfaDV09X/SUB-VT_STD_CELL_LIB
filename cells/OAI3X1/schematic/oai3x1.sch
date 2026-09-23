v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -80 -360 -80 -320 {lab=#net1}
N 100 -340 100 -320 {lab=#net1}
N -80 -320 100 -320 {lab=#net1}
N -10 -320 -10 -280 {lab=#net1}
N -80 -430 -80 -410 {lab=Y}
N -80 -430 100 -430 {lab=Y}
N 100 -430 100 -400 {lab=Y}
N -80 -480 -80 -470 {lab=Y}
N -80 -470 100 -470 {lab=Y}
N 100 -530 100 -470 {lab=Y}
N -80 -560 -80 -540 {lab=#net2}
N -80 -640 -80 -620 {lab=VDD}
N 100 -640 100 -590 {lab=VDD}
N 90 -640 100 -640 {lab=VDD}
N 10 -450 10 -430 {lab=Y}
N -80 -640 90 -640 {lab=VDD}
N -10 -610 -10 -520 {lab=VDD}
N -10 -640 -10 -610 {lab=VDD}
N 60 -640 60 -570 {lab=VDD}
N 0 -210 140 -210 {lab=GND}
N 10 -470 10 -450 {lab=Y}
N 20 -690 20 -640 {lab=VDD}
N -10 -180 -10 -170 {lab=GND}
N -10 -220 -10 -180 {lab=GND}
N -10 -190 0 -190 {lab=GND}
N -170 -380 -120 -380 {lab=A}
N -70 -250 -50 -250 {lab=C}
N -90 -250 -70 -250 {lab=C}
N 50 -370 60 -370 {lab=B}
N -150 -510 -120 -510 {lab=B}
N -160 -590 -120 -590 {lab=A}
N 140 -560 170 -560 {lab=C}
N 10 -450 100 -450 {lab=Y}
N 60 -570 60 -560 {lab=VDD}
N 60 -560 100 -560 {lab=VDD}
N -80 -590 -10 -590 {lab=VDD}
N -80 -510 -10 -510 {lab=VDD}
N -10 -520 -10 -510 {lab=VDD}
N -10 -250 -0 -250 {lab=GND}
N -80 -380 -0 -380 {lab=GND}
N -0 -380 0 -190 {lab=GND}
N 100 -370 140 -370 {lab=GND}
N 140 -370 140 -210 {lab=GND}
C {sky130_fd_pr/pfet_01v8.sym} -100 -510 0 0 {name=M1
W=2.52
L=0.15
body=VDD
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
C {sky130_fd_pr/pfet_01v8.sym} -100 -590 0 0 {name=M2
W=2.52
L=0.15
body=VDD
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
C {sky130_fd_pr/pfet_01v8.sym} 120 -560 0 1 {name=M3
W=1.26
L=0.15
body=VDD
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
C {sky130_fd_pr/nfet_01v8.sym} -100 -380 0 0 {name=M4
W=0.84
L=0.15
body=GND
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
C {sky130_fd_pr/nfet_01v8.sym} 80 -370 0 0 {name=M5
W=0.84
L=0.15
body=GND
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
C {sky130_fd_pr/nfet_01v8.sym} -30 -250 0 0 {name=M6
W=0.84
L=0.15
body=GND
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
C {iopin.sym} 20 -690 0 0 {name=p1 lab=VDD}
C {iopin.sym} -10 -170 0 1 {name=p2 lab=GND}
C {ipin.sym} -170 -380 0 0 {name=p3 lab=A}
C {ipin.sym} 50 -370 0 0 {name=p4 lab=B}
C {ipin.sym} -90 -250 0 0 {name=p5 lab=C}
C {opin.sym} 100 -450 0 0 {name=p9 lab=Y}
C {lab_wire.sym} -160 -590 0 0 {name=p6 sig_type=std_logic lab=A}
C {lab_wire.sym} 170 -560 0 0 {name=p7 sig_type=std_logic lab=C}
C {lab_wire.sym} -150 -510 0 0 {name=p8 sig_type=std_logic lab=B}
