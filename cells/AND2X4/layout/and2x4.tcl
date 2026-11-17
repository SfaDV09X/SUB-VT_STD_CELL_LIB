drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/AND2X4/layout
load and2x4

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

rect nwell -0.23 2.2 10.81 4.41
rect psubstratepdiff 0.18 -0.145 10.4 0.145
rect nsubstratendiff 0.18 3.935 10.4 4.225
rect ndiffusion 0.885 0.42 5.515 1.26
rect ndiffusion 6.725 0.42 8.725 1.26
rect pdiffusion 0.385 2.82 10.195 3.66
rect polysilicon 1.17 0.29 1.43 1.485
rect polysilicon 1.73 0.29 1.99 1.485
rect polysilicon 2.27 0.29 2.53 1.485
rect polysilicon 2.81 0.29 3.07 1.485
rect polysilicon 3.35 0.29 3.61 1.485
rect polysilicon 3.89 0.29 4.15 1.485
rect polysilicon 4.43 0.29 4.69 1.485
rect polysilicon 4.97 0.29 5.23 1.485
rect polysilicon 7.01 0.29 7.3 1.485
rect polysilicon 7.58 0.29 7.87 1.485
rect polysilicon 8.15 0.29 8.44 1.485
rect polysilicon 0.67 2.595 0.89 3.79
rect polysilicon 1.19 2.595 1.41 3.79
rect polysilicon 1.75 2.595 1.97 3.79
rect polysilicon 2.29 2.595 2.51 3.79
rect polysilicon 2.83 2.595 3.05 3.79
rect polysilicon 3.37 2.595 3.59 3.79
rect polysilicon 3.91 2.595 4.13 3.79
rect polysilicon 4.45 2.595 4.67 3.79
rect polysilicon 4.99 2.595 5.21 3.79
rect polysilicon 5.51 2.595 5.73 3.79
rect polysilicon 6.01 2.595 6.23 3.79
rect polysilicon 6.51 2.595 6.73 3.79
rect polysilicon 7.05 2.595 7.26 3.79
rect polysilicon 7.62 2.595 7.83 3.79
rect polysilicon 8.19 2.595 8.4 3.79
rect polysilicon 8.72 2.595 8.93 3.79
rect polysilicon 9.21 2.595 9.42 3.79
rect polysilicon 9.7 2.595 9.91 3.79
rect polysilicon 1.73 1.335 2.53 1.485
rect polysilicon 2.81 1.335 3.61 1.485
rect polysilicon 3.89 1.335 4.69 1.485
rect polysilicon 7.01 1.335 8.44 1.485
rect polysilicon 0.67 2.595 1.41 2.745
rect polysilicon 1.75 2.595 2.51 2.745
rect polysilicon 2.83 2.595 3.59 2.745
rect polysilicon 3.91 2.595 4.67 2.745
rect polysilicon 4.99 2.595 5.73 2.745
rect polysilicon 6.01 2.595 6.73 2.745
rect polysilicon 7.05 2.595 9.91 2.745
rect polysilicon 1.19 1.335 1.41 2.745
rect polysilicon 1.135 1.695 1.465 1.965
rect polysilicon 4.99 1.335 5.21 2.745
rect polysilicon 4.935 1.695 5.265 1.965
rect polysilicon 1.75 1.335 1.97 2.745
rect polysilicon 1.695 2.095 2.025 2.365
rect polysilicon 2.83 1.335 3.05 2.745
rect polysilicon 2.775 1.695 3.105 1.965
rect polysilicon 3.91 1.335 4.13 2.745
rect polysilicon 3.855 2.095 4.185 2.365
rect polysilicon 6.01 2.23 6.23 2.745
rect polysilicon 5.955 2.095 6.285 2.365
rect polysilicon 7.05 1.335 7.26 2.745
rect polysilicon 6.99 1.695 7.32 1.965
rect psubstratepcontact 0.3 -0.085 10.28 0.085
rect nsubstratencontact 0.3 3.995 10.28 4.165
rect ndcontact 0.945 0.48 1.115 1.2
rect ndcontact 1.505 0.48 1.675 1.2
rect ndcontact 2.045 0.48 2.215 1.2
rect ndcontact 2.585 0.48 2.755 1.2
rect ndcontact 3.125 0.48 3.295 1.2
rect ndcontact 3.665 0.48 3.835 1.2
rect ndcontact 4.205 0.48 4.375 1.2
rect ndcontact 4.745 0.48 4.915 1.2
rect ndcontact 5.285 0.48 5.455 1.2
rect ndcontact 6.785 0.48 6.955 1.2
rect ndcontact 7.355 0.48 7.525 1.2
rect ndcontact 7.925 0.48 8.095 1.2
rect ndcontact 8.495 0.48 8.665 1.2
rect pdcontact 0.445 2.88 0.615 3.6
rect pdcontact 0.945 2.88 1.115 3.6
rect pdcontact 1.505 2.88 1.675 3.6
rect pdcontact 2.045 2.88 2.215 3.6
rect pdcontact 2.585 2.88 2.755 3.6
rect pdcontact 3.125 2.88 3.295 3.6
rect pdcontact 3.665 2.88 3.835 3.6
rect pdcontact 4.205 2.88 4.375 3.6
rect pdcontact 4.745 2.88 4.915 3.6
rect pdcontact 5.285 2.88 5.455 3.6
rect pdcontact 5.785 2.88 5.955 3.6
rect pdcontact 6.285 2.88 6.455 3.6
rect pdcontact 6.785 2.88 6.955 3.6
rect pdcontact 7.355 2.88 7.525 3.6
rect pdcontact 7.925 2.88 8.095 3.6
rect pdcontact 8.495 2.88 8.665 3.6
rect pdcontact 8.985 2.88 9.155 3.6
rect pdcontact 9.475 2.88 9.645 3.6
rect pdcontact 9.965 2.88 10.135 3.6
rect pcontact 1.215 1.745 1.385 1.915
rect pcontact 5.015 1.745 5.185 1.915
rect pcontact 1.775 2.145 1.945 2.315
rect pcontact 2.855 1.745 3.025 1.915
rect pcontact 3.935 2.145 4.105 2.315
rect pcontact 6.035 2.145 6.205 2.315
rect pcontact 7.07 1.745 7.24 1.915
rect locali 0.21 -0.165 10.37 0.165
rect locali 0.21 3.915 10.37 4.245
rect locali 0.945 0 1.115 1.28
rect locali 1.505 0.4 1.675 1.28
rect locali 2.045 0.4 2.215 1.28
rect locali 2.585 0.4 2.755 1.28
rect locali 3.125 0 3.295 1.28
rect locali 3.665 0.4 3.835 1.28
rect locali 4.205 0.4 4.375 1.28
rect locali 4.745 0.4 4.915 1.28
rect locali 5.285 0 5.455 1.28
rect locali 6.785 0 6.955 1.28
rect locali 7.355 0.4 7.525 1.28
rect locali 7.925 0 8.095 1.28
rect locali 8.495 0.4 8.665 1.28
rect locali 0.445 2.8 0.615 4.08
rect locali 0.945 2.8 1.115 3.68
rect locali 1.505 2.8 1.675 4.08
rect locali 2.045 2.8 2.215 3.68
rect locali 2.585 2.8 2.755 4.08
rect locali 3.125 2.8 3.295 3.68
rect locali 3.665 2.8 3.835 4.08
rect locali 4.205 2.8 4.375 3.68
rect locali 4.745 2.8 4.915 4.08
rect locali 5.285 2.8 5.455 3.68
rect locali 5.785 2.8 5.955 4.08
rect locali 6.285 2.8 6.455 3.68
rect locali 6.785 2.8 6.955 4.08
rect locali 7.355 2.8 7.525 3.68
rect locali 7.925 2.8 8.095 4.08
rect locali 8.495 2.8 8.665 3.68
rect locali 8.985 2.8 9.155 4.08
rect locali 9.475 2.8 9.645 3.68
rect locali 9.965 2.8 10.135 4.08
rect locali 1.135 1.745 1.465 1.915
rect locali 4.935 1.745 5.265 1.915
rect locali 1.695 2.145 2.025 2.315
rect locali 2.775 1.745 3.105 1.915
rect locali 3.855 2.145 4.185 2.315
rect locali 5.955 2.145 6.285 2.315
rect locali 6.99 1.745 7.32 1.915
rect viali 0.3 -0.085 10.28 0.085
rect viali 0.3 3.995 10.28 4.165
rect viali 1.215 1.745 1.385 1.915
rect viali 5.015 1.745 5.185 1.915
rect viali 1.775 2.145 1.945 2.315
rect viali 2.855 1.745 3.025 1.915
rect viali 3.935 2.145 4.105 2.315
rect viali 6.035 2.145 6.205 2.315
rect viali 7.07 1.745 7.24 1.915
rect viali 2.045 0.825 2.215 0.995
rect viali 4.205 0.825 4.375 0.995
rect viali 0.945 3.085 1.115 3.255
rect viali 2.045 3.085 2.215 3.255
rect viali 3.125 3.085 3.295 3.255
rect viali 4.205 3.085 4.375 3.255
rect viali 5.285 3.085 5.455 3.255
rect viali 6.285 3.085 6.455 3.255
rect viali 7.355 0.425 7.525 0.595
rect viali 8.495 0.425 8.665 0.595
rect viali 7.355 3.085 7.525 3.255
rect viali 8.495 3.085 8.665 3.255
rect viali 9.475 3.085 9.645 3.255
rect viali 1.505 0.425 1.675 0.595
rect viali 2.585 0.425 2.755 0.595
rect viali 3.665 0.425 3.835 0.595
rect viali 4.745 0.425 4.915 0.595
rect metal1 0 -0.24 10.58 0.24
rect metal1 0 3.84 10.58 4.32
rect metal1 0.87 3.04 6.53 3.3
rect metal1 1.97 0.78 7.03 1.04
rect metal1 6.71 1.7 7.315 1.96
rect metal1 7.28 3.04 9.72 3.3
rect metal1 7.28 0.38 8.74 0.64
rect metal1 1.43 0.38 4.99 0.64
rect metal1 1.14 1.7 5.26 1.96
rect metal1 1.7 2.1 6.28 2.36
rect via1 6.74 0.78 7 1.04
rect via1 6.74 1.7 7 1.96
rect via1 2 0.78 2.26 1.04
rect via1 2 3.04 2.26 3.3
rect via1 7.31 0.38 7.57 0.64
rect via1 7.31 3.04 7.57 3.3
rect metal2 6.74 0.75 7 1.99
rect metal2 6.74 0.75 7 1.07
rect metal2 6.74 1.67 7 1.99
rect metal2 2 0.75 2.26 3.33
rect metal2 2 0.75 2.26 1.07
rect metal2 2 3.01 2.26 3.33
rect metal2 7.31 0.35 7.57 3.33
rect metal2 7.31 0.35 7.57 0.67
rect metal2 7.31 3.01 7.57 3.33

pin A 3.905 2.115 4.135 2.345
pin B 3.095 1.715 3.325 1.945
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18
pin Y 7.895 3.055 8.125 3.285

property FIXED_BBOX {0 0 1058 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
