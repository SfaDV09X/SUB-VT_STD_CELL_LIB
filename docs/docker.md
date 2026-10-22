# Docker launch reference

Tool image: iic-jku/iic-osic-tools

Launcher repo: cloned separately

Quick start guide:

    Set DOCKER_TAG = 2026.07 as a persistent environment variable
    Open docker desktop
    Open command prompt and navigate to cloned iic-osic-tools folder
    Run start_vnc.bat
    Open browser and type http://localhost:80 and enter password abc123
    Open terminal in vnc desktop and type the following:
        sak-pdk sky130A
        cd /foss/designs/SUB-VT_STD_CELL_LIB

Per-user `.designinit` (kept in your local DESIGNS folder, not tracked in this repo):

    export PDK=sky130A
    export PDKPATH=$PDK_ROOT/$PDK
    export STD_CELL_LIBRARY=sky130_fd_sc_hd
    export SPICE_USERINIT_DIR=$PDKPATH/libs.tech/ngspice
    export KLAYOUT_PATH=$PDKPATH/libs.tech/klayout
