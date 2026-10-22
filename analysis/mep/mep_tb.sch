v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 -40 0 {}
N -60 0 -30 -0 {lab=A}
N 80 -120 80 -90 {lab=VDD}
N 80 90 80 120 {lab=0}
N -80 0 -60 -0 {lab=A}
N -80 60 -80 80 {lab=0}
N 80 -200 80 -180 {lab=0}
N 160 0 180 0 {lab=Y}
N 10 -40 40 -40 {lab=A}
N 10 40 40 40 {lab=A}
N 10 0 10 40 {lab=A}
N 80 0 80 10 {lab=Y}
N 80 0 160 0 {lab=Y}
N -30 0 10 0 {lab=A}
N 80 -10 80 0 {lab=Y}
N 10 -40 10 0 {lab=A}
N 80 -40 150 -40 {lab=VDD}
N 150 -70 150 -40 {lab=VDD}
N 80 -70 150 -70 {lab=VDD}
N 80 40 150 40 {lab=0}
N 150 40 150 70 {lab=0}
N 80 70 150 70 {lab=0}
N 80 -90 80 -70 {lab=VDD}
N 80 70 80 90 {lab=0}
N 250 -40 280 -40 {lab=Y}
N 250 40 280 40 {lab=Y}
N 250 0 250 40 {lab=Y}
N 320 0 320 10 {lab=Z}
N 320 0 400 0 {lab=Z}
N 320 -10 320 0 {lab=Z}
N 250 -40 250 0 {lab=Y}
N 320 -40 390 -40 {lab=VDD}
N 390 -70 390 -40 {lab=VDD}
N 320 -70 390 -70 {lab=VDD}
N 320 40 390 40 {lab=0}
N 390 40 390 70 {lab=0}
N 320 70 390 70 {lab=0}
N 320 70 320 90 {lab=0}
N 320 -90 320 -70 {lab=VDD}
N 80 -90 320 -90 {lab=VDD}
N 80 90 320 90 {lab=0}
N 170 -0 170 20 {lab=Y}
N 170 20 220 20 {lab=Y}
N 220 0 220 20 {lab=Y}
N 220 0 250 -0 {lab=Y}
C {vsource.sym} -80 30 0 0 {name=V2 value="PULSE(0 0.4 0 0.1p 0.1p 500n 1u)" savecurrent=false}
C {gnd.sym} -80 80 0 0 {name=l1 lab=0}
C {gnd.sym} 80 120 0 0 {name=l2 lab=0}
C {vsource.sym} 80 -150 2 0 {name=V1 value=0.4 savecurrent=false}
C {gnd.sym} 80 -200 2 0 {name=l3 lab=0}
C {opin.sym} 180 0 0 0 {name=p1 lab=Y}
C {lab_pin.sym} 80 -110 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -50 0 0 0 {name=p2 sig_type=std_logic lab=A}
C {devices/code.sym} -200 -160 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval( @value )"
value="
** opencircuitdesign pdks install
.lib $::SKYWATER_MODELS/sky130.lib.spice tt
"
spice_ignore=false}
C {devices/code_shown.sym} 480 -170 0 0 {name=NGSPICE
only_toplevel=true
value="
.option savecurrents
.control
save all

dc V2 0 0.4 0.0005

let Vdiff = v(Y) - v(A)
let Vderiv = deriv(v(Y))

meas dc Vth find v(A) when Vdiff=0 cross=1
meas dc Vil find v(A) when Vderiv=-1 cross=1
meas dc Vih find v(A) when Vderiv=-1 cross=2
meas dc Vol find v(Y) when v(A)=Vih
meas dc Voh find v(Y) when v(A)=Vil

let NMh = Voh - Vih
let NMl = Vil - Vol

echo ========== INV1X1 DC ==========
print Vth
print NMh
print NMl

plot v(Y) v(A)

tran 50p 1u

meas tran Trise TRIG v(Y) VAL=0.04 RISE=1 TARG v(Y) VAL=0.36 RISE=1
meas tran Tfall TRIG v(Y) VAL=0.36 FALL=1 TARG v(Y) VAL=0.04 FALL=1

echo ========== INV1X1 TRAN ==========
print Trise
print Tfall

plot v(Y) v(A)

.endc
" }
C {sky130_fd_pr/nfet_01v8.sym} 60 40 0 0 {name=M1
W=3.36
L=0.15
nf=4 
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
C {sky130_fd_pr/pfet_01v8.sym} 60 -40 0 0 {name=M2
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
C {sky130_fd_pr/nfet_01v8.sym} 300 40 0 0 {name=M3
W=3.36
L=0.15
nf=4 
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
C {sky130_fd_pr/pfet_01v8.sym} 300 -40 0 0 {name=M4
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
C {opin.sym} 400 0 0 0 {name=p4 lab=Z}
