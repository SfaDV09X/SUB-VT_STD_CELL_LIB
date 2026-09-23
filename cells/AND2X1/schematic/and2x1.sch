v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -90 -210 130 -210 {lab=#net1}
N 50 -120 50 -100 {lab=#net1}
N 50 -210 50 -120 {lab=#net1}
N 50 -40 50 -10 {lab=#net2}
N 50 50 50 90 {lab=GND}
N -90 -270 130 -270 {lab=VDD}
N -90 -240 -60 -240 {lab=VDD}
N -60 -270 -60 -240 {lab=VDD}
N 130 -240 140 -240 {lab=VDD}
N 140 -240 160 -240 {lab=VDD}
N 160 -270 160 -240 {lab=VDD}
N 130 -270 160 -270 {lab=VDD}
N 60 -240 90 -240 {lab=B}
N -20 -70 10 -70 {lab=A}
N -20 20 10 20 {lab=#net3}
N 50 -70 130 -70 {lab=GND}
N 130 -70 130 70 {lab=GND}
N 50 70 130 70 {lab=GND}
N 50 20 90 20 {lab=GND}
N 90 20 90 60 {lab=GND}
N 50 60 90 60 {lab=GND}
N 30 -300 30 -270 {lab=VDD}
N -150 -240 -130 -240 {lab=A}
N -160 -240 -150 -240 {lab=A}
N 50 -150 200 -150 {lab=#net1}
N 200 -150 210 -150 {lab=#net1}
N 210 -150 210 -50 {lab=#net1}
N 210 -50 260 -50 {lab=#net1}
N 210 -200 210 -150 {lab=#net1}
N 210 -200 260 -200 {lab=#net1}
N 300 -170 300 -80 {lab=Y}
N 300 -20 300 70 {lab=GND}
N 30 -350 30 -300 {lab=VDD}
N 50 90 50 160 {lab=GND}
N 300 70 300 120 {lab=GND}
N 50 120 300 120 {lab=GND}
N 300 -50 340 -50 {lab=GND}
N 340 -50 340 130 {lab=GND}
N 50 130 340 130 {lab=GND}
N 300 -290 300 -230 {lab=VDD}
N 30 -290 300 -290 {lab=VDD}
N 300 -200 340 -200 {lab=VDD}
N 340 -300 340 -200 {lab=VDD}
N 300 -130 390 -130 {lab=Y}
N 30 -300 340 -300 {lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} 30 20 0 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} 30 -70 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} -110 -240 0 0 {name=M3
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
C {sky130_fd_pr/pfet_01v8.sym} 110 -240 0 0 {name=M4
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
C {ipin.sym} -160 -240 0 0 {name=p1 lab=A}
C {ipin.sym} 60 -240 0 0 {name=p2 lab=B
}
C {iopin.sym} 30 -350 0 0 {name=p6 lab=VDD}
C {iopin.sym} 50 160 0 0 {name=p8 lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 280 -50 0 0 {name=M5
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
C {sky130_fd_pr/pfet_01v8.sym} 280 -200 0 0 {name=M6
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
C {opin.sym} 380 -130 0 0 {name=p5 lab=Y

}
C {lab_wire.sym} -20 -70 0 0 {name=p3 sig_type=std_logic lab=A}
C {lab_wire.sym} -20 20 0 0 {name=p4 sig_type=std_logic lab=B}
