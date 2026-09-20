v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -60 0 -30 -0 {lab=A}
N 320 -30 320 0 {lab=VDD}
N 270 40 270 70 {lab=0}
N -80 0 -60 -0 {lab=A}
N -80 60 -80 80 {lab=0}
N 320 -110 320 -90 {lab=0}
N 270 -0 320 0 {lab=VDD}
N 270 20 290 20 {lab=Y}
C {vsource.sym} -80 30 0 0 {name=V2 value="PULSE(0 1.8 0 0.1p 0.1p 2n 4n)" savecurrent=false}
C {gnd.sym} -80 80 0 0 {name=l1 lab=0}
C {gnd.sym} 270 70 0 0 {name=l2 lab=0}
C {vsource.sym} 320 -60 2 0 {name=V1 value=1.8 savecurrent=false}
C {gnd.sym} 320 -110 2 0 {name=l3 lab=0}
C {opin.sym} 290 20 0 0 {name=p1 lab=Y}
C {lab_pin.sym} 320 -20 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {/foss/designs/SUB-VT_STD_CELL_LIB/cells/INV1X1/schematic/inv1x1.sym} 120 20 0 0 {name=x1}
C {lab_wire.sym} -50 0 0 0 {name=p2 sig_type=std_logic lab=A}
C {devices/code.sym} -200 -160 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval( @value )"
value="
** opencircuitdesign pdks install
.lib $::SKYWATER_MODELS/sky130.lib.spice tt
"
spice_ignore=false}
C {devices/code_shown.sym} 380 -180 0 0 {name=NGSPICE
only_toplevel=true
value="
.option savecurrents
.control
save all

dc V2 0 1.8 0.0005

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

tran 0.02p 4.5n

meas tran Trise TRIG v(Y) VAL=0.18 RISE=1 TARG v(Y) VAL=1.62 RISE=1
meas tran Tfall TRIG v(Y) VAL=1.62 FALL=1 TARG v(Y) VAL=0.18 FALL=1

echo ========== INV1X1 TRAN ==========
print Trise
print Tfall

plot v(Y) v(A)

.endc
" }
