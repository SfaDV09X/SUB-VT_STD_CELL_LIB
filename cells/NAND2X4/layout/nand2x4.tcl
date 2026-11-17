drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/NAND2X4/layout
load nand2x4

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

rect nwell -0.23 2.2 7.59 4.41
rect psubstratepdiff 0.18 -0.145 7.18 0.145
rect nsubstratendiff 0.18 3.935 7.18 4.225
rect ndiffusion 0.865 0.42 5.495 1.26
rect pdiffusion 0.365 2.82 6.995 3.66
rect polysilicon 1.15 0.29 1.41 1.485
rect polysilicon 1.71 0.29 1.97 1.485
rect polysilicon 2.25 0.29 2.51 1.485
rect polysilicon 2.79 0.29 3.05 1.485
rect polysilicon 3.33 0.29 3.59 1.485
rect polysilicon 3.87 0.29 4.13 1.485
rect polysilicon 4.41 0.29 4.67 1.485
rect polysilicon 4.95 0.29 5.21 1.485
rect polysilicon 0.65 2.595 0.87 3.79
rect polysilicon 1.17 2.595 1.39 3.79
rect polysilicon 1.73 2.595 1.95 3.79
rect polysilicon 2.27 2.595 2.49 3.79
rect polysilicon 2.81 2.595 3.03 3.79
rect polysilicon 3.35 2.595 3.57 3.79
rect polysilicon 3.89 2.595 4.11 3.79
rect polysilicon 4.43 2.595 4.65 3.79
rect polysilicon 4.97 2.595 5.19 3.79
rect polysilicon 5.49 2.595 5.71 3.79
rect polysilicon 5.99 2.595 6.21 3.79
rect polysilicon 6.49 2.595 6.71 3.79
rect polysilicon 1.71 1.335 2.51 1.485
rect polysilicon 2.79 1.335 3.59 1.485
rect polysilicon 3.87 1.335 4.67 1.485
rect polysilicon 0.65 2.595 1.39 2.745
rect polysilicon 1.73 2.595 2.49 2.745
rect polysilicon 2.81 2.595 3.57 2.745
rect polysilicon 3.89 2.595 4.65 2.745
rect polysilicon 4.97 2.595 5.71 2.745
rect polysilicon 5.99 2.595 6.71 2.745
rect polysilicon 1.17 1.335 1.39 2.745
rect polysilicon 1.115 1.695 1.445 1.965
rect polysilicon 4.97 1.335 5.19 2.745
rect polysilicon 4.915 1.695 5.245 1.965
rect polysilicon 1.73 1.335 1.95 2.745
rect polysilicon 1.675 2.095 2.005 2.365
rect polysilicon 2.81 1.335 3.03 2.745
rect polysilicon 2.755 1.695 3.085 1.965
rect polysilicon 3.89 1.335 4.11 2.745
rect polysilicon 3.835 2.095 4.165 2.365
rect polysilicon 5.99 2.23 6.21 2.745
rect polysilicon 5.935 2.095 6.265 2.365
rect psubstratepcontact 0.3 -0.085 7.06 0.085
rect nsubstratencontact 0.3 3.995 7.06 4.165
rect ndcontact 0.925 0.48 1.095 1.2
rect ndcontact 1.485 0.48 1.655 1.2
rect ndcontact 2.025 0.48 2.195 1.2
rect ndcontact 2.565 0.48 2.735 1.2
rect ndcontact 3.105 0.48 3.275 1.2
rect ndcontact 3.645 0.48 3.815 1.2
rect ndcontact 4.185 0.48 4.355 1.2
rect ndcontact 4.725 0.48 4.895 1.2
rect ndcontact 5.265 0.48 5.435 1.2
rect pdcontact 0.425 2.88 0.595 3.6
rect pdcontact 0.925 2.88 1.095 3.6
rect pdcontact 1.485 2.88 1.655 3.6
rect pdcontact 2.025 2.88 2.195 3.6
rect pdcontact 2.565 2.88 2.735 3.6
rect pdcontact 3.105 2.88 3.275 3.6
rect pdcontact 3.645 2.88 3.815 3.6
rect pdcontact 4.185 2.88 4.355 3.6
rect pdcontact 4.725 2.88 4.895 3.6
rect pdcontact 5.265 2.88 5.435 3.6
rect pdcontact 5.765 2.88 5.935 3.6
rect pdcontact 6.265 2.88 6.435 3.6
rect pdcontact 6.765 2.88 6.935 3.6
rect pcontact 1.195 1.745 1.365 1.915
rect pcontact 4.995 1.745 5.165 1.915
rect pcontact 1.755 2.145 1.925 2.315
rect pcontact 2.835 1.745 3.005 1.915
rect pcontact 3.915 2.145 4.085 2.315
rect pcontact 6.015 2.145 6.185 2.315
rect locali 0.21 -0.165 7.15 0.165
rect locali 0.21 3.915 7.15 4.245
rect locali 0.925 0 1.095 1.28
rect locali 1.485 0.4 1.655 1.28
rect locali 2.025 0.4 2.195 1.28
rect locali 2.565 0.4 2.735 1.28
rect locali 3.105 0 3.275 1.28
rect locali 3.645 0.4 3.815 1.28
rect locali 4.185 0.4 4.355 1.28
rect locali 4.725 0.4 4.895 1.28
rect locali 5.265 0 5.435 1.28
rect locali 0.425 2.8 0.595 4.08
rect locali 0.925 2.8 1.095 3.68
rect locali 1.485 2.8 1.655 4.08
rect locali 2.025 2.8 2.195 3.68
rect locali 2.565 2.8 2.735 4.08
rect locali 3.105 2.8 3.275 3.68
rect locali 3.645 2.8 3.815 4.08
rect locali 4.185 2.8 4.355 3.68
rect locali 4.725 2.8 4.895 4.08
rect locali 5.265 2.8 5.435 3.68
rect locali 5.765 2.8 5.935 4.08
rect locali 6.265 2.8 6.435 3.68
rect locali 6.765 2.8 6.935 4.08
rect locali 1.115 1.745 1.445 1.915
rect locali 4.915 1.745 5.245 1.915
rect locali 1.675 2.145 2.005 2.315
rect locali 2.755 1.745 3.085 1.915
rect locali 3.835 2.145 4.165 2.315
rect locali 5.935 2.145 6.265 2.315
rect viali 0.3 -0.085 7.06 0.085
rect viali 0.3 3.995 7.06 4.165
rect viali 1.195 1.745 1.365 1.915
rect viali 4.995 1.745 5.165 1.915
rect viali 1.755 2.145 1.925 2.315
rect viali 2.835 1.745 3.005 1.915
rect viali 3.915 2.145 4.085 2.315
rect viali 6.015 2.145 6.185 2.315
rect viali 2.025 0.425 2.195 0.595
rect viali 4.185 0.425 4.355 0.595
rect viali 0.925 3.085 1.095 3.255
rect viali 2.025 3.085 2.195 3.255
rect viali 3.105 3.085 3.275 3.255
rect viali 4.185 3.085 4.355 3.255
rect viali 5.265 3.085 5.435 3.255
rect viali 6.265 3.085 6.435 3.255
rect viali 1.485 0.425 1.655 0.595
rect viali 2.565 0.825 2.735 0.995
rect viali 3.645 0.825 3.815 0.995
rect viali 4.725 0.825 4.895 0.995
rect metal1 0 -0.24 7.36 0.24
rect metal1 0 3.84 7.36 4.32
rect metal1 1.95 0.38 4.43 0.64
rect metal1 0.85 3.04 6.51 3.3
rect metal1 1.41 0.38 1.73 0.64
rect metal1 1.41 0.78 4.97 1.04
rect metal1 1.12 1.7 5.24 1.96
rect metal1 1.68 2.1 6.26 2.36
rect via1 1.98 0.38 2.24 0.64
rect via1 1.98 3.04 2.24 3.3
rect via1 1.44 0.38 1.7 0.64
rect via1 1.44 0.78 1.7 1.04
rect metal2 1.98 0.35 2.24 3.33
rect metal2 1.98 0.35 2.24 0.67
rect metal2 1.98 3.01 2.24 3.33
rect metal2 1.44 0.35 1.7 1.07
rect metal2 1.44 0.35 1.7 0.67
rect metal2 1.44 0.75 1.7 1.07

pin A 3.885 2.115 4.115 2.345
pin B 3.075 1.715 3.305 1.945
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18
pin Y 2.535 3.055 2.765 3.285

property FIXED_BBOX {0 0 736 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
