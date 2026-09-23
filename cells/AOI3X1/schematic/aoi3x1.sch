v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -300 -490 -300 -450 {lab=#net1}
N -300 -560 -300 -540 {lab=Y}
N -300 -560 -120 -560 {lab=Y}
N -120 -560 -120 -530 {lab=Y}
N -300 -770 -300 -750 {lab=VDD}
N -130 -770 -120 -770 {lab=VDD}
N -210 -580 -210 -560 {lab=Y}
N -300 -770 -130 -770 {lab=VDD}
N -300 -720 -230 -720 {lab=VDD}
N -210 -600 -210 -580 {lab=Y}
N -200 -820 -200 -770 {lab=VDD}
N -230 -310 -230 -300 {lab=GND}
N -390 -510 -340 -510 {lab=A}
N -380 -720 -340 -720 {lab=A}
N -120 -690 -120 -680 {lab=#net2}
N -300 -690 -300 -680 {lab=#net2}
N -300 -680 -120 -680 {lab=#net2}
N -230 -750 -230 -740 {lab=VDD}
N -230 -740 -230 -730 {lab=VDD}
N -230 -770 -230 -750 {lab=VDD}
N -190 -770 -190 -640 {lab=VDD}
N -80 -720 -40 -720 {lab=B}
N -270 -630 -250 -630 {lab=C}
N -120 -770 -120 -750 {lab=VDD}
N -80 -500 -50 -500 {lab=C}
N -300 -450 -300 -410 {lab=#net1}
N -300 -350 -300 -340 {lab=GND}
N -300 -340 -300 -330 {lab=GND}
N -300 -330 -120 -330 {lab=GND}
N -120 -470 -120 -330 {lab=GND}
N -230 -330 -230 -310 {lab=GND}
N -370 -380 -340 -380 {lab=B}
N -210 -590 -130 -590 {lab=Y}
N -300 -380 -250 -380 {lab=GND}
N -300 -510 -250 -510 {lab=GND}
N -250 -500 -120 -500 {lab=GND}
N -250 -510 -250 -330 {lab=GND}
N -190 -640 -190 -630 {lab=VDD}
N -210 -630 -190 -630 {lab=VDD}
N -230 -730 -230 -720 {lab=VDD}
N -190 -720 -120 -720 {lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} -230 -630 0 0 {name=M1
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
C {sky130_fd_pr/pfet_01v8.sym} -320 -720 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} -100 -720 0 1 {name=M3
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
C {sky130_fd_pr/nfet_01v8.sym} -320 -510 0 0 {name=M4
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
C {sky130_fd_pr/nfet_01v8.sym} -100 -500 0 1 {name=M5
W=0.42
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
C {sky130_fd_pr/nfet_01v8.sym} -320 -380 0 0 {name=M6
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
C {iopin.sym} -200 -820 0 0 {name=p1 lab=VDD}
C {iopin.sym} -230 -300 0 1 {name=p2 lab=GND}
C {ipin.sym} -390 -510 0 0 {name=p3 lab=A}
C {ipin.sym} -370 -380 0 0 {name=p4 lab=B}
C {ipin.sym} -50 -500 0 1 {name=p5 lab=C}
C {opin.sym} -130 -590 0 0 {name=p9 lab=Y}
C {lab_wire.sym} -380 -720 0 0 {name=p6 sig_type=std_logic lab=A}
C {lab_wire.sym} -270 -630 0 0 {name=p7 sig_type=std_logic lab=C}
C {lab_wire.sym} -40 -720 0 0 {name=p8 sig_type=std_logic lab=B}
