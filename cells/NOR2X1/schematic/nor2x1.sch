v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 310 1190 310 1220 {lab=Y}
N 310 1190 500 1190 {lab=Y}
N 500 1190 500 1220 {lab=Y}
N 400 1090 400 1190 {lab=Y}
N 400 960 400 1030 {lab=#net1}
N 300 930 360 930 {lab=A}
N 310 1060 360 1060 {lab=xxx}
N 400 800 400 900 {lab=VDD}
N 400 930 430 930 {lab=VDD}
N 430 890 430 930 {lab=VDD}
N 400 890 430 890 {lab=VDD}
N 400 1060 470 1060 {lab=VDD}
N 470 860 470 1060 {lab=VDD}
N 400 860 470 860 {lab=VDD}
N 430 1250 460 1250 {lab=B}
N 240 1250 270 1250 {lab=A}
N 310 1280 310 1300 {lab=GND}
N 310 1300 500 1300 {lab=GND}
N 500 1280 500 1300 {lab=GND}
N 310 1250 350 1250 {lab=GND}
N 350 1250 350 1300 {lab=GND}
N 500 1250 550 1250 {lab=GND}
N 550 1250 550 1300 {lab=GND}
N 500 1300 550 1300 {lab=GND}
N 400 1300 400 1360 {lab=GND}
N 400 1130 520 1130 {lab=Y}
C {sky130_fd_pr/nfet_01v8.sym} 290 1250 0 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} 480 1250 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} 380 930 0 0 {name=M3
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
C {sky130_fd_pr/pfet_01v8.sym} 380 1060 0 0 {name=M4
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
C {ipin.sym} 240 1250 0 0 {name=p3 lab=A}
C {ipin.sym} 430 1250 0 0 {name=p4 lab=B}
C {iopin.sym} 400 800 0 0 {name=p5 lab=VDD}
C {iopin.sym} 400 1360 0 0 {name=p6 lab=GND}
C {opin.sym} 520 1130 0 0 {name=p7 lab=Y}
C {lab_wire.sym} 300 930 0 0 {name=p1 sig_type=std_logic lab=A}
C {lab_wire.sym} 310 1060 0 0 {name=p2 sig_type=std_logic lab=B}
