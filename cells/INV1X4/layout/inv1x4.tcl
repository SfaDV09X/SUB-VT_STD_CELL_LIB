drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/INV1X4/layout
load inv1x4

set portErrors {}

proc rect {layer x1 y1 x2 y2} {
    box ${x1}um ${y1}um ${x2}um ${y2}um
    paint $layer
}
proc pin {name x1 y1 x2 y2} {
    global portErrors
    box ${x1}um ${y1}um ${x2}um ${y2}um
    label $name c metal1
    select area labels
    if {[catch {port make} msg]} { lappend portErrors "$name: $msg" }
    select clear
}

rect nwell -0.23 2.2 2.53 4.41
rect psubstratepdiff 0.18 -0.145 2.12 0.145
rect nsubstratendiff 0.18 3.935 2.12 4.225
rect ndiffusion 0.475 0.42 1.335 1.26
rect pdiffusion 0.475 2.82 1.825 3.66
rect polysilicon 0.76 0.29 1.05 1.485
rect polysilicon 0.8 2.595 1.01 3.79
rect polysilicon 1.33 2.595 1.54 3.79
rect polysilicon 0.8 2.595 1.54 2.745
rect polysilicon 0.8 1.335 1.01 2.745
rect polysilicon 0.74 1.695 1.07 1.965
rect psubstratepcontact 0.3 -0.085 2 0.085
rect nsubstratencontact 0.3 3.995 2 4.165
rect ndcontact 0.535 0.48 0.705 1.2
rect ndcontact 1.105 0.48 1.275 1.2
rect pdcontact 0.535 2.88 0.705 3.6
rect pdcontact 1.105 2.88 1.275 3.6
rect pdcontact 1.595 2.88 1.765 3.6
rect pcontact 0.82 1.745 0.99 1.915
rect locali 0.21 -0.165 2.09 0.165
rect locali 0.21 3.915 2.09 4.245
rect locali 0.535 0 0.705 1.28
rect locali 1.105 0.4 1.275 1.28
rect locali 0.535 2.8 0.705 4.08
rect locali 1.105 2.8 1.275 3.68
rect locali 1.595 2.8 1.765 4.08
rect locali 0.74 1.745 1.07 1.915
rect viali 0.3 -0.085 2 0.085
rect viali 0.3 3.995 2 4.165
rect viali 0.82 1.745 0.99 1.915
rect viali 1.105 0.425 1.275 0.595
rect viali 1.105 3.085 1.275 3.255
rect metal1 0 -0.24 2.3 0.24
rect metal1 0 3.84 2.3 4.32
rect metal1 1.03 0.38 1.35 0.64
rect metal1 1.03 3.04 1.35 3.3
rect metal1 0.745 1.7 1.065 1.96
rect via1 1.06 0.38 1.32 0.64
rect via1 1.06 3.04 1.32 3.3
rect metal2 1.06 0.35 1.32 3.33
rect metal2 1.06 0.35 1.32 0.67
rect metal2 1.06 3.01 1.32 3.33

pin A 0.79 1.715 1.02 1.945
pin Y 1.075 3.055 1.305 3.285
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18

property FIXED_BBOX {0 0 230 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
