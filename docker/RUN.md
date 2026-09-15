# Docker launch reference for this project

Tool image: iic-jku/iic-osic-tools

Launcher repo: cloned separately

Quick start guide:

    Set DOCKER_TAG = 2026.08 as a persistent environment variable
    Open docker desktop
    Open command prompt and navigiate to cloned iic-osic-tools folder
    Run start_vnc.bat
    Open browser and type http://localhost80 and enter password abc123
    Open terminal in vnc desktop and type the following:
        sak-pdk sky130A
        cd /foss/designs/SUB-VT_STD_CELL_LIB