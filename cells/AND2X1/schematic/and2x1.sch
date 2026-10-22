v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -250 -410 -30 -410 {lab=#net1}
N -110 -320 -110 -300 {lab=#net1}
N -110 -410 -110 -320 {lab=#net1}
N -110 -240 -110 -210 {lab=#net2}
N -110 -150 -110 -110 {lab=GND}
N -250 -470 -30 -470 {lab=VDD}
N -250 -440 -220 -440 {lab=VDD}
N -220 -470 -220 -440 {lab=VDD}
N -30 -440 -20 -440 {lab=VDD}
N -20 -440 0 -440 {lab=VDD}
N 0 -470 0 -440 {lab=VDD}
N -30 -470 0 -470 {lab=VDD}
N -100 -440 -70 -440 {lab=B}
N -180 -270 -150 -270 {lab=A}
N -180 -180 -150 -180 {lab=B}
N -110 -270 -30 -270 {lab=GND}
N -30 -270 -30 -130 {lab=GND}
N -110 -130 -30 -130 {lab=GND}
N -110 -180 -70 -180 {lab=GND}
N -70 -180 -70 -140 {lab=GND}
N -110 -140 -70 -140 {lab=GND}
N -130 -500 -130 -470 {lab=VDD}
N -310 -440 -290 -440 {lab=A}
N -320 -440 -310 -440 {lab=A}
N -110 -350 40 -350 {lab=#net1}
N 40 -350 50 -350 {lab=#net1}
N 50 -350 50 -250 {lab=#net1}
N 50 -250 100 -250 {lab=#net1}
N 50 -400 50 -350 {lab=#net1}
N 50 -400 100 -400 {lab=#net1}
N 140 -370 140 -280 {lab=Y}
N 140 -220 140 -130 {lab=GND}
N -130 -550 -130 -500 {lab=VDD}
N -110 -110 -110 -40 {lab=GND}
N 140 -130 140 -80 {lab=GND}
N -110 -80 140 -80 {lab=GND}
N 140 -250 180 -250 {lab=GND}
N 180 -250 180 -70 {lab=GND}
N -110 -70 180 -70 {lab=GND}
N 140 -490 140 -430 {lab=VDD}
N -130 -490 140 -490 {lab=VDD}
N 140 -400 180 -400 {lab=VDD}
N 180 -500 180 -400 {lab=VDD}
N 140 -330 230 -330 {lab=Y}
N -130 -500 180 -500 {lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} -130 -270 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} -270 -440 0 0 {name=M3
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
C {ipin.sym} -320 -440 0 0 {name=p1 lab=A}
C {ipin.sym} -100 -440 0 0 {name=p2 lab=B
}
C {iopin.sym} -130 -550 0 0 {name=p6 lab=VDD}
C {iopin.sym} -110 -40 0 0 {name=p8 lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 120 -250 0 0 {name=M5
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
C {opin.sym} 220 -330 0 0 {name=p5 lab=Y

}
C {lab_wire.sym} -180 -270 0 0 {name=p3 sig_type=std_logic lab=A}
C {lab_wire.sym} -180 -180 0 0 {name=p4 sig_type=std_logic lab=B}
C {sky130_fd_pr/pfet_01v8.sym} -50 -440 0 0 {name=M4
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
C {sky130_fd_pr/pfet_01v8.sym} 120 -400 0 0 {name=M6
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
C {sky130_fd_pr/nfet_01v8.sym} -130 -180 0 0 {name=M1
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
