#!/usr/bin/env python3
# Write simple behavioural Verilog models of library cells from their Liberty functions
# (combinational assigns, ff/latch groups as always blocks). Used for equivalence checking
# and gate-level simulation. Usage: models.py <lib> <out.v> <cell> [cell ...]

import re, sys
from libs import cell_map
from libtools import blocks


# Liberty function syntax -> Verilog operators.
def vexpr(f):
    return f.replace("!", "~").replace("+", "|").replace("*", "&")


def attr(b, k):
    m = re.search(r'\b%s\s*:\s*"([^"]+)"' % k, b)
    return m.group(1) if m else None


def main(lib, out, cells):
    t = open(lib).read()
    cb = cell_map(t)
    lines = ["`timescale 1ns/1ps", ""]
    for name in cells:
        s, e = cb[name]
        body = t[s:e]
        pins = [(m.group(1), body[ps:pe]) for ps, pe, m in blocks(body, r'(?m)^\s*pin\s*\(\s*"?(\w+)"?\s*\)\s*\{')]
        ins = [p for p, b in pins if re.search(r"direction\s*:\s*\"?input", b)]
        outs = [(p, attr(b, "function")) for p, b in pins if re.search(r"direction\s*:\s*\"?output", b)]
        g = re.search(r'(?m)^\s*(ff|latch)\s*\(\s*"?(\w+)"?\s*,\s*"?(\w+)"?\s*\)\s*\{(.*?)\}', body, re.S)
        lines.append("module %s (%s);" % (name, ", ".join(ins + [o for o, _ in outs])))
        lines.append("  input %s;" % ", ".join(ins))
        lines.append("  output %s;" % ", ".join(o for o, _ in outs))
        if g:
            kind, iq, iqn, blk = g.groups()
            lines.append("  reg %s;" % iq)
            if kind == "latch":
                lines.append("  always @* if (%s) %s = %s;" % (vexpr(attr(blk, "enable")), iq, vexpr(attr(blk, "data_in"))))
            else:
                ck = attr(blk, "clocked_on")
                if not re.fullmatch(r"\w+", ck):
                    sys.exit("unsupported clock expression in %s: %s" % (name, ck))
                lines.append("  always @(posedge %s) %s <= %s;" % (ck, iq, vexpr(attr(blk, "next_state"))))
            lines.append("  wire %s = ~%s;" % (iqn, iq))
        for o, f in outs:
            lines.append("  assign %s = %s;" % (o, vexpr(f)))
        lines.append("endmodule\n")
    open(out, "w").write("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
