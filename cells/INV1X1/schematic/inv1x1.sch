v {xschem version=3.4.8RC file_version=1.3}
G {}
K {.param WP=1u LP=0.15u WN=1u lN=0.15u}
V {}
S {}
F {}
E {}
P 4 1 -80 0 {}
N -30 -40 -0 -40 {lab=A}
N -30 40 -0 40 {lab=A}
N -30 -0 -30 40 {lab=A}
N 40 -0 40 10 {lab=Y}
N 40 -0 120 0 {lab=Y}
N -70 -0 -30 -0 {lab=A}
N 40 -10 40 -0 {lab=Y}
N -30 -40 -30 -0 {lab=A}
N 40 -40 110 -40 {lab=VDD}
N 110 -70 110 -40 {lab=VDD}
N 40 -70 110 -70 {lab=VDD}
N 40 40 110 40 {lab=GND}
N 110 40 110 70 {lab=GND}
N 40 70 110 70 {lab=GND}
N 40 -90 40 -70 {lab=VDD}
N 40 70 40 90 {lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 20 40 0 0 {name=M1
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
C {sky130_fd_pr/pfet_01v8.sym} 20 -40 0 0 {name=M2
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
C {ipin.sym} -70 0 0 0 {name=p1 lab=A}
C {opin.sym} 120 0 0 0 {name=p2 lab=Y}
C {iopin.sym} 40 -90 0 0 {name=p3 lab=VDD}
C {iopin.sym} 40 90 0 0 {name=p4 lab=GND}
