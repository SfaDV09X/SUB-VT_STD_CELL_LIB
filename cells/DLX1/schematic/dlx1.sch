v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -780 -190 -760 -190 {lab=D}
N -780 -190 -780 -110 {lab=D}
N -780 -110 -760 -110 {lab=D}
N -700 -190 -680 -190 {lab=#net1}
N -680 -190 -680 -110 {lab=#net1}
N -700 -110 -680 -110 {lab=#net1}
N -20 -120 -20 -80 {lab=#net2}
N -80 -150 -60 -150 {lab=#net3}
N -80 -150 -80 -50 {lab=#net3}
N -80 -50 -60 -50 {lab=#net3}
N -20 -20 -20 10 {lab=GND}
N -20 10 -20 20 {lab=GND}
N -20 -210 -20 -180 {lab=VDD}
N -110 -100 -80 -100 {lab=#net3}
N -20 -100 20 -100 {lab=#net2}
N -350 -120 -350 -80 {lab=#net3}
N -410 -150 -390 -150 {lab=#net1}
N -410 -150 -410 -50 {lab=#net1}
N -410 -50 -390 -50 {lab=#net1}
N -350 -20 -350 10 {lab=GND}
N -350 10 -350 20 {lab=GND}
N -350 -210 -350 -180 {lab=VDD}
N -440 -130 -410 -130 {lab=#net1}
N -350 -100 -310 -100 {lab=#net3}
N -410 150 -390 150 {lab=#net4}
N -410 150 -410 230 {lab=#net4}
N -410 230 -390 230 {lab=#net4}
N -330 150 -310 150 {lab=#net2}
N -310 150 -310 230 {lab=#net2}
N -330 230 -310 230 {lab=#net2}
N -360 270 -360 290 {lab=CLKB}
N -360 70 -360 110 {lab=CLK}
N -360 60 -360 70 {lab=CLK}
N -620 290 -360 290 {lab=CLKB}
N -910 60 -620 60 {lab=CLK}
N -920 290 -620 290 {lab=CLKB}
N -730 -80 -730 -70 {lab=CLK}
N -730 -240 -730 -230 {lab=CLKB}
N -730 -250 -730 -240 {lab=CLKB}
N -680 -130 -440 -130 {lab=#net1}
N -310 -100 -270 -100 {lab=#net3}
N -270 -100 -110 -100 {lab=#net3}
N -870 -150 -780 -150 {lab=D}
N -20 -10 10 -10 {lab=GND}
N -20 -200 20 -200 {lab=VDD}
N 20 -200 20 -160 {lab=VDD}
N -350 -190 -330 -190 {lab=VDD}
N -330 -190 -330 -160 {lab=VDD}
N -350 -10 -320 -10 {lab=GND}
N -470 210 -370 210 {lab=GND}
N -350 170 -220 170 {lab=VDD}
N -20 -50 10 -50 {lab=GND}
N 10 -50 10 -10 {lab=GND}
N -20 -150 20 -150 {lab=VDD}
N 20 -160 20 -150 {lab=VDD}
N -330 -160 -330 -150 {lab=VDD}
N -350 -150 -330 -150 {lab=VDD}
N -350 -50 -320 -50 {lab=GND}
N -320 -50 -320 -10 {lab=GND}
N -360 150 -360 170 {lab=VDD}
N -360 170 -350 170 {lab=VDD}
N -370 210 -360 210 {lab=GND}
N -360 210 -360 230 {lab=GND}
N -730 -190 -730 -180 {lab=VDD}
N -730 -180 -640 -180 {lab=VDD}
N -730 -130 -730 -110 {lab=GND}
N -730 -140 -730 -130 {lab=GND}
N -730 -140 -670 -140 {lab=GND}
N -1230 -90 -1230 -50 {lab=CLKB}
N -1290 -120 -1270 -120 {lab=CLK}
N -1290 -120 -1290 -20 {lab=CLK}
N -1290 -20 -1270 -20 {lab=CLK}
N -1230 10 -1230 40 {lab=GND}
N -1230 40 -1230 50 {lab=GND}
N -1230 -180 -1230 -150 {lab=VDD}
N -1320 -80 -1290 -80 {lab=CLK}
N -1230 -70 -1190 -70 {lab=CLKB}
N -1230 20 -1190 20 {lab=GND}
N -1200 -160 -1200 -130 {lab=VDD}
N -1230 -160 -1200 -160 {lab=VDD}
N -1200 -130 -1200 -120 {lab=VDD}
N -1230 -120 -1200 -120 {lab=VDD}
N -1230 -20 -1190 -20 {lab=GND}
N -1190 -20 -1190 20 {lab=GND}
N -730 -70 -730 60 {lab=CLK}
N -830 -260 -730 -260 {lab=CLKB}
N -830 -260 -830 290 {lab=CLKB}
N -730 -260 -730 -250 {lab=CLKB}
N -620 60 -360 60 {lab=CLK}
N -940 290 -920 290 {lab=CLKB}
N -310 190 170 190 {lab=#net2}
N 170 -100 170 190 {lab=#net2}
N 20 -100 300 -100 {lab=#net2}
N -160 -100 -160 70 {lab=#net3}
N -160 70 300 70 {lab=#net3}
C {sky130_fd_pr/pfet_01v8.sym} -730 -210 1 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} -730 -90 3 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} -40 -150 0 0 {name=M5
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
C {sky130_fd_pr/nfet_01v8.sym} -40 -50 0 0 {name=M6
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
C {sky130_fd_pr/pfet_01v8.sym} -370 -150 0 0 {name=M7
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
C {sky130_fd_pr/nfet_01v8.sym} -370 -50 0 0 {name=M8
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
C {sky130_fd_pr/pfet_01v8.sym} -360 130 1 0 {name=M15
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
C {sky130_fd_pr/nfet_01v8.sym} -360 250 3 0 {name=M16
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
C {lab_wire.sym} -940 290 0 0 {name=p23 sig_type=std_logic lab=CLKB}
C {ipin.sym} -870 -150 0 0 {name=p5 lab=D}
C {lab_wire.sym} -20 -210 0 0 {name=p13 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -350 -210 0 0 {name=p14 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -20 20 0 0 {name=p7 sig_type=std_logic lab=GND}
C {lab_wire.sym} -350 20 0 0 {name=p15 sig_type=std_logic lab=GND}
C {lab_wire.sym} -910 60 0 0 {name=p8 sig_type=std_logic lab=CLK}
C {lab_wire.sym} -640 -180 0 0 {name=p17 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -670 -140 0 1 {name=p18 sig_type=std_logic lab=GND}
C {lab_wire.sym} -470 210 0 1 {name=p19 sig_type=std_logic lab=GND}
C {lab_wire.sym} -220 170 0 1 {name=p20 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} -1250 -120 0 0 {name=M3
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
C {sky130_fd_pr/nfet_01v8.sym} -1250 -20 0 0 {name=M4
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
C {iopin.sym} -1230 -180 0 0 {name=p1 lab=VDD}
C {iopin.sym} -1230 50 0 0 {name=p2 lab=GND}
C {lab_wire.sym} -1190 -70 0 0 {name=p4 sig_type=std_logic lab=CLKB}
C {ipin.sym} -1320 -80 0 0 {name=p3 lab=CLK}
C {opin.sym} 300 70 0 0 {name=p6 lab=QB}
C {opin.sym} 300 -100 0 0 {name=p9 lab=Q}
