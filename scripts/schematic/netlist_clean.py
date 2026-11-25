#!/usr/bin/env python3
# Turn a raw xschem netlist into the form used everywhere in the flow: one line per device
# with only the nets, the model and L, W, nf (the drain/source area parameters of the sky130
# symbols are dropped; extraction gets the real ones from the layout). Checks that the file
# has exactly one .subckt with VDD/GND and that every device has numeric sizes.
# Usage: netlist_clean.py <raw xschem netlist> <cells/<CELL>/spice/<cell>.spice>

import os, re, sys

KEEP = ("L", "W", "nf")


def joined(path):
    out = []
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("+") and out:
            out[-1] += " " + line[1:].strip()
        else:
            out.append(line)
    return out


def clean(lines, src):
    out, subckt, ends = [], 0, 0
    for line in lines:
        t = line.split()
        if not t:
            continue
        low = t[0].lower()
        if low == ".subckt":
            subckt += 1
            if not {"VDD", "GND"} <= set(t[2:]):
                sys.exit("%s: .subckt %s has no VDD/GND ports" % (src, t[1]))
            out.append(line)
        elif low == ".ends":
            ends += 1
            out.append(".ends")
        elif low == ".end":
            continue
        elif t[0].startswith("**") or t[0].startswith("*."):
            out.append(line)
        elif t[0][0] in "xXmM":
            if len(t) < 6 or "sky130_fd_pr__" not in t[5]:
                sys.exit("%s: unexpected device line: %s" % (src, line))
            kv = dict(x.split("=", 1) for x in t[6:] if "=" in x)
            vals = []
            for k in KEEP:
                v = kv.get(k)
                try:
                    float(v)
                except (TypeError, ValueError):
                    sys.exit("%s: %s has %s=%s, expected a number" % (src, t[0], k, v))
                vals.append("%s=%s" % (k, v))
            if float(kv["nf"]) != int(float(kv["nf"])):
                sys.exit("%s: %s has a non-integer nf" % (src, t[0]))
            out.append(" ".join(t[:6] + vals))
        elif t[0].startswith("*"):
            continue
        else:
            sys.exit("%s: unexpected line: %s" % (src, line))
    if subckt != 1 or ends != 1:
        sys.exit("%s: expected one .subckt / .ends, found %d / %d" % (src, subckt, ends))
    return "\n".join(out) + "\n"


def main(raw, dst):
    text = clean(joined(raw), raw)
    name = os.path.basename(dst)
    old = open(dst).read() if os.path.isfile(dst) else None
    # Only the sch_path comment depends on where the repo sits; ignore it when comparing.
    body = lambda s: [l for l in s.splitlines() if not l.startswith("** sch_path")]
    if old is not None and body(old) == body(text):
        print("%-16s unchanged" % name)
        return
    open(dst, "w").write(text)
    if old is None:
        print("%-16s written" % name)
    else:
        changed = len(set(body(text)) ^ set(body(old)))
        print("%-16s updated (%d lines differ from the previous netlist)" % (name, changed))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: netlist_clean.py <raw netlist> <output .spice>")
    main(sys.argv[1], sys.argv[2])
