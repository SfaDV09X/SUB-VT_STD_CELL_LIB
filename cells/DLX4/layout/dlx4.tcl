drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/DLX4/layout
load dlx4

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

rect nwell -0.23 2.2 12.65 4.41
rect psubstratepdiff 0.18 -0.145 12.24 0.145
rect nsubstratendiff 0.18 3.935 12.24 4.225
rect ndiffusion 0.355 0.42 1.785 1.26
rect ndiffusion 3.035 0.42 4.265 1.26
rect ndiffusion 6.225 0.42 7.265 0.84
rect ndiffusion 7.535 0.42 10.105 1.26
rect pdiffusion 0.355 2.82 2.765 3.66
rect pdiffusion 3.035 2.82 5.955 3.66
rect pdiffusion 7.535 2.82 12.065 3.66
rect polysilicon 0.64 0.29 0.93 1.485
rect polysilicon 1.21 0.29 1.5 1.485
rect polysilicon 3.32 0.29 3.51 1.485
rect polysilicon 3.79 0.29 3.98 1.485
rect polysilicon 6.51 0.29 6.98 1.485
rect polysilicon 7.82 0.29 8.11 1.485
rect polysilicon 8.39 0.29 8.68 1.485
rect polysilicon 8.96 0.29 9.25 1.485
rect polysilicon 9.53 0.29 9.82 1.485
rect polysilicon 0.68 2.595 0.89 3.79
rect polysilicon 1.25 2.595 1.46 3.79
rect polysilicon 1.78 2.595 1.99 3.79
rect polysilicon 2.27 2.595 2.48 3.79
rect polysilicon 3.32 2.595 3.51 3.79
rect polysilicon 3.79 2.595 3.98 3.79
rect polysilicon 4.26 2.595 4.45 3.79
rect polysilicon 4.73 2.595 4.92 3.79
rect polysilicon 5.2 2.595 5.67 3.79
rect polysilicon 7.86 2.595 8.07 3.79
rect polysilicon 8.43 2.595 8.64 3.79
rect polysilicon 9 2.595 9.21 3.79
rect polysilicon 9.57 2.595 9.78 3.79
rect polysilicon 10.1 2.595 10.31 3.79
rect polysilicon 10.59 2.595 10.8 3.79
rect polysilicon 11.08 2.595 11.29 3.79
rect polysilicon 11.57 2.595 11.78 3.79
rect polysilicon 0.64 1.335 1.5 1.485
rect polysilicon 3.32 1.335 3.98 1.485
rect polysilicon 7.82 1.335 8.68 1.485
rect polysilicon 8.96 1.335 9.82 1.485
rect polysilicon 0.68 2.595 2.48 2.745
rect polysilicon 3.32 2.595 4.92 2.745
rect polysilicon 7.86 2.595 9.78 2.745
rect polysilicon 10.1 2.595 11.78 2.745
rect polysilicon 6.51 1.335 6.98 2.23
rect polysilicon 6.58 2.095 6.91 2.365
rect polysilicon 5.2 1.83 5.67 2.745
rect polysilicon 5.27 1.695 5.6 1.965
rect polysilicon 0.68 1.335 0.89 2.745
rect polysilicon 0.62 1.695 0.95 1.965
rect polysilicon 3.32 1.335 3.51 1.83
rect polysilicon 3.25 1.695 3.58 1.965
rect polysilicon 7.86 1.335 8.07 2.745
rect polysilicon 7.8 1.695 8.13 1.965
rect polysilicon 9 1.335 9.21 2.23
rect polysilicon 8.94 2.095 9.27 2.365
rect polysilicon 4.26 2.23 4.45 2.745
rect polysilicon 4.19 2.095 4.52 2.365
rect polysilicon 10.1 2.23 10.31 2.745
rect polysilicon 10.04 2.095 10.37 2.365
rect psubstratepcontact 0.3 -0.085 12.12 0.085
rect nsubstratencontact 0.3 3.995 12.12 4.165
rect ndcontact 0.415 0.48 0.585 1.2
rect ndcontact 0.985 0.48 1.155 1.2
rect ndcontact 1.555 0.48 1.725 1.2
rect ndcontact 3.095 0.48 3.265 1.2
rect ndcontact 3.565 0.48 3.735 1.2
rect ndcontact 4.035 0.48 4.205 1.2
rect ndcontact 6.285 0.48 6.455 0.78
rect ndcontact 7.035 0.48 7.205 0.78
rect ndcontact 7.595 0.48 7.765 1.2
rect ndcontact 8.165 0.48 8.335 1.2
rect ndcontact 8.735 0.48 8.905 1.2
rect ndcontact 9.305 0.48 9.475 1.2
rect ndcontact 9.875 0.48 10.045 1.2
rect pdcontact 0.415 2.88 0.585 3.6
rect pdcontact 0.985 2.88 1.155 3.6
rect pdcontact 1.555 2.88 1.725 3.6
rect pdcontact 2.045 2.88 2.215 3.6
rect pdcontact 2.535 2.88 2.705 3.6
rect pdcontact 3.095 2.88 3.265 3.6
rect pdcontact 3.565 2.88 3.735 3.6
rect pdcontact 4.035 2.88 4.205 3.6
rect pdcontact 4.505 2.88 4.675 3.6
rect pdcontact 4.975 2.88 5.145 3.6
rect pdcontact 5.725 2.88 5.895 3.6
rect pdcontact 7.595 2.88 7.765 3.6
rect pdcontact 8.165 2.88 8.335 3.6
rect pdcontact 8.735 2.88 8.905 3.6
rect pdcontact 9.305 2.88 9.475 3.6
rect pdcontact 9.875 2.88 10.045 3.6
rect pdcontact 10.365 2.88 10.535 3.6
rect pdcontact 10.855 2.88 11.025 3.6
rect pdcontact 11.345 2.88 11.515 3.6
rect pdcontact 11.835 2.88 12.005 3.6
rect pcontact 6.66 2.145 6.83 2.315
rect pcontact 5.35 1.745 5.52 1.915
rect pcontact 0.7 1.745 0.87 1.915
rect pcontact 3.33 1.745 3.5 1.915
rect pcontact 7.88 1.745 8.05 1.915
rect pcontact 9.02 2.145 9.19 2.315
rect pcontact 4.27 2.145 4.44 2.315
rect pcontact 10.12 2.145 10.29 2.315
rect locali 0.21 -0.165 12.21 0.165
rect locali 0.21 3.915 12.21 4.245
rect locali 0.415 0 0.585 1.28
rect locali 0.985 0.4 1.155 1.28
rect locali 1.555 0 1.725 1.28
rect locali 3.095 0.4 3.265 1.28
rect locali 3.565 0.4 3.735 1.28
rect locali 4.035 0.4 4.205 1.28
rect locali 6.285 0.4 6.455 0.86
rect locali 7.035 0.4 7.205 0.86
rect locali 7.595 0 7.765 1.28
rect locali 8.165 0.4 8.335 1.28
rect locali 8.735 0 8.905 1.28
rect locali 9.305 0.4 9.475 1.28
rect locali 9.875 0 10.045 1.28
rect locali 0.415 2.8 0.585 4.08
rect locali 0.985 2.8 1.155 3.68
rect locali 1.555 2.8 1.725 4.08
rect locali 2.045 2.8 2.215 3.68
rect locali 2.535 2.8 2.705 4.08
rect locali 3.095 2.8 3.265 3.68
rect locali 3.565 2.8 3.735 3.68
rect locali 4.035 2.8 4.205 3.68
rect locali 4.505 2.8 4.675 3.68
rect locali 4.975 2.8 5.145 3.68
rect locali 5.725 2.8 5.895 3.68
rect locali 7.595 2.8 7.765 4.08
rect locali 8.165 2.8 8.335 3.68
rect locali 8.735 2.8 8.905 4.08
rect locali 9.305 2.8 9.475 3.68
rect locali 9.875 2.8 10.045 4.08
rect locali 10.365 2.8 10.535 3.68
rect locali 10.855 2.8 11.025 4.08
rect locali 11.345 2.8 11.515 3.68
rect locali 11.835 2.8 12.005 4.08
rect locali 6.58 2.145 6.91 2.315
rect locali 5.27 1.745 5.6 1.915
rect locali 0.62 1.745 0.95 1.915
rect locali 3.25 1.745 3.58 1.915
rect locali 7.8 1.745 8.13 1.915
rect locali 8.94 2.145 9.27 2.315
rect locali 4.19 2.145 4.52 2.315
rect locali 10.04 2.145 10.37 2.315
rect viali 0.3 -0.085 12.12 0.085
rect viali 0.3 3.995 12.12 4.165
rect viali 6.66 2.145 6.83 2.315
rect viali 5.35 1.745 5.52 1.915
rect viali 0.7 1.745 0.87 1.915
rect viali 3.33 1.745 3.5 1.915
rect viali 7.88 1.745 8.05 1.915
rect viali 9.02 2.145 9.19 2.315
rect viali 4.27 2.145 4.44 2.315
rect viali 10.12 2.145 10.29 2.315
rect viali 3.095 0.825 3.265 0.995
rect viali 4.035 0.825 4.205 0.995
rect viali 6.285 0.825 6.455 0.995
rect viali 3.095 3.085 3.265 3.255
rect viali 4.035 3.085 4.205 3.255
rect viali 4.975 3.085 5.145 3.255
rect viali 0.985 0.825 1.155 0.995
rect viali 0.985 3.085 1.155 3.255
rect viali 2.045 3.085 2.215 3.255
rect viali 7.035 0.425 7.205 0.595
rect viali 9.305 0.425 9.475 0.595
rect viali 5.725 3.085 5.895 3.255
rect viali 10.365 3.085 10.535 3.255
rect viali 11.345 3.085 11.515 3.255
rect viali 8.165 0.825 8.335 0.995
rect viali 8.165 3.485 8.335 3.655
rect viali 9.305 3.485 9.475 3.655
rect viali 3.565 0.425 3.735 0.595
rect viali 3.565 3.485 3.735 3.655
rect viali 4.505 3.485 4.675 3.655
rect metal1 0 -0.24 12.42 0.24
rect metal1 0 3.84 12.42 4.32
rect metal1 3.02 0.78 7.84 1.04
rect metal1 3.02 3.04 5.22 3.3
rect metal1 7.52 1.7 8.125 1.96
rect metal1 2.46 2.1 6.905 2.36
rect metal1 0.91 3.04 2.78 3.3
rect metal1 0.91 0.78 2.78 1.04
rect metal1 5.65 3.04 11.59 3.3
rect metal1 6.96 0.38 9.55 0.64
rect metal1 8.66 2.1 10.365 2.36
rect metal1 8.09 3.44 9.55 3.7
rect metal1 8.09 0.78 8.98 1.04
rect metal1 3.49 3.44 4.75 3.7
rect metal1 3.49 0.38 3.81 0.64
rect metal1 0.625 1.7 5.595 1.96
rect via1 3.05 0.78 3.31 1.04
rect via1 3.05 3.04 3.31 3.3
rect via1 7.55 0.78 7.81 1.04
rect via1 7.55 1.7 7.81 1.96
rect via1 2.49 0.78 2.75 1.04
rect via1 2.49 2.1 2.75 2.36
rect via1 2.49 3.04 2.75 3.3
rect via1 6.99 0.38 7.25 0.64
rect via1 6.99 3.04 7.25 3.3
rect via1 8.69 0.78 8.95 1.04
rect via1 8.69 2.1 8.95 2.36
rect via1 8.69 3.44 8.95 3.7
rect via1 3.52 0.38 3.78 0.64
rect via1 3.52 3.44 3.78 3.7
rect metal2 3.05 0.75 3.31 3.33
rect metal2 3.05 0.75 3.31 1.07
rect metal2 3.05 3.01 3.31 3.33
rect metal2 7.55 0.75 7.81 1.99
rect metal2 7.55 0.75 7.81 1.07
rect metal2 7.55 1.67 7.81 1.99
rect metal2 2.49 0.75 2.75 3.33
rect metal2 2.49 0.75 2.75 1.07
rect metal2 2.49 2.07 2.75 2.39
rect metal2 2.49 3.01 2.75 3.33
rect metal2 6.99 0.35 7.25 3.33
rect metal2 6.99 0.35 7.25 0.67
rect metal2 6.99 3.01 7.25 3.33
rect metal2 8.69 0.75 8.95 3.73
rect metal2 8.69 0.75 8.95 1.07
rect metal2 8.69 2.07 8.95 2.39
rect metal2 8.69 3.41 8.95 3.73
rect metal2 3.52 0.35 3.78 3.73
rect metal2 3.52 0.35 3.78 0.67
rect metal2 3.52 3.41 3.78 3.73

pin D 4.005 3.455 4.235 3.685
pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18
pin CLK 3.065 1.715 3.295 1.945
pin QB 9.845 2.115 10.075 2.345
pin Q 7.565 3.055 7.795 3.285

property FIXED_BBOX {0 0 1242 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
