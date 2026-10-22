#!/usr/bin/env python3
"""Write the lctime Liberty template for one combinational cell at one corner.
usage: gen_template.py <cell> <corner:tt|ss|ff> <out.lib> [--cells-dir DIR] [--tsv cells.tsv]
Cell width/height come from <cells-dir>/<cell>/<cell>.lef (SIZE w BY h); area = w*h (um^2)."""
import argparse, os, re, sys

p = argparse.ArgumentParser()
p.add_argument("cell"); p.add_argument("corner", choices=["tt", "ss", "ff"]); p.add_argument("out")
p.add_argument("--cells-dir", default="cells")
p.add_argument("--tsv", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "cells.tsv"))
a = p.parse_args()

row = None
for line in open(a.tsv):
    if line.startswith("#") or not line.strip(): continue
    c = line.rstrip("\n").split("\t")
    if c[0] == a.cell: row = c
if row is None: sys.exit("cell %s not in %s" % (a.cell, a.tsv))
_, ins, out, fn = row
m = re.search(r"SIZE\s+([\d.]+)\s+BY\s+([\d.]+)", open(os.path.join(a.cells_dir, a.cell, a.cell + ".lef")).read())
if not m: sys.exit("no SIZE statement in LEF")
area = float(m.group(1)) * float(m.group(2))

pins = "\n".join("    pin (%s) { direction : input; }" % i for i in ins.split(","))
open(a.out, "w").write("""library (subvt_sky130_%(c)s_0p40v_27c) {
  delay_model : table_lookup;
  time_unit : "1ns";
  voltage_unit : "1V";
  current_unit : "1uA";
  pulling_resistance_unit : "1kohm";
  leakage_power_unit : "1nW";
  capacitive_load_unit (1, pf);
  nom_process : 1;
  nom_temperature : 27;
  nom_voltage : 0.4;
  input_threshold_pct_rise : 50;
  input_threshold_pct_fall : 50;
  output_threshold_pct_rise : 50;
  output_threshold_pct_fall : 50;
  slew_lower_threshold_pct_rise : 30;
  slew_upper_threshold_pct_rise : 70;
  slew_lower_threshold_pct_fall : 30;
  slew_upper_threshold_pct_fall : 70;
  slew_derate_from_library : 1.0;
  cell (%(cell)s) {
    area : %(area).4f;
    pg_pin (VDD) { pg_type : primary_power; voltage_name : VDD; }
    pg_pin (GND) { pg_type : primary_ground; voltage_name : GND; }
%(pins)s
    pin (%(out)s) { direction : output; function : "%(fn)s"; }
  }
}
""" % dict(c=a.corner, cell=a.cell, area=area, pins=pins, out=out, fn=fn))
