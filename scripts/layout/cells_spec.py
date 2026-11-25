# Placement recipe for every X4 cell. Each function lists, column by column, which
# net sits on each source/drain and which (gate net, device) sits on each gate in the
# N row and the P row. layoutgen.Cell checks this against the netlist, then places and routes.

from layoutgen import Cell, chain, par
import os
# Root of the cells folder; gen_layouts.py sets CELLS_DIR before importing this file.
NET=os.environ.get("CELLS_DIR","/foss/designs/SUB-VT_STD_CELL_LIB/cells")
def C(name):
    return Cell(name, f"{NET}/{name}/spice/{name.lower()}.spice")

# Inverter: 1 nmos finger, 2 pmos fingers sharing the Y column.
def inv1x4():
    c=C("INV1X4")
    c.N.put(0,["GND",("A","XM1"),"Y"])
    c.P.put(0,["VDD",("A","XM2"),"Y",("A","XM2"),"VDD"])
    return c

# NAND2: series nmos stack folded into 4 finger pairs, 12 parallel pmos fingers.
def nand2x4():
    c=C("NAND2X4")
    c.N.put(1,chain("Y",("A","XM2"),"net1",("B","XM1"),"GND",4,"rail"))
    pg=[("B","XM4"),("B","XM4"),("A","XM3"),("A","XM3")]*3
    c.P.put(0,par("VDD","Y",pg))
    return c

# NOR2: series pmos stack folded into 5 finger pairs, 6 parallel nmos fingers.
def nor2x4():
    c=C("NOR2X4")
    c.P.put(0,chain("Y",("B","XM4"),"net1",("A","XM3"),"VDD",5,"rail"))
    ng=[("B","XM2"),("A","XM1"),("A","XM1"),("B","XM2"),("B","XM2"),("A","XM1")]
    c.N.put(2,par("GND","Y",ng))
    return c

# Cell name -> recipe; gen_layouts.py builds whatever is listed here.
CELLS={"INV1X4":inv1x4,"NAND2X4":nand2x4,"NOR2X4":nor2x4}

# AND2 = NAND2 stage (output net1) followed by an inverter at column 12.
def and2x4():
    c=C("AND2X4")
    c.N.put(1,chain("net1",("A","XM2"),"net2",("B","XM1"),"GND",4,"rail"))
    c.P.put(0,par("VDD","net1",[("B","XM4"),("B","XM4"),("A","XM3"),("A","XM3")]*3))
    c.P.put(12,par("VDD","Y",[("net1","XM6")]*6))
    c.N.put(12,par("GND","Y",[("net1","XM5")]*3))
    return c

# OR2 = NOR2 stage (output net1) followed by an inverter at column 10.
def or2x4():
    c=C("OR2X4")
    c.P.put(0,chain("net1",("B","XM4"),"net2",("A","XM3"),"VDD",5,"out"))
    ng=[("B","XM2"),("A","XM1"),("A","XM1"),("B","XM2"),("B","XM2"),("A","XM1")]
    c.N.put(4,par("GND","net1",ng))
    c.P.put(10,par("VDD","Y",[("net1","XM5")]*6))
    c.N.put(10,par("GND","Y",[("net1","XM6")]*3))
    return c

# AOI21 (Y = !(A&B | C)): folded A-B nmos stack plus C nmos to GND; A||B pmos to net2, then C pmos to Y.
def aoi3x4():
    c=C("AOI3X4")
    nseq=chain("Y",("A","XM4"),"net1",("B","XM6"),"GND",5,"out")
    c.N.put(1,nseq)
    ng=[t for t in nseq[1::2]]
    pmap={"A":("A","XM2"),"B":("B","XM3")}
    pg=[pmap["A"]]+[pmap[g[0]] for g in ng]+[pmap["B"]]
    c.P.put(0,par("net2","VDD",pg))
    c.P.put(12,par("net2","Y",[("C","XM1")]*6))
    c.N.put(11,par("GND","Y",[("C","XM5")]*3))
    return c

# OAI21 (Y = !((A|B) & C)): folded A-B pmos stack plus C pmos to Y; A||B nmos to net1, then C nmos to GND.
def oai3x4():
    c=C("OAI3X4")
    pseq=chain("Y",("B","XM1"),"net2",("A","XM2"),"VDD",6,"rail")
    c.P.put(0,pseq)
    pg=pseq[1::2]
    nmap={"A":("A","XM4"),"B":("B","XM5")}
    c.N.put(0,par("net1","Y",[nmap[g[0]] for g in pg[:10]]))
    c.N.put(10,par("net1","GND",[("C","XM6")]*5))
    c.P.put(12,par("VDD","Y",[("C","XM3")]*3))
    return c

