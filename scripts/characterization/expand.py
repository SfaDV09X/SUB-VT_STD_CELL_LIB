#!/usr/bin/env python3
"""schematic (units um, nf fingers) -> local-model netlist: l/w in metres, nf>1 expanded into nf parallel nf=1 devices of W/nf."""
import sys,re
for l in open(sys.argv[1]):
    l=l.rstrip("\n"); t=l.split()
    if l.startswith("X") and len(t)>=6 and "fet" in t[5]:
        kv=dict(x.split("=") for x in t[6:] if "=" in x)
        nf=int(float(kv.get("nf","1"))); W=float(kv["W"]); L=float(kv["L"])
        for i in range(nf):
            nm=t[0] if nf==1 else "%s_f%d"%(t[0],i)
            print("%s %s %s %s %s %s l=%ge-6 w=%.6ge-6 nf=1"%(nm,*t[1:6],L,W/nf))
    else: print(l)
