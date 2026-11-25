# Switching activity from a VCD: for every bit, toggles per operation and the fraction of
# time it is 1, counted only while dumping is on. Same result as synth.vcd_activity but it
# only touches the bits that change, which makes it about twice as fast on the core VCDs.

import collections, re, sys


def activity(path, op):
    ids, vals, tog, high, since = {}, {}, collections.Counter(), collections.Counter(), {}
    t = 0.0
    scale = 1.0
    t0, t1 = None, None
    on = True
    with open(path) as f:
        hdr = True
        for line in f:
            s = line.strip()
            if hdr:
                if s.startswith("$timescale"):
                    m = re.search(r"(\d+)\s*(s|ms|us|ns|ps|fs)", s + next(f, ""))
                    scale = float(m.group(1)) * {"s": 1e9, "ms": 1e6, "us": 1e3, "ns": 1.0, "ps": 1e-3, "fs": 1e-6}[m.group(2)]
                elif s.startswith("$var"):
                    p = s.split()
                    w, code, name = int(p[2]), p[3], p[4]
                    rng = p[5] if len(p) > 6 and p[5].startswith("[") else None
                    if w == 1:
                        bits = [name + (rng if rng else "")]
                    else:
                        hi, lo = [int(x) for x in rng.strip("[]").split(":")]
                        step = -1 if hi >= lo else 1
                        bits = ["%s[%d]" % (name, i) for i in range(hi, lo + step, step)]
                    ids[code] = bits
                elif s.startswith("$enddefinitions"):
                    hdr = False
                continue
            if not s:
                continue
            c = s[0]
            if c == "#":
                t = float(s[1:]) * scale
                continue
            # Close the high-time intervals of bits that are 1 when dumping stops.
            if s.startswith("$dumpoff"):
                if on:
                    for b, st in since.items():
                        high[b] += t - st
                    since = {}
                on = False
                t1 = t
                continue
            if s.startswith("$dumpon"):
                on = True
                t0 = t
                since = {b: t for b, v in vals.items() if v == "1"}
                continue
            if s.startswith("$"):
                continue
            if c in "01xzXZ":
                code, bv = s[1:], c
                pairs = [(ids[code][0], bv)] if code in ids else []
            elif c in "bB":
                v, code = s[1:].split()
                bits = ids.get(code, [])
                v = v.rjust(len(bits), "0")
                pairs = list(zip(bits, v))
            else:
                continue
            if t0 is None:
                t0 = t
            for b, bv in pairs:
                old = vals.get(b)
                if old == bv:
                    continue
                if on:
                    if old in ("0", "1") and bv in ("0", "1"):
                        tog[b] += 1
                    if old == "1":
                        high[b] += t - since.pop(b, t)
                    if bv == "1":
                        since[b] = t
                vals[b] = bv
    if on:
        for b, st in since.items():
            high[b] += t - st
    if t1 is None or t1 < t0:
        t1 = t
    dur = t1 - t0
    ops = dur / op
    if ops <= 0:
        sys.exit("no simulated operations in " + path)
    return {b: (tog[b] / ops, min(1.0, high[b] / dur)) for b in set(list(tog) + list(high) + list(vals))}, ops
