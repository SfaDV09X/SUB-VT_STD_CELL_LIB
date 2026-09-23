v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -460 -500 -240 -500 {lab=Y}
N -320 -410 -320 -390 {lab=Y}
N -320 -500 -320 -410 {lab=Y}
N -320 -330 -320 -300 {lab=#net1}
N -320 -240 -320 -200 {lab=GND}
N -460 -560 -240 -560 {lab=VDD}
N -460 -530 -430 -530 {lab=VDD}
N -430 -560 -430 -530 {lab=VDD}
N -240 -530 -230 -530 {lab=VDD}
N -230 -530 -210 -530 {lab=VDD}
N -210 -560 -210 -530 {lab=VDD}
N -240 -560 -210 -560 {lab=VDD}
N -310 -530 -280 -530 {lab=B}
N -390 -360 -360 -360 {lab=A}
N -390 -270 -360 -270 {lab=#net2}
N -320 -360 -240 -360 {lab=GND}
N -240 -360 -240 -220 {lab=GND}
N -320 -220 -240 -220 {lab=GND}
N -320 -270 -280 -270 {lab=GND}
N -280 -270 -280 -230 {lab=GND}
N -320 -230 -280 -230 {lab=GND}
N -340 -590 -340 -560 {lab=VDD}
N -520 -530 -500 -530 {lab=A}
N -530 -530 -520 -530 {lab=A}
N -320 -440 -170 -440 {lab=Y}
N -170 -440 -160 -440 {lab=Y}
N -340 -640 -340 -590 {lab=VDD}
N -320 -200 -320 -130 {lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} -340 -270 0 0 {name=M1
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} -340 -360 0 0 {name=M2
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} -480 -530 0 0 {name=M3
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
C {sky130_fd_pr/pfet_01v8.sym} -260 -530 0 0 {name=M4
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
C {ipin.sym} -530 -530 0 0 {name=p1 lab=A}
C {ipin.sym} -310 -530 0 0 {name=p2 lab=B
}
C {iopin.sym} -340 -640 0 0 {name=p6 lab=VDD}
C {iopin.sym} -320 -130 0 0 {name=p8 lab=GND}
C {opin.sym} -160 -440 0 0 {name=p5 lab=Y}
C {lab_wire.sym} -390 -360 0 0 {name=p3 sig_type=std_logic lab=A}
C {lab_wire.sym} -390 -270 0 0 {name=p4 sig_type=std_logic lab=B}
