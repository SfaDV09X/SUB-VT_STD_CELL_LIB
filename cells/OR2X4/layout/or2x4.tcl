drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/OR2X4/layout
load or2x4

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

rect nwell -0.23 2.2 9.89 4.41
rect psubstratepdiff 0.18 -0.145 9.48 0.145
rect nsubstratendiff 0.18 3.935 9.48 4.225
rect ndiffusion 2.425 0.42 7.685 1.26
rect pdiffusion 0.505 2.82 9.155 3.66
rect polysilicon 2.71 0.29 2.97 1.485
rect polysilicon 3.27 0.29 3.53 1.485
rect polysilicon 3.81 0.29 4.07 1.485
rect polysilicon 4.35 0.29 4.61 1.485
rect polysilicon 4.89 0.29 5.15 1.485
rect polysilicon 5.43 0.29 5.69 1.485
rect polysilicon 5.97 0.29 6.26 1.485
rect polysilicon 6.54 0.29 6.83 1.485
rect polysilicon 7.11 0.29 7.4 1.485
rect polysilicon 0.79 2.595 0.99 3.79
rect polysilicon 1.27 2.595 1.47 3.79
rect polysilicon 1.75 2.595 1.95 3.79
rect polysilicon 2.23 2.595 2.43 3.79
rect polysilicon 2.74 2.595 2.94 3.79
rect polysilicon 3.3 2.595 3.5 3.79
rect polysilicon 3.84 2.595 4.04 3.79
rect polysilicon 4.38 2.595 4.58 3.79
rect polysilicon 4.92 2.595 5.12 3.79
rect polysilicon 5.46 2.595 5.66 3.79
rect polysilicon 6.01 2.595 6.22 3.79
rect polysilicon 6.58 2.595 6.79 3.79
rect polysilicon 7.15 2.595 7.36 3.79
rect polysilicon 7.68 2.595 7.89 3.79
rect polysilicon 8.17 2.595 8.38 3.79
rect polysilicon 8.66 2.595 8.87 3.79
rect polysilicon 3.27 1.335 4.07 1.485
rect polysilicon 4.35 1.335 5.15 1.485
rect polysilicon 5.97 1.335 7.4 1.485
rect polysilicon 1.27 2.595 1.95 2.745
rect polysilicon 2.23 2.595 2.94 2.745
rect polysilicon 3.3 2.595 4.04 2.745
rect polysilicon 4.38 2.595 5.12 2.745
rect polysilicon 6.01 2.595 8.87 2.745
rect polysilicon 2.74 1.335 2.94 2.745
rect polysilicon 2.675 1.695 3.005 1.965
rect polysilicon 5.46 1.335 5.66 2.745
rect polysilicon 5.395 2.095 5.725 2.365
rect polysilicon 0.79 1.83 0.99 2.745
rect polysilicon 0.725 1.695 1.055 1.965
rect polysilicon 3.3 1.335 3.5 2.745
rect polysilicon 3.235 2.095 3.565 2.365
rect polysilicon 4.38 1.335 4.58 2.745
rect polysilicon 4.315 1.695 4.645 1.965
rect polysilicon 1.75 2.23 1.95 2.745
rect polysilicon 1.685 2.095 2.015 2.365
rect polysilicon 6.58 1.335 6.79 2.745
rect polysilicon 6.52 1.695 6.85 1.965
rect psubstratepcontact 0.3 -0.085 9.36 0.085
rect nsubstratencontact 0.3 3.995 9.36 4.165
rect ndcontact 2.485 0.48 2.655 1.2
rect ndcontact 3.045 0.48 3.215 1.2
rect ndcontact 3.585 0.48 3.755 1.2
rect ndcontact 4.125 0.48 4.295 1.2
rect ndcontact 4.665 0.48 4.835 1.2
rect ndcontact 5.205 0.48 5.375 1.2
rect ndcontact 5.745 0.48 5.915 1.2
rect ndcontact 6.315 0.48 6.485 1.2
rect ndcontact 6.885 0.48 7.055 1.2
rect ndcontact 7.455 0.48 7.625 1.2
rect pdcontact 0.565 2.88 0.735 3.6
rect pdcontact 1.045 2.88 1.215 3.6
rect pdcontact 1.525 2.88 1.695 3.6
rect pdcontact 2.005 2.88 2.175 3.6
rect pdcontact 2.485 2.88 2.655 3.6
rect pdcontact 3.045 2.88 3.215 3.6
rect pdcontact 3.585 2.88 3.755 3.6
rect pdcontact 4.125 2.88 4.295 3.6
rect pdcontact 4.665 2.88 4.835 3.6
rect pdcontact 5.205 2.88 5.375 3.6
rect pdcontact 5.745 2.88 5.915 3.6
rect pdcontact 6.315 2.88 6.485 3.6
rect pdcontact 6.885 2.88 7.055 3.6
rect pdcontact 7.455 2.88 7.625 3.6
rect pdcontact 7.945 2.88 8.115 3.6
rect pdcontact 8.435 2.88 8.605 3.6
rect pdcontact 8.925 2.88 9.095 3.6
rect pcontact 2.755 1.745 2.925 1.915
rect pcontact 5.475 2.145 5.645 2.315
rect pcontact 0.805 1.745 0.975 1.915
rect pcontact 3.315 2.145 3.485 2.315
rect pcontact 4.395 1.745 4.565 1.915
rect pcontact 1.765 2.145 1.935 2.315
rect pcontact 6.6 1.745 6.77 1.915
rect locali 0.21 -0.165 9.45 0.165
rect locali 0.21 3.915 9.45 4.245
rect locali 2.485 0 2.655 1.28
rect locali 3.045 0.4 3.215 1.28
rect locali 3.585 0 3.755 1.28
rect locali 4.125 0.4 4.295 1.28
rect locali 4.665 0 4.835 1.28
rect locali 5.205 0.4 5.375 1.28
rect locali 5.745 0 5.915 1.28
rect locali 6.315 0.4 6.485 1.28
rect locali 6.885 0 7.055 1.28
rect locali 7.455 0.4 7.625 1.28
rect locali 0.565 2.8 0.735 3.68
rect locali 1.045 2.8 1.215 3.68
rect locali 1.525 2.8 1.695 4.08
rect locali 2.005 2.8 2.175 3.68
rect locali 2.485 2.8 2.655 3.68
rect locali 3.045 2.8 3.215 3.68
rect locali 3.585 2.8 3.755 4.08
rect locali 4.125 2.8 4.295 3.68
rect locali 4.665 2.8 4.835 3.68
rect locali 5.205 2.8 5.375 3.68
rect locali 5.745 2.8 5.915 4.08
rect locali 6.315 2.8 6.485 3.68
rect locali 6.885 2.8 7.055 4.08
rect locali 7.455 2.8 7.625 3.68
rect locali 7.945 2.8 8.115 4.08
rect locali 8.435 2.8 8.605 3.68
rect locali 8.925 2.8 9.095 4.08
rect locali 2.675 1.745 3.005 1.915
rect locali 5.395 2.145 5.725 2.315
rect locali 0.725 1.745 1.055 1.915
rect locali 3.235 2.145 3.565 2.315
rect locali 4.315 1.745 4.645 1.915
rect locali 1.685 2.145 2.015 2.315
rect locali 6.52 1.745 6.85 1.915
rect viali 0.3 -0.085 9.36 0.085
rect viali 0.3 3.995 9.36 4.165
rect viali 2.755 1.745 2.925 1.915
rect viali 5.475 2.145 5.645 2.315
rect viali 0.805 1.745 0.975 1.915
rect viali 3.315 2.145 3.485 2.315
rect viali 4.395 1.745 4.565 1.915
rect viali 1.765 2.145 1.935 2.315
rect viali 6.6 1.745 6.77 1.915
rect viali 3.045 0.825 3.215 0.995
rect viali 4.125 0.825 4.295 0.995
rect viali 5.205 0.825 5.375 0.995
rect viali 0.565 3.085 0.735 3.255
rect viali 2.485 3.085 2.655 3.255
rect viali 4.665 3.085 4.835 3.255
rect viali 6.315 0.425 6.485 0.595
rect viali 7.455 0.425 7.625 0.595
rect viali 6.315 3.085 6.485 3.255
rect viali 7.455 3.085 7.625 3.255
rect viali 8.435 3.085 8.605 3.255
rect viali 1.045 3.485 1.215 3.655
rect viali 2.005 3.485 2.175 3.655
rect viali 3.045 3.485 3.215 3.655
rect viali 4.125 3.485 4.295 3.655
rect viali 5.205 3.485 5.375 3.655
rect metal1 0 -0.24 9.66 0.24
rect metal1 0 3.84 9.66 4.32
rect metal1 0.49 3.04 4.91 3.3
rect metal1 6.24 1.7 6.845 1.96
rect metal1 2.97 0.78 6.56 1.04
rect metal1 6.24 0.38 7.7 0.64
rect metal1 6.24 3.04 8.68 3.3
rect metal1 0.97 3.44 5.45 3.7
rect metal1 0.73 1.7 4.64 1.96
rect metal1 1.69 2.1 5.72 2.36
rect via1 3 0.78 3.26 1.04
rect via1 3 3.04 3.26 3.3
rect via1 6.27 0.78 6.53 1.04
rect via1 6.27 1.7 6.53 1.96
rect via1 6.84 0.38 7.1 0.64
rect via1 6.84 3.04 7.1 3.3
rect metal2 3 0.75 3.26 3.33
rect metal2 3 0.75 3.26 1.07
rect metal2 3 3.01 3.26 3.33
rect metal2 6.27 0.75 6.53 1.99
rect metal2 6.27 0.75 6.53 1.07
rect metal2 6.27 1.67 6.53 1.99
rect metal2 6.84 0.35 7.1 3.33
rect metal2 6.84 0.35 7.1 0.67
rect metal2 6.84 3.01 7.1 3.33

pin A 3.555 2.115 3.785 2.345
pin B 2.455 1.715 2.685 1.945
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18
pin Y 6.855 3.055 7.085 3.285

property FIXED_BBOX {0 0 966 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
