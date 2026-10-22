#!/usr/bin/env python3
"""Write a copy of a Liberty file with only the given cells.
usage: sublib.py <in.lib> <out.lib> <target> <helper>...
The helper cells are only there to keep the library functionally complete (ABC refuses to map
with a library that cannot implement an arbitrary AND node); their area is multiplied by 1000
so that an area-driven mapper uses <target> whenever it can implement the function."""
import re, sys
src, dst, target, helpers = sys.argv[1], sys.argv[2], sys.argv[3], set(sys.argv[4:])
keep = helpers | {target}
t = open(src).read(); out = []; pos = 0
for m in re.finditer(r'^\s*cell\s*\(\s*(\w+)\s*\)\s*\{', t, re.M):
    i, d = m.end(), 1
    while d: d += (t[i] == '{') - (t[i] == '}'); i += 1
    out.append(t[pos:m.start()]); pos = i
    name, blk = m.group(1), t[m.start():i]
    if name in keep:
        if name != target:
            blk = re.sub(r'(\barea\s*:\s*)([0-9.]+)', lambda x: x.group(1) + str(float(x.group(2)) * 1000), blk, count=1)
        out.append(blk)
out.append(t[pos:]); open(dst, 'w').write(''.join(out))
