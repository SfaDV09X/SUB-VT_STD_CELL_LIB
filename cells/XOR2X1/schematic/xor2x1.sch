v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 -530 -90 {}
P 4 1 -540 170 {}
N -170 70 -170 120 {lab=#net1}
N -170 180 -170 220 {lab=GND}
N -170 220 60 220 {lab=GND}
N 60 180 60 220 {lab=GND}
N 60 70 60 120 {lab=#net2}
N -170 -20 -170 10 {lab=Y}
N -170 -20 60 -20 {lab=Y}
N 60 -20 60 10 {lab=Y}
N -170 -250 -170 -240 {lab=#net3}
N -170 -240 60 -240 {lab=#net3}
N 60 -250 60 -240 {lab=#net3}
N -170 -190 -170 -170 {lab=#net3}
N -170 -190 60 -190 {lab=#net3}
N 60 -190 60 -170 {lab=#net3}
N -50 -240 -50 -190 {lab=#net3}
N -170 -110 -170 -80 {lab=Y}
N -170 -80 60 -80 {lab=Y}
N 60 -110 60 -80 {lab=Y}
N -50 -80 -50 -20 {lab=Y}
N -170 -350 -170 -320 {lab=VDD}
N -170 -360 60 -360 {lab=VDD}
N 60 -360 60 -310 {lab=VDD}
N -170 -360 -170 -350 {lab=VDD}
N -170 -320 -170 -310 {lab=VDD}
N -170 150 -140 150 {lab=GND}
N -140 150 -140 220 {lab=GND}
N -170 40 -130 40 {lab=GND}
N -130 40 -130 220 {lab=GND}
N 60 150 80 150 {lab=GND}
N 80 150 80 220 {lab=GND}
N 60 220 80 220 {lab=GND}
N 60 40 120 40 {lab=GND}
N 120 40 120 220 {lab=GND}
N 80 220 120 220 {lab=GND}
N 60 -280 70 -280 {lab=VDD}
N 70 -360 70 -280 {lab=VDD}
N 60 -360 70 -360 {lab=VDD}
N 60 -140 90 -140 {lab=VDD}
N 90 -360 90 -150 {lab=VDD}
N 70 -360 90 -360 {lab=VDD}
N 90 -150 90 -140 {lab=VDD}
N -170 -280 -160 -280 {lab=VDD}
N -160 -360 -160 -280 {lab=VDD}
N -170 -140 -140 -140 {lab=VDD}
N -140 -360 -140 -140 {lab=VDD}
N -250 -280 -210 -280 {lab=A}
N -260 -140 -210 -140 {lab=Abar}
N -250 40 -210 40 {lab=A}
N -250 150 -210 150 {lab=B}
N 0 40 20 40 {lab=Abar}
N -10 150 20 150 {lab=Bbar}
N 0 -140 20 -140 {lab=Bbar}
N 0 -280 20 -280 {lab=B}
N 0 40 20 40 {lab=Abar}
N -480 -130 -450 -130 {lab=A}
N -480 -50 -450 -50 {lab=A}
N -480 -90 -480 -50 {lab=A}
N -410 -90 -410 -80 {lab=Abar}
N -410 -90 -330 -90 {lab=Abar}
N -520 -90 -480 -90 {lab=A}
N -410 -100 -410 -90 {lab=Abar}
N -480 -130 -480 -90 {lab=A}
N -410 -130 -340 -130 {lab=VDD}
N -340 -160 -340 -130 {lab=VDD}
N -410 -160 -340 -160 {lab=VDD}
N -410 -50 -340 -50 {lab=GND}
N -340 -50 -340 -20 {lab=GND}
N -410 -20 -340 -20 {lab=GND}
N -410 -180 -410 -160 {lab=VDD}
N -410 -20 -410 0 {lab=GND}
N -50 -60 -40 -60 {lab=Y}
N -40 -60 180 -60 {lab=Y}
N -490 130 -460 130 {lab=B}
N -490 210 -460 210 {lab=B}
N -490 170 -490 210 {lab=B}
N -420 170 -420 180 {lab=Bbar}
N -420 170 -340 170 {lab=Bbar}
N -530 170 -490 170 {lab=B}
N -420 160 -420 170 {lab=Bbar}
N -490 130 -490 170 {lab=B}
N -420 130 -350 130 {lab=VDD}
N -350 100 -350 130 {lab=VDD}
N -420 100 -350 100 {lab=VDD}
N -420 210 -350 210 {lab=GND}
N -350 210 -350 240 {lab=GND}
N -420 240 -350 240 {lab=GND}
N -420 80 -420 100 {lab=VDD}
N -420 240 -420 260 {lab=GND}
N -30 220 -30 260 {lab=GND}
N -50 -390 -50 -360 {lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} -190 40 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} -190 -280 0 0 {name=M5
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
C {sky130_fd_pr/nfet_01v8.sym} -430 -50 0 0 {name=M9
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
C {sky130_fd_pr/pfet_01v8.sym} -430 -130 0 0 {name=M10
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
C {ipin.sym} -520 -90 0 0 {name=p1 lab=A}
C {opin.sym} 180 -60 0 0 {name=p2 lab=Y}
C {iopin.sym} -50 -390 0 0 {name=p5 lab=VDD}
C {iopin.sym} -30 260 0 0 {name=p6 lab=GND}
C {ipin.sym} -530 170 0 0 {name=p8 lab=B}
C {lab_wire.sym} -410 -180 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -330 -90 0 0 {name=p4 sig_type=std_logic lab=Abar}
C {lab_wire.sym} -410 0 0 0 {name=p7 sig_type=std_logic lab=GND}
C {lab_wire.sym} -420 80 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -340 170 0 0 {name=p10 sig_type=std_logic lab=Bbar}
C {lab_wire.sym} -420 260 0 0 {name=p11 sig_type=std_logic lab=GND}
C {lab_wire.sym} -250 -280 0 0 {name=p12 sig_type=std_logic lab=A}
C {lab_wire.sym} -260 -140 0 0 {name=p13 sig_type=std_logic lab=Abar}
C {lab_wire.sym} 0 -280 0 0 {name=p14 sig_type=std_logic lab=B}
C {lab_wire.sym} 0 -140 0 0 {name=p15 sig_type=std_logic lab=Bbar}
C {lab_wire.sym} -250 40 0 0 {name=p16 sig_type=std_logic lab=A}
C {lab_wire.sym} -250 150 0 0 {name=p17 sig_type=std_logic lab=B}
C {lab_wire.sym} 0 40 0 0 {name=p18 sig_type=std_logic lab=Abar}
C {lab_wire.sym} -10 150 0 0 {name=p19 sig_type=std_logic lab=Bbar}
C {sky130_fd_pr/pfet_01v8.sym} -190 -140 0 0 {name=M6
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
C {sky130_fd_pr/pfet_01v8.sym} 40 -140 0 0 {name=M8
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
C {sky130_fd_pr/pfet_01v8.sym} 40 -280 0 0 {name=M7
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
C {sky130_fd_pr/nfet_01v8.sym} -190 150 0 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} 40 40 0 0 {name=M4
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
C {sky130_fd_pr/nfet_01v8.sym} 40 150 0 0 {name=M3
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
C {sky130_fd_pr/pfet_01v8.sym} -440 130 0 0 {name=M12
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
C {sky130_fd_pr/nfet_01v8.sym} -440 210 0 0 {name=M11
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
