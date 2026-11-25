# Layout engine for the X4 cells. Takes a cell's spice netlist plus a hand-written
# device order for the N and P rows, places the fingers on a fixed 4.08 um tall
# template, routes the internal nets on metal1/metal2 and writes a Magic tcl script.
# Used by gen_layouts.py; the per-cell placements live in cells_spec.py.

import re, math, heapq, itertools, random

# Snap every coordinate to the 5 nm manufacturing grid.
R = lambda v: round(round(v / 0.005) * 0.005, 3)

# Cell template (um): height, N/P diffusion edges, poly bars that tie gates
# together, metal1 routing tracks (bottom to top) and the n-well start.
H = 4.08
N_Y0 = 0.42
P_Y1 = 3.66
N_BAR = (1.335, 1.485)
P_BAR = (2.595, 2.745)
TRACKS = {"N1": 0.51, "N2": 0.91, "C1": 1.31, "C2": 1.83, "C3": 2.23, "C4": 2.63, "P2": 3.17, "P1": 3.57}
TORDER = ["N1", "N2", "C1", "C2", "C3", "C4", "P2", "P1"]
ROW_TRACKS = {"N": ["N1", "N2"], "P": ["P2", "P1"]}
PC_TRACKS = ["C2", "C3"]
NWELL_Y0 = 2.20
# Half width of a source/drain contact column, diffusion overhang past the
# last contact, and the minimum centre-to-centre distance between two different nets on metal.
SD_HALF = 0.14
DIFF_END = 0.145
MSEP = 0.46


# Read the .subckt ports and every XM transistor (type, d/g/s nets, W, nf, L).
def parse_spice(path):
    devs, ports, name = {}, [], None
    for l in open(path):
        t = l.split()
        if not t:
            continue
        if t[0] == ".subckt":
            name, ports = t[1], t[2:]
        elif t[0].startswith("XM"):
            kv = dict(x.split("=") for x in t[6:])
            devs[t[0]] = dict(t="n" if "nfet" in t[5] else "p", d=t[1], g=t[2], s=t[3], W=float(kv["W"]), nf=int(kv["nf"]), L=float(kv["L"]))
    return name, ports, devs


# One diffusion row. S[i] is the net on source/drain column i, G[i] is the
# (gate net, device) on the gate between columns i and i+1.
class Row:
    def __init__(self):
        self.S, self.G = {}, {}

    # seq alternates sd, gate, sd, gate, ... starting at column `start`.
    # Shared sd columns must carry the same net, a gate slot can only be used once.
    def put(self, start, seq):
        for k, tok in enumerate(seq):
            if k % 2 == 0:
                i = start + k // 2
                if i in self.S and self.S[i] != tok:
                    raise ValueError(f"S{i} conflict {self.S[i]} vs {tok}")
                self.S[i] = tok
            else:
                i = start + k // 2
                if i in self.G:
                    raise ValueError(f"G{i} occupied")
                self.G[i] = tok


# Series stack folded into k finger pairs, e.g. out-A-mid-B-rail-B-mid-A-out...
# so the stack can be drawn with shared diffusion. `start` picks the end it begins on.
def chain(out, g_out, mid, g_rail, rail, k, start="rail"):
    seq, state = [], start
    for _ in range(2 * k):
        if state == "rail":
            seq += [rail, g_rail]; state = "mid_up"
        elif state == "mid_up":
            seq += [mid, g_out]; state = "out"
        elif state == "out":
            seq += [out, g_out]; state = "mid_dn"
        else:
            seq += [mid, g_rail]; state = "rail"
    end = {"rail": rail, "out": out, "mid_up": mid, "mid_dn": mid}[state]
    seq.append(end)
    return seq


# Parallel fingers between nets a and b: a-g-b-g-a-g-b ...
def par(a, b, gates):
    seq = []
    for i, g in enumerate(gates):
        seq += [a if i % 2 == 0 else b, g]
    seq.append(a if len(gates) % 2 == 0 else b)
    return seq


