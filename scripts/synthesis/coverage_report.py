#!/usr/bin/env python3
"""Count library cells instantiated in a gate-level netlist and flag unused / foreign cells.
usage: coverage_report.py <lib> <netlist.v> [require_all=0|1]
exit 1 on a non-library cell; with require_all=1 also on any unused library cell"""
import re, sys, collections
lib, net = sys.argv[1:3]
require_all = len(sys.argv) > 3 and sys.argv[3] == '1'
cells = re.findall(r'^\s*cell\s*\(\s*(\w+)\s*\)', open(lib).read(), re.M)
txt = open(net).read()
used = collections.Counter(m for m in re.findall(r'^\s*(\w+)\s+(?:\\\S+|\w+)\s*\(', txt, re.M)
                           if m not in ('module', 'input', 'output', 'wire', 'assign'))
foreign = {k: v for k, v in used.items() if k not in cells}
print("%-9s %5s" % ("cell", "count")); 
for c in cells: print("%-9s %5d%s" % (c, used.get(c, 0), "" if used.get(c, 0) else "   <-- UNUSED"))
if foreign: print("NON-LIBRARY CELLS IN NETLIST:", foreign)
print("library cells used: %d / %d" % (sum(1 for c in cells if used.get(c, 0)), len(cells)))
sys.exit(1 if foreign or (require_all and any(not used.get(c, 0) for c in cells)) else 0)
