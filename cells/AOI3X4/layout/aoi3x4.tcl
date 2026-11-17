drc off
cd /foss/designs/SUB-VT_STD_CELL_LIB/cells/AOI3X4/layout
load aoi3x4

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
rect ndiffusion 0.905 0.42 8.235 1.26
rect pdiffusion 0.425 2.82 10.155 3.66
rect polysilicon 1.19 0.29 1.45 1.485
rect polysilicon 1.75 0.29 2.01 1.485
rect polysilicon 2.29 0.29 2.55 1.485
rect polysilicon 2.83 0.29 3.09 1.485
rect polysilicon 3.37 0.29 3.63 1.485
rect polysilicon 3.91 0.29 4.17 1.485
rect polysilicon 4.45 0.29 4.71 1.485
rect polysilicon 4.99 0.29 5.25 1.485
rect polysilicon 5.53 0.29 5.79 1.485
rect polysilicon 6.07 0.29 6.33 1.485
rect polysilicon 6.61 0.29 6.87 1.485
rect polysilicon 7.15 0.29 7.41 1.485
rect polysilicon 7.69 0.29 7.95 1.485
rect polysilicon 0.71 2.595 0.91 3.79
rect polysilicon 1.22 2.595 1.42 3.79
rect polysilicon 1.78 2.595 1.98 3.79
rect polysilicon 2.32 2.595 2.52 3.79
rect polysilicon 2.86 2.595 3.06 3.79
rect polysilicon 3.4 2.595 3.6 3.79
rect polysilicon 3.94 2.595 4.14 3.79
rect polysilicon 4.48 2.595 4.68 3.79
rect polysilicon 5.02 2.595 5.22 3.79
rect polysilicon 5.56 2.595 5.76 3.79
rect polysilicon 6.1 2.595 6.3 3.79
rect polysilicon 6.64 2.595 6.84 3.79
rect polysilicon 7.18 2.595 7.38 3.79
rect polysilicon 7.72 2.595 7.92 3.79
rect polysilicon 8.23 2.595 8.43 3.79
rect polysilicon 8.71 2.595 8.91 3.79
rect polysilicon 9.19 2.595 9.39 3.79
rect polysilicon 9.67 2.595 9.87 3.79
rect polysilicon 1.75 1.335 2.55 1.485
rect polysilicon 2.83 1.335 3.63 1.485
rect polysilicon 3.91 1.335 4.71 1.485
rect polysilicon 4.99 1.335 5.79 1.485
rect polysilicon 6.61 1.335 7.95 1.485
rect polysilicon 0.71 2.595 1.42 2.745
rect polysilicon 1.78 2.595 2.52 2.745
rect polysilicon 2.86 2.595 3.6 2.745
rect polysilicon 3.94 2.595 4.68 2.745
rect polysilicon 5.02 2.595 5.76 2.745
rect polysilicon 6.1 2.595 6.84 2.745
rect polysilicon 7.18 2.595 9.87 2.745
rect polysilicon 1.22 1.335 1.42 2.745
rect polysilicon 1.155 1.695 1.485 1.965
rect polysilicon 6.1 1.335 6.3 2.745
rect polysilicon 6.035 2.095 6.365 2.365
rect polysilicon 1.78 1.335 1.98 2.745
rect polysilicon 1.715 2.095 2.045 2.365
rect polysilicon 2.86 1.335 3.06 2.745
rect polysilicon 2.795 1.695 3.125 1.965
rect polysilicon 3.94 1.335 4.14 2.745
rect polysilicon 3.875 2.095 4.205 2.365
rect polysilicon 5.02 1.335 5.22 2.745
rect polysilicon 4.955 1.695 5.285 1.965
rect polysilicon 7.18 1.335 7.38 2.745
rect polysilicon 7.115 1.695 7.445 1.965
rect psubstratepcontact 0.3 -0.085 10.28 0.085
rect nsubstratencontact 0.3 3.995 10.28 4.165
rect ndcontact 0.965 0.48 1.135 1.2
rect ndcontact 1.525 0.48 1.695 1.2
rect ndcontact 2.065 0.48 2.235 1.2
rect ndcontact 2.605 0.48 2.775 1.2
rect ndcontact 3.145 0.48 3.315 1.2
rect ndcontact 3.685 0.48 3.855 1.2
rect ndcontact 4.225 0.48 4.395 1.2
rect ndcontact 4.765 0.48 4.935 1.2
rect ndcontact 5.305 0.48 5.475 1.2
rect ndcontact 5.845 0.48 6.015 1.2
rect ndcontact 6.385 0.48 6.555 1.2
rect ndcontact 6.925 0.48 7.095 1.2
rect ndcontact 7.465 0.48 7.635 1.2
rect ndcontact 8.005 0.48 8.175 1.2
rect pdcontact 0.485 2.88 0.655 3.6
rect pdcontact 0.965 2.88 1.135 3.6
rect pdcontact 1.525 2.88 1.695 3.6
rect pdcontact 2.065 2.88 2.235 3.6
rect pdcontact 2.605 2.88 2.775 3.6
rect pdcontact 3.145 2.88 3.315 3.6
rect pdcontact 3.685 2.88 3.855 3.6
rect pdcontact 4.225 2.88 4.395 3.6
rect pdcontact 4.765 2.88 4.935 3.6
rect pdcontact 5.305 2.88 5.475 3.6
rect pdcontact 5.845 2.88 6.015 3.6
rect pdcontact 6.385 2.88 6.555 3.6
rect pdcontact 6.925 2.88 7.095 3.6
rect pdcontact 7.465 2.88 7.635 3.6
rect pdcontact 8.005 2.88 8.175 3.6
rect pdcontact 8.485 2.88 8.655 3.6
rect pdcontact 8.965 2.88 9.135 3.6
rect pdcontact 9.445 2.88 9.615 3.6
rect pdcontact 9.925 2.88 10.095 3.6
rect pcontact 1.235 1.745 1.405 1.915
rect pcontact 6.115 2.145 6.285 2.315
rect pcontact 1.795 2.145 1.965 2.315
rect pcontact 2.875 1.745 3.045 1.915
rect pcontact 3.955 2.145 4.125 2.315
rect pcontact 5.035 1.745 5.205 1.915
rect pcontact 7.195 1.745 7.365 1.915
rect locali 0.21 -0.165 10.37 0.165
rect locali 0.21 3.915 10.37 4.245
rect locali 0.965 0.4 1.135 1.28
rect locali 1.525 0.4 1.695 1.28
rect locali 2.065 0 2.235 1.28
rect locali 2.605 0.4 2.775 1.28
rect locali 3.145 0.4 3.315 1.28
rect locali 3.685 0.4 3.855 1.28
rect locali 4.225 0 4.395 1.28
rect locali 4.765 0.4 4.935 1.28
rect locali 5.305 0.4 5.475 1.28
rect locali 5.845 0.4 6.015 1.28
rect locali 6.385 0 6.555 1.28
rect locali 6.925 0.4 7.095 1.28
rect locali 7.465 0 7.635 1.28
rect locali 8.005 0.4 8.175 1.28
rect locali 0.485 2.8 0.655 3.68
rect locali 0.965 2.8 1.135 4.08
rect locali 1.525 2.8 1.695 3.68
rect locali 2.065 2.8 2.235 4.08
rect locali 2.605 2.8 2.775 3.68
rect locali 3.145 2.8 3.315 4.08
rect locali 3.685 2.8 3.855 3.68
rect locali 4.225 2.8 4.395 4.08
rect locali 4.765 2.8 4.935 3.68
rect locali 5.305 2.8 5.475 4.08
rect locali 5.845 2.8 6.015 3.68
rect locali 6.385 2.8 6.555 4.08
rect locali 6.925 2.8 7.095 3.68
rect locali 7.465 2.8 7.635 3.68
rect locali 8.005 2.8 8.175 3.68
rect locali 8.485 2.8 8.655 3.68
rect locali 8.965 2.8 9.135 3.68
rect locali 9.445 2.8 9.615 3.68
rect locali 9.925 2.8 10.095 3.68
rect locali 1.155 1.745 1.485 1.915
rect locali 6.035 2.145 6.365 2.315
rect locali 1.715 2.145 2.045 2.315
rect locali 2.795 1.745 3.125 1.915
rect locali 3.875 2.145 4.205 2.315
rect locali 4.955 1.745 5.285 1.915
rect locali 7.115 1.745 7.445 1.915
rect viali 0.3 -0.085 10.28 0.085
rect viali 0.3 3.995 10.28 4.165
rect viali 1.235 1.745 1.405 1.915
rect viali 6.115 2.145 6.285 2.315
rect viali 1.795 2.145 1.965 2.315
rect viali 2.875 1.745 3.045 1.915
rect viali 3.955 2.145 4.125 2.315
rect viali 5.035 1.745 5.205 1.915
rect viali 7.195 1.745 7.365 1.915
rect viali 0.485 3.085 0.655 3.255
rect viali 1.525 3.085 1.695 3.255
rect viali 2.605 3.085 2.775 3.255
rect viali 3.685 3.085 3.855 3.255
rect viali 4.765 3.085 4.935 3.255
rect viali 5.845 3.085 6.015 3.255
rect viali 6.925 3.085 7.095 3.255
rect viali 8.005 3.085 8.175 3.255
rect viali 8.965 3.085 9.135 3.255
rect viali 9.925 3.085 10.095 3.255
rect viali 0.965 0.425 1.135 0.595
rect viali 3.145 0.425 3.315 0.595
rect viali 5.305 0.425 5.475 0.595
rect viali 6.925 0.425 7.095 0.595
rect viali 8.005 0.425 8.175 0.595
rect viali 7.465 3.485 7.635 3.655
rect viali 8.485 3.485 8.655 3.655
rect viali 9.445 3.485 9.615 3.655
rect viali 1.525 0.825 1.695 0.995
rect viali 2.605 0.825 2.775 0.995
rect viali 3.685 0.825 3.855 0.995
rect viali 4.765 0.825 4.935 0.995
rect viali 5.845 0.825 6.015 0.995
rect metal1 0 -0.24 10.58 0.24
rect metal1 0 3.84 10.58 4.32
rect metal1 0.41 3.04 10.17 3.3
rect metal1 0.89 0.38 8.25 0.64
rect metal1 7.39 3.44 9.69 3.7
rect metal1 1.45 0.78 6.09 1.04
rect metal1 1.16 1.7 5.28 1.96
rect metal1 1.72 2.1 6.36 2.36
rect metal1 7.12 1.7 7.44 1.96
rect via1 7.42 0.38 7.68 0.64
rect via1 7.42 3.44 7.68 3.7
rect metal2 7.42 0.35 7.68 3.73
rect metal2 7.42 0.35 7.68 0.67
rect metal2 7.42 3.41 7.68 3.73

pin VDD 0.05 3.90 0.35 4.26
pin GND 0.05 -0.18 0.35 0.18
pin A 3.115 1.715 3.345 1.945
pin B 3.925 2.115 4.155 2.345
pin C 7.165 1.715 7.395 1.945
pin Y 5.815 0.395 6.045 0.625

property FIXED_BBOX {0 0 1058 408}

writeall force

if {[llength $portErrors] > 0} {
    foreach e $portErrors { puts "PORT ERROR $e" }
} else {
    puts "Port errors: none"
}