class Cell:
    def __init__(self, name, spice):
        self.name = name
        self.sub, self.ports, self.devs = parse_spice(spice)
        self.N, self.P = Row(), Row()
        self.extra_ws = {}

    def rows(self):
        return {"N": self.N, "P": self.P}

    # Sanity check the hand placement against the netlist: right device type in each
    # row, gate and sd nets match the device, and every device gets exactly nf fingers.
    def validate(self):
        ns = max(list(self.N.S) + list(self.P.S)) + 1
        self.ns = ns
        cnt = {}
        for rn, row in self.rows().items():
            for i, (net, dev) in row.G.items():
                d = self.devs[dev]
                assert d["t"] == rn.lower(), (self.name, dev, rn)
                assert net == d["g"], (self.name, dev, net, d["g"])
                a, b = row.S.get(i), row.S.get(i + 1)
                assert a is not None and b is not None, (self.name, rn, "gate without SD", i)
                assert {a, b} == {d["d"], d["s"]}, (self.name, dev, a, b, d["d"], d["s"])
                cnt[dev] = cnt.get(dev, 0) + 1
            for i in row.S:
                if (i - 1) not in row.G and i not in row.G:
                    raise ValueError(f"{self.name} {rn} S{i} isolated")
        for dev, d in self.devs.items():
            assert cnt.get(dev, 0) == d["nf"], (self.name, dev, cnt.get(dev, 0), d["nf"])

    # Width of a single finger.
    def wf(self, dev):
        d = self.devs[dev]
        return round(d["W"] / d["nf"], 3)

    # Groups of adjacent gates in a row; each group becomes one continuous diffusion.
    def strips(self, rn):
        row = self.rows()[rn]
        gs = sorted(row.G)
        out, cur = [], []
        for i in gs:
            if cur and i == cur[-1] + 1:
                cur.append(i)
            else:
                if cur:
                    out.append(cur)
                cur = [i]
        if cur:
            out.append(cur)
        return out

    # Runs of adjacent gates driven by the same net; each run needs one poly contact.
    def comps(self, rn):
        row = self.rows()[rn]
        gs = sorted(row.G)
        out, cur = [], []
        for i in gs:
            if cur and i == cur[-1] + 1 and row.G[i][0] == row.G[cur[-1]][0]:
                cur.append(i)
            else:
                if cur:
                    out.append(cur)
                cur = [i]
        if cur:
            out.append(cur)
        return [(row.G[c[0]][0], c) for c in out]

    def gate_L(self, i):
        Ls = [self.devs[r.G[i][1]]["L"] for r in (self.N, self.P) if i in r.G]
        return max(Ls) if Ls else 0.0

    # Choose the column where each gate run gets its poly contact. A contact can be
    # shared by the N and P run of the same net when they line up. Small exhaustive
    # search that prefers no two contacts in neighbouring columns, then fewest contacts.
    def plan_pcs(self):
        ncomps, pcomps = self.comps("N"), self.comps("P")
        items = [("N", k, net, cols) for k, (net, cols) in enumerate(ncomps)] + [("P", k, net, cols) for k, (net, cols) in enumerate(pcomps)]
        best = None
        order = sorted(range(len(items)), key=lambda j: len(items[j][3]))

        def options(item):
            rn, k, net, cols = item
            other = "P" if rn == "N" else "N"
            orow = self.rows()[other]
            opts = []
            for c in cols:
                if c in orow.G and orow.G[c][0] == net:
                    ocomp = [j for j, it in enumerate(items) if it[0] == other and c in it[3]][0]
                    opts.append((c, ocomp))
                else:
                    opts.append((c, None))
            return opts

        assign, used_cols = {}, {}

        def score():
            pcs = sorted(set(v[0] for v in assign.values()))
            adj = sum(1 for a, b in zip(pcs, pcs[1:]) if b - a == 1)
            return adj, len(pcs)

        def rec(idx):
            nonlocal best
            if idx == len(order):
                s = score()
                if best is None or s < best[0]:
                    best = (s, dict(assign))
                return
            j = order[idx]
            if j in assign:
                rec(idx + 1)
                return
            for c, oj in options(items[j]):
                if c in used_cols:
                    continue
                if oj is not None and oj in assign:
                    continue
                assign[j] = (c, oj)
                used_cols[c] = j
                if oj is not None:
                    assign[oj] = (c, j)
                rec(idx + 1)
                del assign[j]
                del used_cols[c]
                if oj is not None:
                    del assign[oj]
            if best is not None and best[0][0] == 0 and idx > 12:
                return

        sys_limit = [0]
        rec(0)
        if best is None:
            raise RuntimeError(f"{self.name}: no pc placement")
        pcs = {}
        for j, (c, oj) in best[1].items():
            rn, k, net, cols = items[j]
            pcs.setdefault(c, {"net": net, "rows": set()})["rows"].add(rn)
        self.items = items
        self.pcs = pcs
        cols = sorted(pcs)
        # Neighbouring poly contacts need extra gate spacing, remembered in extra_ws.
        for a, b in zip(cols, cols[1:]):
            if b - a == 1:
                L = max(self.gate_L(a), self.gate_L(b))
                need = max(0.56, 0.40 + L / 2)
                self.extra_ws[b] = need
        self.bars = []
        for rn, k, net, cols_ in items:
            if len(cols_) > 1:
                self.bars.append((rn, cols_))

    # Assign x positions: sd column, gate, sd column ... with the gate width set by
    # the longest L in that column and widened where poly contacts sit side by side.
    # Then round the cell width up to the 0.46 um site and centre the content.
    def place(self):
        ns = self.ns
        wg = {}
        for i in range(ns - 1):
            Ls = [self.devs[r.G[i][1]]["L"] for r in (self.N, self.P) if i in r.G]
            w = max(Ls) if Ls else 0.0
            for r in (self.N, self.P):
                if i not in r.G and i in r.S and (i + 1) in r.S:
                    w = max(w, 0.28)
            wg[i] = max(w, 0.28) if not Ls else w
        # This first pass and the gx2/sx2 lines below are left over from an earlier version;
        # the positions actually used come from the gx3/sx3 pass.
        gx, sx = {}, [0.0] * ns
        for i in range(ns - 1):
            gx[i] = sx[i] + SD_HALF + wg[i] / 2
            sx[i + 1] = gx[i] + wg[i] / 2 + SD_HALF
            nxt = i + 1
            if nxt in self.extra_ws and nxt <= ns - 2:
                gnext = sx[i + 1] + SD_HALF + wg[nxt] / 2
                d = gnext - gx[i]
                if d < self.extra_ws[nxt]:
                    sx[i + 1] += (self.extra_ws[nxt] - d) / 2
        gx2 = {}
        for i in range(ns - 1):
            gx2[i] = gx[i]
        sx2 = [sx[0]]
        cur = sx[0]
        for i in range(ns - 1):
            pass
        shift = 0.0
        # Final pass: same walk, but the whole extra gap is added before a widened gate.
        gx3, sx3 = {}, [0.0] * ns
        for i in range(ns - 1):
            base_g = sx3[i] + SD_HALF + wg[i] / 2
            gx3[i] = base_g
            sx3[i + 1] = base_g + wg[i] / 2 + SD_HALF
            nxt = i + 1
            if nxt in self.extra_ws and nxt <= ns - 2:
                gnext = sx3[i + 1] + SD_HALF + wg[nxt] / 2
                d = gnext - gx3[i]
                if d < self.extra_ws[nxt]:
                    sx3[i + 1] += self.extra_ws[nxt] - d
        content_l = -DIFF_END
        content_r = sx3[-1] + DIFF_END
        width = content_r - content_l + 2 * 0.30
        W = math.ceil(round(width / 0.46, 6)) * 0.46
        off = R((W - (content_r - content_l)) / 2 - content_l)
        self.sx = [R(v + off) for v in sx3]
        self.gx = {i: R(v + off) for i, v in gx3.items()}
        self.wg = wg
        self.W = R(W)

    # Generate all the geometry: rails, taps, n-well, diffusion strips with contacts,
    # gate poly, poly bars and poly contacts, then route the signal nets.
    def build(self):
        self.validate()
        self.plan_pcs()
        self.place()
        self.geom = []
        g = self.geom
        rect = lambda layer, x1, y1, x2, y2: g.append((layer, R(x1), R(y1), R(x2), R(y2)))
        W = self.W
        # Power rails with substrate and well taps along the full cell width.
        rect("metal1", 0, -0.24, W, 0.24)
        rect("metal1", 0, 3.84, W, 4.32)
        rect("psubstratepdiff", 0.18, -0.145, W - 0.18, 0.145)
        rect("psubstratepcontact", 0.30, -0.085, W - 0.30, 0.085)
        rect("locali", 0.21, -0.165, W - 0.21, 0.165)
        rect("viali", 0.30, -0.085, W - 0.30, 0.085)
        rect("nsubstratendiff", 0.18, 3.935, W - 0.18, 4.225)
        rect("nsubstratencontact", 0.30, 3.995, W - 0.30, 4.165)
        rect("locali", 0.21, 3.915, W - 0.21, 4.245)
        rect("viali", 0.30, 3.995, W - 0.30, 4.165)
        rect("nwell", -0.23, NWELL_Y0, W + 0.23, 4.41)
        # Diffusion strips and their sd contacts. Contacts on GND/VDD go straight to the rail.
        self.sd_term = {}
        for rn, row in self.rows().items():
            dtype = "ndiffusion" if rn == "N" else "pdiffusion"
            ctype = "ndcontact" if rn == "N" else "pdcontact"
            for strip in self.strips(rn):
                wfs = {self.wf(row.G[i][1]) for i in strip}
                assert len(wfs) == 1, (self.name, rn, strip, wfs)
                wf = wfs.pop()
                y0, y1 = (N_Y0, N_Y0 + wf) if rn == "N" else (P_Y1 - wf, P_Y1)
                xl = self.sx[strip[0]] - DIFF_END
                xr = self.sx[strip[-1] + 1] + DIFF_END
                rect(dtype, xl, y0, xr, y1)
                for i in strip + [strip[-1] + 1]:
                    if (rn, i) in self.sd_term:
                        continue
                    x = self.sx[i]
                    cy0, cy1 = y0 + 0.06, y1 - 0.06
                    rect(ctype, x - 0.085, cy0, x + 0.085, cy1)
                    ly0, ly1 = cy0 - 0.08, cy1 + 0.08
                    net = row.S[i]
                    if rn == "N" and net == "GND":
                        ly0 = 0.0
                    if rn == "P" and net == "VDD":
                        ly1 = 4.08
                    rect("locali", x - 0.085, ly0, x + 0.085, ly1)
                    self.sd_term[(rn, i)] = (net, x, cy0, cy1)
        pcy = {}
        for c, info in self.pcs.items():
            pcy[c] = None
        self.pc_list = sorted(self.pcs)
        # Gate poly per finger, stretched to the poly bar when it joins a contact.
        self.assign_pc_tracks()
        for rn, row in self.rows().items():
            for i, (net, dev) in row.G.items():
                L = self.devs[dev]["L"]
                wf = self.wf(dev)
                x = self.gx[i]
                if rn == "N":
                    y0, y1 = N_Y0 - 0.13, N_Y0 + wf + 0.13
                    in_bar = any(b[0] == "N" and i in b[1] for b in self.bars)
                    if in_bar or (i in self.pcs and "N" in self.pcs[i]["rows"]):
                        y1 = N_BAR[1]
                else:
                    y0, y1 = P_Y1 - wf - 0.13, P_Y1 + 0.13
                    in_bar = any(b[0] == "P" and i in b[1] for b in self.bars)
                    if in_bar or (i in self.pcs and "P" in self.pcs[i]["rows"]):
                        y0 = P_BAR[0]
                rect("polysilicon", x - L / 2, y0, x + L / 2, y1)
        # Horizontal poly bars tying a run of fingers together.
        for rn, cols in self.bars:
            row = self.rows()[rn]
            xl = self.gx[cols[0]] - self.devs[row.G[cols[0]][1]]["L"] / 2
            xr = self.gx[cols[-1]] + self.devs[row.G[cols[-1]][1]]["L"] / 2
            y0, y1 = N_BAR if rn == "N" else P_BAR
            rect("polysilicon", xl, y0, xr, y1)
        # Poly contacts with their landing pad on the chosen middle track.
        self.pc_nodes = {}
        for c, info in self.pcs.items():
            x = self.gx[c]
            ty = TRACKS[info["track"]]
            Ls = [self.devs[r.G[c][1]]["L"] for r in (self.N, self.P) if c in r.G]
            sw = max(min(Ls), 0.15)
            ylo = N_BAR[0] if "N" in info["rows"] else ty
            yhi = P_BAR[1] if "P" in info["rows"] else ty
            rect("polysilicon", x - sw / 2, min(ylo, ty), x + sw / 2, max(yhi, ty))
            rect("polysilicon", x - 0.165, ty - 0.135, x + 0.165, ty + 0.135)
            rect("pcontact", x - 0.085, ty - 0.085, x + 0.085, ty + 0.085)
            rect("locali", x - 0.165, ty - 0.085, x + 0.165, ty + 0.085)
            rect("viali", x - 0.085, ty - 0.085, x + 0.085, ty + 0.085)
            self.pc_nodes[c] = (info["net"], info["track"], x)
        self.route()
        self.paint_routes(rect)

    # Put each net's poly contacts on C2 or C3 so different nets don't overlap.
    def assign_pc_tracks(self):
        nets = {}
        for c, info in self.pcs.items():
            nets.setdefault(info["net"], []).append(self.gx[c])
        spans = sorted(((min(v), max(v), n) for n, v in nets.items()))
        trk_end = {t: -1e9 for t in PC_TRACKS}
        choice = {}
        for lo, hi, n in spans:
            best = min(PC_TRACKS, key=lambda t: (trk_end[t] + MSEP > lo, trk_end[t]))
            choice[n] = best
            trk_end[best] = max(trk_end[best], hi)
        for c, info in self.pcs.items():
            info["track"] = choice[info["net"]]

    # Grid router. Columns are the sd and gate x positions, rows are the metal1 tracks.
    # Tries the largest nets first, then up to 400 random net orders until all fit.
    def route(self, seed=0):
        xs = sorted(set([("S", i, x) for i, x in enumerate(self.sx)] + [("G", i, x) for i, x in self.gx.items()]), key=lambda t: t[2])
        self.xs = xs
        xpos = [t[2] for t in xs]
        sidx = {t[1]: k for k, t in enumerate(xs) if t[0] == "S"}
        gidx = {t[1]: k for k, t in enumerate(xs) if t[0] == "G"}
        nets = {}
        for (rn, i), (net, x, cy0, cy1) in self.sd_term.items():
            if net in ("VDD", "GND"):
                continue
            nets.setdefault(net, []).append(("sd", rn, sidx[i]))
        for c, (net, trk, x) in self.pc_nodes.items():
            nets.setdefault(net, []).append(("pc", trk, gidx[c]))
        self.route_nets = nets
        fixed_m1 = {}
        for c, (net, trk, x) in self.pc_nodes.items():
            fixed_m1[(trk, gidx[c])] = net
        order0 = sorted(nets, key=lambda n: -len(nets[n]))
        rng = random.Random(seed)
        for attempt in range(400):
            order = order0 if attempt == 0 else rng.sample(order0, len(order0))
            ok, res = self.try_route(order, nets, fixed_m1, xpos, xs)
            if ok:
                self.routes = res
                self.xpos = xpos
                return
        raise RuntimeError(f"{self.name}: routing failed ({res})")

    # Route nets one at a time. Each terminal can land on any track of its row;
    # terminals are joined to the growing tree with A*, then the tree is reserved.
    def try_route(self, order, nets, fixed_m1, xpos, xs):
        m1 = dict(fixed_m1)
        m2 = {}
        mcon = {}
        res = {}
        tidx = {t: k for k, t in enumerate(TORDER)}

        # metal1 on track t at column k is free if no other net sits closer than MSEP.
        def m1_free(net, t, k):
            for kk in range(len(xpos)):
                o = m1.get((t, kk))
                if o is not None and o != net and abs(xpos[kk] - xpos[k]) < MSEP - 1e-9:
                    return False
            return True

        def m2_free(net, t, k):
            for tt in TORDER:
                o = m2.get((tt, k))
                if o is not None and o != net and abs(TRACKS[tt] - TRACKS[t]) < MSEP - 1e-9:
                    return False
            return True

        for net in order:
            terms = nets[net]
            cand = []
            for term in terms:
                if term[0] == "sd":
                    _, rn, k = term
                    cand.append([("m1", t, k) for t in ROW_TRACKS[rn]])
                else:
                    _, t, k = term
                    cand.append([("m1", t, k)])
            tree = set()
            paths = []
            first = None
            for opts in cand:
                ok_opts = [o for o in opts if m1_free(net, o[1], o[2])]
                if ok_opts:
                    first = ok_opts
                    break
            if first is None:
                return False, net
            start_order = sorted(range(len(cand)), key=lambda j: len(cand[j]))
            j0 = start_order[0]
            o0 = [o for o in cand[j0] if m1_free(net, o[1], o[2])]
            if not o0:
                return False, net
            tree.add(o0[0])
            used_terms = {j0: o0[0]}
            for j in start_order[1:]:
                opts = [o for o in cand[j] if m1_free(net, o[1], o[2])]
                if not opts:
                    return False, net
                if any(o in tree for o in opts):
                    used_terms[j] = [o for o in opts if o in tree][0]
                    continue
                p = self.astar(net, opts, tree, m1_free, m2_free, xpos, xs)
                if p is None:
                    return False, net
                for n_ in p:
                    tree.add(n_)
                used_terms[j] = p[0]
                paths.append(p)
            for n_ in tree:
                if n_[0] == "m1":
                    m1[(n_[1], n_[2])] = net
                else:
                    m2[(n_[1], n_[2])] = net
            res[net] = (tree, paths, used_terms, cand)
        return True, res

    # A* from the start options to any node of the existing tree. metal1 runs along a
    # track, metal2 runs vertically in sd columns, and a via costs 1.5 so it is used sparingly.
    def astar(self, net, starts, tree, m1_free, m2_free, xpos, xs):
        tidx = {t: k for k, t in enumerate(TORDER)}
        goal = tree

        def h(n):
            return min(abs(xpos[n[2]] - xpos[g[2]]) + abs(TRACKS[n[1]] - TRACKS[g[1]]) for g in goal)

        pq = []
        prev = {}
        dist = {}
        for s in starts:
            dist[s] = 0
            heapq.heappush(pq, (h(s), 0, s))
            prev[s] = None
        while pq:
            f, d, n = heapq.heappop(pq)
            if d > dist.get(n, 1e9):
                continue
            if n in goal:
                path = []
                while n is not None:
                    path.append(n)
                    n = prev[n]
                return path[::-1]
            lay, t, k = n
            nbrs = []
            if lay == "m1":
                for kk in (k - 1, k + 1):
                    if 0 <= kk < len(xpos) and m1_free(net, t, kk):
                        nbrs.append((("m1", t, kk), abs(xpos[kk] - xpos[k])))
                if xs[k][0] == "S" and m2_free(net, t, k):
                    nbrs.append((("m2", t, k), 1.5))
            else:
                ti = tidx[t]
                for tj in (ti - 1, ti + 1):
                    if 0 <= tj < len(TORDER):
                        tt = TORDER[tj]
                        if m2_free(net, tt, k):
                            nbrs.append((("m2", tt, k), abs(TRACKS[tt] - TRACKS[t]) * 1.2))
                if m1_free(net, t, k):
                    nbrs.append((("m1", t, k), 1.5))
            for m, c in nbrs:
                nd = d + c
                if nd < dist.get(m, 1e9) - 1e-12:
                    dist[m] = nd
                    prev[m] = n
                    heapq.heappush(pq, (nd + h(m), nd, m))
        return None

    # Turn routed grid nodes into rectangles: merged metal1 runs per track, metal2 runs
    # per column with vias, viali on sd terminals, and a pin box for each port.
    def paint_routes(self, rect):
        xpos = self.xpos
        self.pins = {}
        for net, (tree, paths, used_terms, cand) in self.routes.items():
            m1n = [n for n in tree if n[0] == "m1"]
            m2n = [n for n in tree if n[0] == "m2"]
            by_t = {}
            for _, t, k in m1n:
                by_t.setdefault(t, set()).add(k)
            for t, ks in by_t.items():
                y = TRACKS[t]
                ks = sorted(ks)
                runs, cur = [], [ks[0]]
                for k in ks[1:]:
                    if k == cur[-1] + 1:
                        cur.append(k)
                    else:
                        runs.append(cur); cur = [k]
                runs.append(cur)
                merged = []
                for r in runs:
                    if merged and xpos[r[0]] - xpos[merged[-1][-1]] < 0.32 + 0.14 + 1e-9:
                        merged[-1] = merged[-1] + r
                    else:
                        merged.append(list(r))
                for r in merged:
                    rect("metal1", xpos[r[0]] - 0.16, y - 0.13, xpos[r[-1]] + 0.16, y + 0.13)
            by_x = {}
            for _, t, k in m2n:
                by_x.setdefault(k, set()).add(TORDER.index(t))
            for k, ts in by_x.items():
                x = xpos[k]
                ts = sorted(ts)
                runs, cur = [], [ts[0]]
                for t in ts[1:]:
                    if t == cur[-1] + 1:
                        cur.append(t)
                    else:
                        runs.append(cur); cur = [t]
                runs.append(cur)
                for r in runs:
                    y0, y1 = TRACKS[TORDER[r[0]]], TRACKS[TORDER[r[-1]]]
                    rect("metal2", x - 0.13, y0 - 0.16, x + 0.13, y1 + 0.16)
                for t in ts:
                    y = TRACKS[TORDER[t]]
                    if ("m1", TORDER[t], k) in tree:
                        rect("via1", x - 0.13, y - 0.13, x + 0.13, y + 0.13)
                        rect("metal2", x - 0.13, y - 0.16, x + 0.13, y + 0.16)
            for j, node in used_terms.items():
                term = cand[j]
                if node[0] == "m1":
                    _, t, k = node
                    if self.xs[k][0] == "S":
                        rect("viali", xpos[k] - 0.085, TRACKS[t] - 0.085, xpos[k] + 0.085, TRACKS[t] + 0.085)
            if net in self.ports:
                _, t, k = sorted(m1n, key=lambda n: (TORDER.index(n[1]), n[2]))[len(m1n) // 2]
                self.pins[net] = (xpos[k] - 0.115, TRACKS[t] - 0.115, xpos[k] + 0.115, TRACKS[t] + 0.115)
        for p in self.ports:
            if p not in self.pins and p not in ("VDD", "GND"):
                raise RuntimeError(f"{self.name}: port {p} not routed")

    # Write the Magic script: one rect line per shape (grouped by layer, sorted), pins,
    # fixed bounding box, save, and report any port errors.
    def tcl(self, layout_dir):
        f = lambda v: ("%.3f" % v).rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"
        o = ["drc off", f"cd {layout_dir}", f"load {self.sub}", "", "set portErrors {}", "",
             "proc rect {layer x1 y1 x2 y2} {", "    box ${x1}um ${y1}um ${x2}um ${y2}um", "    paint $layer", "}",
             "proc pin {name x1 y1 x2 y2} {", "    global portErrors", "    box ${x1}um ${y1}um ${x2}um ${y2}um", "    label $name c metal1",
             "    select area labels", "    if {[catch {port make} msg]} { lappend portErrors \"$name: $msg\" }", "    select clear", "}", ""]
        order = ["nwell", "psubstratepdiff", "nsubstratendiff", "ndiffusion", "pdiffusion", "polysilicon", "psubstratepcontact", "nsubstratencontact",
                 "ndcontact", "pdcontact", "pcontact", "locali", "viali", "metal1", "via1", "metal2"]
        for layer in order:
            for (ly, x1, y1, x2, y2) in sorted(set(self.geom)):
                if ly == layer:
                    o.append(f"rect {ly} {f(x1)} {f(y1)} {f(x2)} {f(y2)}")
        o.append("")
        for p in self.ports:
            if p == "VDD":
                o.append(f"pin VDD 0.05 3.90 0.35 4.26")
            elif p == "GND":
                o.append(f"pin GND 0.05 -0.18 0.35 0.18")
            else:
                x1, y1, x2, y2 = self.pins[p]
                o.append(f"pin {p} {f(R(x1))} {f(R(y1))} {f(R(x2))} {f(R(y2))}")
        o += ["", f"property FIXED_BBOX {{0 0 {int(round(self.W * 100))} 408}}", "", "writeall force", "",
              "if {[llength $portErrors] > 0} {", "    foreach e $portErrors { puts \"PORT ERROR $e\" }", "} else {", "    puts \"Port errors: none\"", "}"]
        return "\n".join(o) + "\n"
