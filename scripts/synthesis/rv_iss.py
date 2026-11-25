# Small RV32I instruction-set simulator used as the reference for the RISC-V runs.
# It runs a workload hex file until the program stores its result to 0x00800000 and returns
# the result, the instruction count, an instruction mix and every store (address, mask, data).
# Usage: python3 rv_iss.py <program.hex>

import sys

M = 0xFFFFFFFF


# Sign-extend the low b bits.
def sx(v, b):
    v &= (1 << b) - 1
    return v - (1 << b) if v >> (b - 1) else v


def run(hexfile, done_addr=0x00800000, limit=10_000_000):
    words = [int(l, 16) for l in open(hexfile) if l.strip()]
    mem = bytearray(0x2000)
    for i, w in enumerate(words):
        mem[4 * i:4 * i + 4] = w.to_bytes(4, "little")
    r = [0] * 32
    pc = 0
    n = 0
    hist = {}
    stores = []

    def ld(a, sz):
        return int.from_bytes(mem[a:a + sz], "little")

    while n < limit:
        ins = ld(pc, 4)
        n += 1
        op = ins & 0x7F
        rd = (ins >> 7) & 31
        f3 = (ins >> 12) & 7
        rs1 = r[(ins >> 15) & 31]
        rs2 = r[(ins >> 20) & 31]
        f7 = ins >> 25
        ii = sx(ins >> 20, 12)
        si = sx(((ins >> 25) << 5) | ((ins >> 7) & 31), 12)
        # Immediates of the I, S, B and J formats.
        bi = sx((((ins >> 31) & 1) << 12) | (((ins >> 7) & 1) << 11) | (((ins >> 25) & 63) << 5) | (((ins >> 8) & 15) << 1), 13)
        ji = sx((((ins >> 31) & 1) << 20) | (((ins >> 12) & 255) << 12) | (((ins >> 20) & 1) << 11) | (((ins >> 21) & 1023) << 1), 21)
        npc = (pc + 4) & M
        v = None
        if op == 0x37:
            v = ins & 0xFFFFF000; k = "lui"
        elif op == 0x17:
            v = (pc + (ins & 0xFFFFF000)) & M; k = "auipc"
        elif op == 0x6F:
            v = npc; npc = (pc + ji) & M; k = "jal"
        elif op == 0x67:
            v = npc; npc = (rs1 + ii) & M & ~1; k = "jalr"
        elif op == 0x63:
            k = "branch"
            c = {0: rs1 == rs2, 1: rs1 != rs2, 4: sx(rs1, 32) < sx(rs2, 32), 5: sx(rs1, 32) >= sx(rs2, 32), 6: rs1 < rs2, 7: rs1 >= rs2}[f3]
            if c:
                npc = (pc + bi) & M
        elif op == 0x03:
            k = "load"
            a = (rs1 + ii) & M
            v = {0: lambda: sx(ld(a, 1), 8) & M, 1: lambda: sx(ld(a, 2), 16) & M, 2: lambda: ld(a, 4), 4: lambda: ld(a, 1), 5: lambda: ld(a, 2)}[f3]()
        # Stores are recorded as (word address, byte mask, data in byte lanes) to compare with the cores.
        elif op == 0x23:
            k = "store"
            a = (rs1 + si) & M
            sz = {0: 1, 1: 2, 2: 4}[f3]
            msk = ((1 << sz) - 1) << (a & 3)
            dat = ((rs2 & ((1 << (8 * sz)) - 1)) << (8 * (a & 3))) & M
            stores.append((a & ~3, msk, dat))
            if a == done_addr:
                return dict(result=rs2, instret=n, hist=hist, stores=stores)
            mem[a:a + sz] = (rs2 & ((1 << (8 * sz)) - 1)).to_bytes(sz, "little")
        # OP-IMM and OP: add/sub, shifts, compares and logic.
        elif op in (0x13, 0x33):
            k = "alu"
            b = ii & M if op == 0x13 else rs2
            sh = b & 31
            alt = (f7 == 0x20)
            if f3 == 0:
                v = (rs1 - b) & M if (op == 0x33 and alt) else (rs1 + b) & M
            elif f3 == 1:
                v = (rs1 << sh) & M
            elif f3 == 2:
                v = int(sx(rs1, 32) < sx(b, 32))
            elif f3 == 3:
                v = int(rs1 < b)
            elif f3 == 4:
                v = rs1 ^ b
            elif f3 == 5:
                v = (sx(rs1, 32) >> sh) & M if alt else rs1 >> sh
            elif f3 == 6:
                v = rs1 | b
            else:
                v = rs1 & b
        else:
            sys.exit("unsupported opcode %02x at %08x" % (op, pc))
        hist[k] = hist.get(k, 0) + 1
        if v is not None and rd:
            r[rd] = v & M
        pc = npc
    sys.exit("no completion")


if __name__ == "__main__":
    R = run(sys.argv[1])
    print("result 0x%08x instret %d" % (R["result"], R["instret"]))
    print(R["hist"])
