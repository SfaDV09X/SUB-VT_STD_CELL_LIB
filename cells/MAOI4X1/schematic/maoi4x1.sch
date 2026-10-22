v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 -530 -150 {}
P 4 1 -540 110 {}
P 4 1 360 -30 {}
N -480 -190 -450 -190 {lab=A}
N -480 -110 -450 -110 {lab=A}
N -480 -150 -480 -110 {lab=A}
N -410 -150 -410 -140 {lab=Anot}
N -410 -150 -330 -150 {lab=Anot}
N -520 -150 -480 -150 {lab=A}
N -410 -160 -410 -150 {lab=Anot}
N -480 -190 -480 -150 {lab=A}
N -410 -190 -340 -190 {lab=VDD}
N -340 -220 -340 -190 {lab=VDD}
N -410 -110 -340 -110 {lab=GND}
N -340 -110 -340 -80 {lab=GND}
N -410 -240 -410 -220 {lab=VDD}
N -410 -80 -410 -60 {lab=GND}
N -490 70 -460 70 {lab=B}
N -490 150 -460 150 {lab=B}
N -490 110 -490 150 {lab=B}
N -420 110 -420 120 {lab=Bnot}
N -420 110 -340 110 {lab=Bnot}
N -530 110 -490 110 {lab=B}
N -420 100 -420 110 {lab=Bnot}
N -490 70 -490 110 {lab=B}
N -420 70 -350 70 {lab=VDD}
N -350 40 -350 70 {lab=VDD}
N -420 150 -350 150 {lab=GND}
N -350 150 -350 180 {lab=GND}
N -420 20 -420 40 {lab=VDD}
N -420 180 -420 200 {lab=GND}
N -50 100 -50 150 {lab=#net1}
N -50 210 -50 250 {lab=GND}
N -50 250 180 250 {lab=GND}
N 180 210 180 250 {lab=GND}
N 180 100 180 150 {lab=#net2}
N -50 10 -50 40 {lab=Y}
N -50 10 180 10 {lab=Y}
N 180 10 180 40 {lab=Y}
N -50 -220 -50 -210 {lab=#net3}
N -50 -210 180 -210 {lab=#net3}
N 180 -220 180 -210 {lab=#net3}
N -50 -160 -50 -140 {lab=#net3}
N -50 -160 180 -160 {lab=#net3}
N 180 -160 180 -140 {lab=#net3}
N 70 -210 70 -160 {lab=#net3}
N -50 -80 -50 -50 {lab=Y}
N -50 -50 180 -50 {lab=Y}
N 180 -80 180 -50 {lab=Y}
N 70 -50 70 10 {lab=Y}
N -50 -320 -50 -290 {lab=VDD}
N -50 -330 180 -330 {lab=VDD}
N 180 -330 180 -280 {lab=VDD}
N -50 -330 -50 -320 {lab=VDD}
N -50 -290 -50 -280 {lab=VDD}
N -50 180 -20 180 {lab=GND}
N -20 180 -20 250 {lab=GND}
N -50 70 -10 70 {lab=GND}
N -10 70 -10 250 {lab=GND}
N 180 180 200 180 {lab=GND}
N 200 180 200 250 {lab=GND}
N 180 250 200 250 {lab=GND}
N 180 70 240 70 {lab=GND}
N 240 70 240 250 {lab=GND}
N 200 250 240 250 {lab=GND}
N 180 -250 190 -250 {lab=VDD}
N 190 -330 190 -250 {lab=VDD}
N 180 -330 190 -330 {lab=VDD}
N 180 -110 210 -110 {lab=VDD}
N 210 -330 210 -120 {lab=VDD}
N 190 -330 210 -330 {lab=VDD}
N 210 -120 210 -110 {lab=VDD}
N -50 -250 -40 -250 {lab=VDD}
N -40 -330 -40 -250 {lab=VDD}
N -50 -110 -20 -110 {lab=VDD}
N -20 -330 -20 -110 {lab=VDD}
N -130 -250 -90 -250 {lab=Anot}
N -140 -110 -90 -110 {lab=C}
N -130 70 -90 70 {lab=Anot}
N -130 180 -90 180 {lab=Bnot}
N 120 70 140 70 {lab=C}
N 110 180 140 180 {lab=D}
N 120 -110 140 -110 {lab=D}
N 120 -250 140 -250 {lab=Bnot}
N 120 70 140 70 {lab=C}
N 70 -30 80 -30 {lab=Y}
N 80 -30 300 -30 {lab=Y}
N 370 -30 410 -30 {lab=Y}
N 300 -30 370 -30 {lab=Y}
N -410 -270 -410 -240 {lab=VDD}
N -340 -240 -340 -220 {lab=VDD}
N -410 -240 -340 -240 {lab=VDD}
N -420 0 -420 20 {lab=VDD}
N -350 30 -350 40 {lab=VDD}
N -420 30 -350 30 {lab=VDD}
N -420 200 -420 220 {lab=GND}
N -350 180 -350 190 {lab=GND}
N -420 190 -350 190 {lab=GND}
N -410 -60 -410 -40 {lab=GND}
N -340 -80 -340 -60 {lab=GND}
N -410 -60 -340 -60 {lab=GND}
N 90 250 90 290 {lab=GND}
N 70 -360 70 -330 {lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} -430 -110 0 0 {name=M9
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
C {ipin.sym} -520 -150 0 0 {name=p1 lab=A}
C {iopin.sym} -410 -270 0 0 {name=p3 lab=VDD}
C {iopin.sym} -410 -40 0 0 {name=p4 lab=GND}
C {lab_pin.sym} -330 -150 0 1 {name=p7 sig_type=std_logic lab=Anot}
C {ipin.sym} -530 110 0 0 {name=p8 lab=B}
C {lab_pin.sym} -340 110 0 1 {name=p11 sig_type=std_logic lab=Bnot}
C {sky130_fd_pr/nfet_01v8.sym} -70 70 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} -70 -250 0 0 {name=M5
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
C {opin.sym} 410 -30 0 0 {name=p2 lab=Y}
C {ipin.sym} 110 180 0 0 {name=p13 lab=D}
C {ipin.sym} 120 70 0 0 {name=p15 lab=C}
C {lab_wire.sym} -140 -110 0 0 {name=p20 sig_type=std_logic lab=C}
C {lab_wire.sym} 120 -110 0 0 {name=p18 sig_type=std_logic lab=D}
C {lab_pin.sym} -130 180 0 0 {name=p19 sig_type=std_logic lab=Bnot}
C {lab_pin.sym} 120 -250 0 0 {name=p23 sig_type=std_logic lab=Bnot}
C {lab_pin.sym} -130 -250 0 0 {name=p14 sig_type=std_logic lab=Anot}
C {lab_pin.sym} -130 70 0 0 {name=p16 sig_type=std_logic lab=Anot}
C {lab_wire.sym} -420 220 0 1 {name=p9 sig_type=std_logic lab=GND}
C {lab_wire.sym} 90 290 0 1 {name=p12 sig_type=std_logic lab=GND}
C {lab_wire.sym} -420 0 0 1 {name=p6 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 70 -360 0 1 {name=p17 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} -430 -190 0 0 {name=M10
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
C {sky130_fd_pr/pfet_01v8.sym} 160 -250 0 0 {name=M7
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
C {sky130_fd_pr/pfet_01v8.sym} 160 -110 0 0 {name=M8
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
C {sky130_fd_pr/pfet_01v8.sym} -70 -110 0 0 {name=M6
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
C {sky130_fd_pr/nfet_01v8.sym} 160 70 0 0 {name=M4
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
C {sky130_fd_pr/nfet_01v8.sym} 160 180 0 0 {name=M3
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
C {sky130_fd_pr/nfet_01v8.sym} -70 180 0 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} -440 150 0 0 {name=M11
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
C {sky130_fd_pr/pfet_01v8.sym} -440 70 0 0 {name=M12
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
