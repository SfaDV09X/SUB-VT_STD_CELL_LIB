drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/NOR2X4/layout
load nor2x4

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

rect nwell -0.23 2.2 6.67 4.41
rect psubstratepdiff 0.18 -0.145 6.26 0.145
rect nsubstratendiff 0.18 3.935 6.26 4.225
rect ndiffusion 1.445 0.42 4.995 1.26
rect pdiffusion 0.485 2.82 5.955 3.66
rect polysilicon 1.73 0.29 1.99 1.485
rect polysilicon 2.29 0.29 2.55 1.485
rect polysilicon 2.83 0.29 3.09 1.485
rect polysilicon 3.37 0.29 3.63 1.485
rect polysilicon 3.91 0.29 4.17 1.485
rect polysilicon 4.45 0.29 4.71 1.485
rect polysilicon 0.77 2.595 0.97 3.79
rect polysilicon 1.25 2.595 1.45 3.79
rect polysilicon 1.76 2.595 1.96 3.79
rect polysilicon 2.32 2.595 2.52 3.79
rect polysilicon 2.86 2.595 3.06 3.79
rect polysilicon 3.4 2.595 3.6 3.79
rect polysilicon 3.94 2.595 4.14 3.79
rect polysilicon 4.48 2.595 4.68 3.79
rect polysilicon 4.99 2.595 5.19 3.79
rect polysilicon 5.47 2.595 5.67 3.79
rect polysilicon 2.29 1.335 3.09 1.485
rect polysilicon 3.37 1.335 4.17 1.485
rect polysilicon 1.25 2.595 1.96 2.745
rect polysilicon 2.32 2.595 3.06 2.745
rect polysilicon 3.4 2.595 4.14 2.745
rect polysilicon 4.48 2.595 5.19 2.745
rect polysilicon 1.76 1.335 1.96 2.745
rect polysilicon 1.695 2.095 2.025 2.365
rect polysilicon 4.48 1.335 4.68 2.745
rect polysilicon 4.415 1.695 4.745 1.965
rect polysilicon 0.77 1.83 0.97 2.745
rect polysilicon 0.705 1.695 1.035 1.965
rect polysilicon 5.47 2.23 5.67 2.745
rect polysilicon 5.405 2.095 5.735 2.365
rect polysilicon 2.32 1.335 2.52 2.745
rect polysilicon 2.255 1.695 2.585 1.965
rect polysilicon 3.4 1.335 3.6 2.745
rect polysilicon 3.335 2.095 3.665 2.365
rect psubstratepcontact 0.3 -0.085 6.14 0.085
rect nsubstratencontact 0.3 3.995 6.14 4.165
rect ndcontact 1.505 0.48 1.675 1.2
rect ndcontact 2.065 0.48 2.235 1.2
rect ndcontact 2.605 0.48 2.775 1.2
rect ndcontact 3.145 0.48 3.315 1.2
rect ndcontact 3.685 0.48 3.855 1.2
rect ndcontact 4.225 0.48 4.395 1.2
rect ndcontact 4.765 0.48 4.935 1.2
rect pdcontact 0.545 2.88 0.715 3.6
rect pdcontact 1.025 2.88 1.195 3.6
rect pdcontact 1.505 2.88 1.675 3.6
rect pdcontact 2.065 2.88 2.235 3.6
rect pdcontact 2.605 2.88 2.775 3.6
rect pdcontact 3.145 2.88 3.315 3.6
rect pdcontact 3.685 2.88 3.855 3.6
rect pdcontact 4.225 2.88 4.395 3.6
rect pdcontact 4.765 2.88 4.935 3.6
rect pdcontact 5.245 2.88 5.415 3.6
rect pdcontact 5.725 2.88 5.895 3.6
rect pcontact 1.775 2.145 1.945 2.315
rect pcontact 4.495 1.745 4.665 1.915
rect pcontact 0.785 1.745 0.955 1.915
rect pcontact 5.485 2.145 5.655 2.315
rect pcontact 2.335 1.745 2.505 1.915
rect pcontact 3.415 2.145 3.585 2.315
rect locali 0.21 -0.165 6.23 0.165
rect locali 0.21 3.915 6.23 4.245
rect locali 1.505 0 1.675 1.28
rect locali 2.065 0.4 2.235 1.28
rect locali 2.605 0 2.775 1.28
rect locali 3.145 0.4 3.315 1.28
rect locali 3.685 0 3.855 1.28
rect locali 4.225 0.4 4.395 1.28
rect locali 4.765 0 4.935 1.28
rect locali 0.545 2.8 0.715 4.08
rect locali 1.025 2.8 1.195 3.68
rect locali 1.505 2.8 1.675 3.68
rect locali 2.065 2.8 2.235 3.68
rect locali 2.605 2.8 2.775 4.08
rect locali 3.145 2.8 3.315 3.68
rect locali 3.685 2.8 3.855 3.68
rect locali 4.225 2.8 4.395 3.68
rect locali 4.765 2.8 4.935 4.08
rect locali 5.245 2.8 5.415 3.68
rect locali 5.725 2.8 5.895 3.68
rect locali 1.695 2.145 2.025 2.315
rect locali 4.415 1.745 4.745 1.915
rect locali 0.705 1.745 1.035 1.915
rect locali 5.405 2.145 5.735 2.315
rect locali 2.255 1.745 2.585 1.915
rect locali 3.335 2.145 3.665 2.315
rect viali 0.3 -0.085 6.14 0.085
rect viali 0.3 3.995 6.14 4.165
rect viali 1.775 2.145 1.945 2.315
rect viali 4.495 1.745 4.665 1.915
rect viali 0.785 1.745 0.955 1.915
rect viali 5.485 2.145 5.655 2.315
rect viali 2.335 1.745 2.505 1.915
rect viali 3.415 2.145 3.585 2.315
rect viali 2.065 0.425 2.235 0.595
rect viali 3.145 0.425 3.315 0.595
rect viali 4.225 0.425 4.395 0.595
rect viali 1.505 3.085 1.675 3.255
rect viali 3.685 3.085 3.855 3.255
rect viali 5.725 3.085 5.895 3.255
rect viali 1.025 3.085 1.195 3.255
rect viali 2.065 3.485 2.235 3.655
rect viali 3.145 3.485 3.315 3.655
rect viali 4.225 3.485 4.395 3.655
rect viali 5.245 3.485 5.415 3.655
rect metal1 0 -0.24 6.44 0.24
rect metal1 0 3.84 6.44 4.32
rect metal1 1.99 0.38 4.47 0.64
rect metal1 1.43 3.04 5.97 3.3
rect metal1 0.95 3.44 5.49 3.7
rect metal1 0.95 3.04 1.27 3.3
rect metal1 1.7 2.1 5.73 2.36
rect metal1 0.71 1.7 4.74 1.96
rect via1 2.02 0.38 2.28 0.64
rect via1 2.02 3.04 2.28 3.3
rect via1 0.98 3.04 1.24 3.3
rect via1 0.98 3.44 1.24 3.7
rect metal2 2.02 0.35 2.28 3.33
rect metal2 2.02 0.35 2.28 0.67
rect metal2 2.02 3.01 2.28 3.33
rect metal2 0.98 3.01 1.24 3.73
rect metal2 0.98 3.01 1.24 3.33
rect metal2 0.98 3.41 1.24 3.73

pin A 2.575 1.715 2.805 1.945
pin B 3.655 2.115 3.885 2.345
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18
pin Y 2.575 3.055 2.805 3.285

property FIXED_BBOX {0 0 644 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