CELLS.update({"AND2X4":and2x4,"OR2X4":or2x4,"AOI3X4":aoi3x4,"OAI3X4":oai3x4})

# Gate list for the shared parallel row: copy the gate order of the stack above or below
# where they overlap (so the poly lines up), then fill the gaps with the devices still
# needing fingers. Returns None if a device would end up with more than ks fingers.
def _fill_shared(chain_nets, n_s, ks, devs):
    nets = list(chain_nets)
    cnt = {k: 0 for k in devs}
    for n in nets:
        if n is not None:
            if n not in cnt: return None
            cnt[n] += 1
    if any(v > ks for v in cnt.values()): return None
    need = [k for k in devs for _ in range(ks - cnt[k])]
    for side in (0, -1):
        pass
    i = 0
    for j in range(len(nets)):
        if nets[j] is None:
            left = next((nets[x] for x in range(j + 1, len(nets)) if nets[x] is not None), None)
            pick = left if left in need else need[0]
            nets[j] = pick
            need.remove(pick)
    return nets

# Common recipe for XOR2, XNOR2, MAOI4 and MOAI4: two input inverters on the left, then
# two folded series stacks in `chain_row` and two parallel groups in the other row that
# share node net3. Tries the four start orientations of the stacks and keeps the first
# one whose gates line up between the rows.
def aoi22like(name, chain_row, r1, r2, shared, invs):
    c = C(name)
    rows = {"N": c.N, "P": c.P}
    crow, srow = rows[chain_row], rows["P" if chain_row == "N" else "N"]
    dev = c.devs
    kc = dev[r1["out_g"][1]]["nf"]
    p1, p2 = shared
    ks = dev[list(p1["devs"].values())[0]]["nf"]
    n_c, n_s = 2 * kc, 2 * ks
    n1 = max(n_c, n_s)
    base = 5
    i1, i2, inv_dev = invs
    c.N.put(0, ["GND", (i1, inv_dev["n1"]), inv_dev["o1"]])
    c.N.put(2, ["GND", (i2, inv_dev["n2"]), inv_dev["o2"]])
    c.P.put(0, ["VDD", (i1, inv_dev["p1"]), inv_dev["o1"], (i1, inv_dev["p1"]), "VDD", (i2, inv_dev["p2"]), inv_dev["o2"], (i2, inv_dev["p2"]), "VDD"])
    for st1 in ("out", "rail"):
        for st2 in ("out", "rail"):
            s1 = chain(r1["out"], r1["out_g"], r1["mid"], r1["rail_g"], r1["rail"], kc, st1)
            s2 = chain(r2["out"], r2["out_g"], r2["mid"], r2["rail_g"], r2["rail"], kc, st2)
            oc = n1 - n_c
            if oc == 0 and s1[-1] != s2[0]:
                continue
            os_ = n1 - n_s
            g1 = [None] * n_s
            for j in range(n_s):
                col = os_ + j - oc
                if 0 <= col < n_c:
                    g1[j] = s1[2 * col + 1][0]
            g2 = [None] * n_s
            for j in range(n_s):
                col = j - (0 if oc == 0 else oc // 2)
                if 0 <= col < n_c:
                    g2[j] = s2[2 * col + 1][0]
            f1 = _fill_shared(g1, n_s, ks, p1["devs"])
            f2 = _fill_shared(g2, n_s, ks, p2["devs"])
            if f1 is None or f2 is None:
                continue
            crow.put(base + oc, s1)
            crow.put(base + n1 + (0 if oc == 0 else oc // 2), s2)
            srow.put(base + os_, par(p1["node"], p1["end"], [(n, p1["devs"][n]) for n in f1]))
            srow.put(base + n1, par(p2["node"], p2["end"], [(n, p2["devs"][n]) for n in f2]))
            return c
    raise RuntimeError(name + ": no arrangement")

# XOR2 from A, B and their inverses Abar, Bbar.
def xor2x4():
    return aoi22like("XOR2X4", "N",
        dict(out="Y", out_g=("A","XM2"), mid="net1", rail_g=("B","XM1"), rail="GND"),
        dict(out="Y", out_g=("Abar","XM4"), mid="net2", rail_g=("Bbar","XM3"), rail="GND"),
        (dict(node="net3", end="VDD", devs={"A":"XM5","B":"XM7"}), dict(node="net3", end="Y", devs={"Abar":"XM6","Bbar":"XM8"})),
        ("A","B",dict(n1="XM9",p1="XM10",o1="Abar",n2="XM11",p2="XM12",o2="Bbar")))

def xnor2x4():
    return aoi22like("XNOR2X4", "N",
        dict(out="Y", out_g=("A","XM2"), mid="net1", rail_g=("Bbar","XM1"), rail="GND"),
        dict(out="Y", out_g=("B","XM4"), mid="net2", rail_g=("Abar","XM3"), rail="GND"),
        (dict(node="net3", end="VDD", devs={"A":"XM5","Bbar":"XM7"}), dict(node="net3", end="Y", devs={"B":"XM6","Abar":"XM8"})),
        ("A","B",dict(n1="XM9",p1="XM10",o1="Abar",n2="XM11",p2="XM12",o2="Bbar")))

# MAOI4: AOI22 with inverted A and B inputs (Anot, Bnot).
def maoi4x4():
    return aoi22like("MAOI4X4", "N",
        dict(out="Y", out_g=("Anot","XM2"), mid="net1", rail_g=("Bnot","XM1"), rail="GND"),
        dict(out="Y", out_g=("C","XM4"), mid="net2", rail_g=("D","XM3"), rail="GND"),
        (dict(node="net3", end="VDD", devs={"Anot":"XM5","Bnot":"XM7"}), dict(node="net3", end="Y", devs={"C":"XM6","D":"XM8"})),
        ("A","B",dict(n1="XM9",p1="XM10",o1="Anot",n2="XM11",p2="XM12",o2="Bnot")))

# MOAI4: OAI22 with inverted A and B inputs; stacks are in the P row here.
def moai4x4():
    return aoi22like("MOAI4X4", "P",
        dict(out="Y", out_g=("Bnot","XM1"), mid="net1", rail_g=("Anot","XM7"), rail="VDD"),
        dict(out="Y", out_g=("D","XM2"), mid="net2", rail_g=("C","XM8"), rail="VDD"),
        (dict(node="net3", end="Y", devs={"Anot":"XM4","Bnot":"XM6"}), dict(node="net3", end="GND", devs={"C":"XM3","D":"XM5"})),
        ("A","B",dict(n1="XM9",p1="XM10",o1="Anot",n2="XM12",p2="XM11",o2="Bnot")))

CELLS.update({"XOR2X4":xor2x4,"XNOR2X4":xnor2x4,"MAOI4X4":maoi4x4,"MOAI4X4":moai4x4})

# Latch, transparent while CLK is high: CLK inverter, D transmission gate into net1,
# feedback transmission gate from Q back to net1, then the QB and Q inverters.
def dlx4():
    c=C("DLX4")
    c.P.put(0,par("VDD","CLKB",[("CLK","XM3")]*4))
    c.N.put(0,par("GND","CLKB",[("CLK","XM4")]*2))
    c.P.put(5,par("net1","D",[("CLKB","XM1")]*4))
    c.N.put(5,par("net1","D",[("CLK","XM2")]*2))
    c.P.put(9,["net1",("CLK","XM7"),"Q"])
    c.N.put(11,["net1",("CLKB","XM10"),"Q"])
    c.P.put(13,par("VDD","QB",[("net1","XM9")]*4))
    c.N.put(13,par("GND","QB",[("net1","XM8")]*2))
    c.P.put(17,par("VDD","Q",[("QB","XM5")]*4))
    c.N.put(15,par("GND","Q",[("QB","XM6")]*2))
    return c

# Master-slave flip-flop: CLK inverter, master transmission gate D->net1 with its keeper
# (net1/net3/net2), slave transmission gate net2->net4 with feedback from Q, then QB and Q.
def dffx4():
    c=C("DFFX4")
    c.P.put(0,par("VDD","CLKB",[("CLK","XM3")]*4))
    c.N.put(0,par("GND","CLKB",[("CLK","XM4")]*2))
    c.P.put(5,par("net1","D",[("CLK","XM1")]*2))
    c.P.put(7,["net1",("CLKB","XM15"),"net2"])
    c.P.put(8,par("net2","VDD",[("net3","XM17")]*2))
    c.P.put(11,par("VDD","net3",[("net1","XM7")]*2))
    c.P.put(14,par("net4","net2",[("CLKB","XM18")]*2))
    c.P.put(16,["net4",("CLK","XM13"),"Q"])
    c.P.put(17,par("Q","VDD",[("QB","XM11")]*4))
    c.P.put(22,par("VDD","QB",[("net4","XM9")]*4))
    c.N.put(5,["net2",("CLK","XM16"),"net1"])
    c.N.put(7,["D",("CLKB","XM2"),"net1"])
    c.N.put(9,["net2",("net3","XM6"),"GND"])
    c.N.put(11,["GND",("net1","XM8"),"net3"])
    c.N.put(14,["Q",("CLKB","XM14"),"net4"])
    c.N.put(16,["net2",("CLK","XM5"),"net4"])
    c.N.put(18,par("GND","Q",[("QB","XM12")]*2))
    c.N.put(22,par("GND","QB",[("net4","XM10")]*2))
    return c

CELLS.update({"DLX4":dlx4,"DFFX4":dffx4})
