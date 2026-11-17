drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/OAI3X4/layout
load oai3x4

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

rect nwell -0.23 2.2 9.43 4.41
rect psubstratepdiff 0.18 -0.145 9.02 0.145
rect nsubstratendiff 0.18 3.935 9.02 4.225
rect ndiffusion 0.395 0.42 8.805 1.26
rect pdiffusion 0.395 2.82 8.805 3.66
rect polysilicon 0.68 0.29 0.94 1.485
rect polysilicon 1.24 0.29 1.5 1.485
rect polysilicon 1.78 0.29 2.04 1.485
rect polysilicon 2.32 0.29 2.58 1.485
rect polysilicon 2.86 0.29 3.12 1.485
rect polysilicon 3.4 0.29 3.66 1.485
rect polysilicon 3.94 0.29 4.2 1.485
rect polysilicon 4.48 0.29 4.74 1.485
rect polysilicon 5.02 0.29 5.28 1.485
rect polysilicon 5.56 0.29 5.82 1.485
rect polysilicon 6.1 0.29 6.36 1.485
rect polysilicon 6.64 0.29 6.9 1.485
rect polysilicon 7.18 0.29 7.44 1.485
rect polysilicon 7.72 0.29 7.98 1.485
rect polysilicon 8.26 0.29 8.52 1.485
rect polysilicon 0.71 2.595 0.91 3.79
rect polysilicon 1.27 2.595 1.47 3.79
rect polysilicon 1.81 2.595 2.01 3.79
rect polysilicon 2.35 2.595 2.55 3.79
rect polysilicon 2.89 2.595 3.09 3.79
rect polysilicon 3.43 2.595 3.63 3.79
rect polysilicon 3.97 2.595 4.17 3.79
rect polysilicon 4.51 2.595 4.71 3.79
rect polysilicon 5.05 2.595 5.25 3.79
rect polysilicon 5.59 2.595 5.79 3.79
rect polysilicon 6.13 2.595 6.33 3.79
rect polysilicon 6.67 2.595 6.87 3.79
rect polysilicon 7.21 2.595 7.41 3.79
rect polysilicon 7.75 2.595 7.95 3.79
rect polysilicon 8.29 2.595 8.49 3.79
rect polysilicon 1.24 1.335 2.04 1.485
rect polysilicon 2.32 1.335 3.12 1.485
rect polysilicon 3.4 1.335 4.2 1.485
rect polysilicon 4.48 1.335 5.28 1.485
rect polysilicon 6.1 1.335 8.52 1.485
rect polysilicon 1.27 2.595 2.01 2.745
rect polysilicon 2.35 2.595 3.09 2.745
rect polysilicon 3.43 2.595 4.17 2.745
rect polysilicon 4.51 2.595 5.25 2.745
rect polysilicon 5.59 2.595 6.33 2.745
rect polysilicon 7.21 2.595 8.49 2.745
rect polysilicon 0.71 1.335 0.91 2.745
rect polysilicon 0.645 1.695 0.975 1.965
rect polysilicon 5.59 1.335 5.79 2.745
rect polysilicon 5.525 2.095 5.855 2.365
rect polysilicon 6.67 1.83 6.87 2.745
rect polysilicon 6.605 1.695 6.935 1.965
rect polysilicon 1.27 1.335 1.47 2.745
rect polysilicon 1.205 2.095 1.535 2.365
rect polysilicon 2.35 1.335 2.55 2.745
rect polysilicon 2.285 1.695 2.615 1.965
rect polysilicon 3.43 1.335 3.63 2.745
rect polysilicon 3.365 2.095 3.695 2.365
rect polysilicon 4.51 1.335 4.71 2.745
rect polysilicon 4.445 1.695 4.775 1.965
rect polysilicon 7.75 1.335 7.95 2.745
rect polysilicon 7.685 2.095 8.015 2.365
rect psubstratepcontact 0.3 -0.085 8.9 0.085
rect nsubstratencontact 0.3 3.995 8.9 4.165
rect ndcontact 0.455 0.48 0.625 1.2
rect ndcontact 1.015 0.48 1.185 1.2
rect ndcontact 1.555 0.48 1.725 1.2
rect ndcontact 2.095 0.48 2.265 1.2
rect ndcontact 2.635 0.48 2.805 1.2
rect ndcontact 3.175 0.48 3.345 1.2
rect ndcontact 3.715 0.48 3.885 1.2
rect ndcontact 4.255 0.48 4.425 1.2
rect ndcontact 4.795 0.48 4.965 1.2
rect ndcontact 5.335 0.48 5.505 1.2
rect ndcontact 5.875 0.48 6.045 1.2
rect ndcontact 6.415 0.48 6.585 1.2
rect ndcontact 6.955 0.48 7.125 1.2
rect ndcontact 7.495 0.48 7.665 1.2
rect ndcontact 8.035 0.48 8.205 1.2
rect ndcontact 8.575 0.48 8.745 1.2
rect pdcontact 0.455 2.88 0.625 3.6
rect pdcontact 1.015 2.88 1.185 3.6
rect pdcontact 1.555 2.88 1.725 3.6
rect pdcontact 2.095 2.88 2.265 3.6
rect pdcontact 2.635 2.88 2.805 3.6
rect pdcontact 3.175 2.88 3.345 3.6
rect pdcontact 3.715 2.88 3.885 3.6
rect pdcontact 4.255 2.88 4.425 3.6
rect pdcontact 4.795 2.88 4.965 3.6
rect pdcontact 5.335 2.88 5.505 3.6
rect pdcontact 5.875 2.88 6.045 3.6
rect pdcontact 6.415 2.88 6.585 3.6
rect pdcontact 6.955 2.88 7.125 3.6
rect pdcontact 7.495 2.88 7.665 3.6
rect pdcontact 8.035 2.88 8.205 3.6
rect pdcontact 8.575 2.88 8.745 3.6
rect pcontact 0.725 1.745 0.895 1.915
rect pcontact 5.605 2.145 5.775 2.315
rect pcontact 6.685 1.745 6.855 1.915
rect pcontact 1.285 2.145 1.455 2.315
rect pcontact 2.365 1.745 2.535 1.915
rect pcontact 3.445 2.145 3.615 2.315
rect pcontact 4.525 1.745 4.695 1.915
rect pcontact 7.765 2.145 7.935 2.315
rect locali 0.21 -0.165 8.99 0.165
rect locali 0.21 3.915 8.99 4.245
rect locali 0.455 0.4 0.625 1.28
rect locali 1.015 0.4 1.185 1.28
rect locali 1.555 0.4 1.725 1.28
rect locali 2.095 0.4 2.265 1.28
rect locali 2.635 0.4 2.805 1.28
rect locali 3.175 0.4 3.345 1.28
rect locali 3.715 0.4 3.885 1.28
rect locali 4.255 0.4 4.425 1.28
rect locali 4.795 0.4 4.965 1.28
rect locali 5.335 0.4 5.505 1.28
rect locali 5.875 0.4 6.045 1.28
rect locali 6.415 0 6.585 1.28
rect locali 6.955 0.4 7.125 1.28
rect locali 7.495 0 7.665 1.28
rect locali 8.035 0.4 8.205 1.28
rect locali 8.575 0 8.745 1.28
rect locali 0.455 2.8 0.625 4.08
rect locali 1.015 2.8 1.185 3.68
rect locali 1.555 2.8 1.725 3.68
rect locali 2.095 2.8 2.265 3.68
rect locali 2.635 2.8 2.805 4.08
rect locali 3.175 2.8 3.345 3.68
rect locali 3.715 2.8 3.885 3.68
rect locali 4.255 2.8 4.425 3.68
rect locali 4.795 2.8 4.965 4.08
rect locali 5.335 2.8 5.505 3.68
rect locali 5.875 2.8 6.045 3.68
rect locali 6.415 2.8 6.585 3.68
rect locali 6.955 2.8 7.125 4.08
rect locali 7.495 2.8 7.665 3.68
rect locali 8.035 2.8 8.205 4.08
rect locali 8.575 2.8 8.745 3.68
rect locali 0.645 1.745 0.975 1.915
rect locali 5.525 2.145 5.855 2.315
rect locali 6.605 1.745 6.935 1.915
rect locali 1.205 2.145 1.535 2.315
rect locali 2.285 1.745 2.615 1.915
rect locali 3.365 2.145 3.695 2.315
rect locali 4.445 1.745 4.775 1.915
rect locali 7.685 2.145 8.015 2.315
rect viali 0.3 -0.085 8.9 0.085
rect viali 0.3 3.995 8.9 4.165
rect viali 0.725 1.745 0.895 1.915
rect viali 5.605 2.145 5.775 2.315
rect viali 6.685 1.745 6.855 1.915
rect viali 1.285 2.145 1.455 2.315
rect viali 2.365 1.745 2.535 1.915
rect viali 3.445 2.145 3.615 2.315
rect viali 4.525 1.745 4.695 1.915
rect viali 7.765 2.145 7.935 2.315
rect viali 1.015 0.425 1.185 0.595
rect viali 2.095 0.425 2.265 0.595
rect viali 3.175 0.425 3.345 0.595
rect viali 4.255 0.425 4.425 0.595
rect viali 5.335 0.425 5.505 0.595
rect viali 1.555 3.085 1.725 3.255
rect viali 3.715 3.085 3.885 3.255
rect viali 5.875 3.085 6.045 3.255
rect viali 7.495 3.085 7.665 3.255
rect viali 8.575 3.085 8.745 3.255
rect viali 0.455 0.425 0.625 0.595
rect viali 1.555 0.825 1.725 0.995
rect viali 2.635 0.825 2.805 0.995
rect viali 3.715 0.825 3.885 0.995
rect viali 4.795 0.825 4.965 0.995
rect viali 5.875 0.825 6.045 0.995
rect viali 6.955 0.825 7.125 0.995
rect viali 8.035 0.825 8.205 0.995
rect viali 1.015 3.085 1.185 3.255
rect viali 2.095 3.485 2.265 3.655
rect viali 3.175 3.485 3.345 3.655
rect viali 4.255 3.485 4.425 3.655
rect viali 5.335 3.485 5.505 3.655
rect viali 6.415 3.485 6.585 3.655
rect metal1 0 -0.24 9.2 0.24
rect metal1 0 3.84 9.2 4.32
rect metal1 1.48 3.04 8.82 3.3
rect metal1 0.94 0.38 5.58 0.64
rect metal1 0.38 0.78 8.28 1.04
rect metal1 0.38 0.38 0.7 0.64
rect metal1 0.94 3.44 6.66 3.7
rect metal1 0.94 3.04 1.26 3.3
rect metal1 0.65 1.7 6.93 1.96
rect metal1 1.21 2.1 5.85 2.36
rect metal1 7.69 2.1 8.01 2.36
rect via1 1.51 0.38 1.77 0.64
rect via1 1.51 3.04 1.77 3.3
rect via1 0.41 0.38 0.67 0.64
rect via1 0.41 0.78 0.67 1.04
rect via1 0.97 3.04 1.23 3.3
rect via1 0.97 3.44 1.23 3.7
rect metal2 1.51 0.35 1.77 3.33
rect metal2 1.51 0.35 1.77 0.67
rect metal2 1.51 3.01 1.77 3.33
rect metal2 0.41 0.35 0.67 1.07
rect metal2 0.41 0.35 0.67 0.67
rect metal2 0.41 0.75 0.67 1.07
rect metal2 0.97 3.01 1.23 3.73
rect metal2 0.97 3.01 1.23 3.33
rect metal2 0.97 3.41 1.23 3.73

pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18
pin A 3.685 1.715 3.915 1.945
pin B 3.415 2.115 3.645 2.345
pin C 7.735 2.115 7.965 2.345
pin Y 2.875 3.055 3.105 3.285

property FIXED_BBOX {0 0 920 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
