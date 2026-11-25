#!/usr/bin/env python3
# Generate the Magic layout script cells/<CELL>/layout/<cell>.tcl for each cell.
# Usage: python3 gen_layouts.py [CELLS_DIR] [CELL ...]
# With no arguments it uses the repo's cells/ folder and builds all 13 cells.

import os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
cells_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(here, "..", "..", "cells"))
# cells_spec reads the netlist location from CELLS_DIR, so set it before the import.
os.environ["CELLS_DIR"] = cells_dir
import cells_spec
names = [a.upper() for a in sys.argv[2:]] or list(cells_spec.CELLS)
# Place, route and write the tcl; verify_layouts.sh then runs it in Magic.
for name in names:
    c = cells_spec.CELLS[name]()
    c.build()
    d = os.path.join(cells_dir, name, "layout")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, name.lower() + ".tcl")
    open(path, "w").write(c.tcl(d))
    print(f"{name:8s} width {c.W:6.2f} um -> {path}")
