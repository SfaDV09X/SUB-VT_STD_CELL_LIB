# Transistor sizing

sky130A, VDD 0.40 V. Every cell was sized for robustness at all 15 PVT corners, not for speed.

## Method
- **Design variables:** one W and one L per pull-down and pull-up network (Wn, Wp, Ln, Lp). Widths are multiples of 0.84 µm fingers (W is the total width, nf the number of fingers); lengths on a 0.01 µm grid.
- **Compound cells** (AND2, OR2, XOR2, XNOR2, MAOI4, MOAI4) reuse already-sized stages (NAND2, NOR2, INV1X4).
- **Load:** FO4 per cell (4 copies of the cell).
- **Objectives:** maximize worst-case noise margin, minimize delay, energy per operation, leakage.
- **Constraints:** NM ≥ 40 mV over the critical corners tt 27, sf 0, fs 85, ss 85, ff 85 °C; rise/fall asymmetry ≤ 0.25 at tt 27 °C; full 0–VDD swing in DC and transient.
- **Search:** Sobol sweep → Gaussian-process surrogates → multi-objective Bayesian optimization (EHVI), with NSGA-II and random search as baselines at equal budget.
- **Verification of picks:** all 15 PVT corners and mismatch Monte Carlo (Pelgrom Vth, 50 samples per critical corner, pass if mean − 3σ ≥ 0).
- **Sequential cells:** role-based sizing (clock inverter, input and feedback transmission gates, output inverter); hold SNM ≥ 40 mV at 15 corners; setup/hold reported only.

## Scripts (`scripts/sizing/`)
Run inside the container. Outputs go to `sizing_work/<run>/` in the repository (not tracked).

| Command | What it does |
|---|---|
| `bash scripts/sizing/run_cell.sh <cell>` | Sweep, dataset, feasibility, GP fit, MOBO / NSGA-II / random, pick, 15-PVT, Monte Carlo, finalists |
| `bash scripts/sizing/verify_cell.sh <cell> Wn Wp Ln Lp [...]` | 15-PVT, Monte Carlo and finalists for given designs |
| `bash scripts/sizing/run_seq.sh <dlx4\|dffx4>` | Stage A (storage-loop SNM) and stage B (input TG, clock inverter) sweeps |
| `bash scripts/sizing/verify_seq.sh <dlx4\|dffx4> Win Lin Wfb Lfb kclk kout kqb` | 15-PVT, Monte Carlo and setup/hold for one sequential design |
| `bash scripts/sizing/status.sh` | Progress of every run in `sizing_work/` |
| `python3 scripts/sizing/diagnose.py --dir sizing_work/<cell>` | Why designs fail after a sweep |

- Cells: inv1x4 nand2x4 nor2x4 and2x4 or2x4 xor2x4 xnor2x4 aoi3x4 oai3x4 maoi4x4 moai4x4. `and2x4_out` and `or2x4_out` size only the output inverter of AND2X4 / OR2X4 with the NAND2 / NOR2 stage fixed.
- `baseline` in `cells.py` is each cell's starting design for the search, not the result.
- Sequential variables: input TG width/length (Win, Lin), feedback TG width/length (Wfb, Lfb); PMOS = 2 × NMOS width; kclk, kout, kqb = clock, output and QB-driver inverters as multiples of INV1X4.
- Environment: `WORKERS` (8), `NSWEEP` (96), `MCN` (50), `NA` (48), `NB` (16).

Reproduce the committed sizing:
```
bash scripts/sizing/verify_cell.sh inv1x4 0.84 1.68 0.29 0.21
bash scripts/sizing/verify_cell.sh nand2x4 3.36 5.04 0.26 0.22
bash scripts/sizing/verify_cell.sh nor2x4 2.52 4.20 0.26 0.20
bash scripts/sizing/verify_cell.sh and2x4_out 2.52 5.04 0.29 0.21
bash scripts/sizing/verify_cell.sh or2x4_out 2.52 5.04 0.29 0.21
bash scripts/sizing/verify_cell.sh xor2x4 4.20 4.20 0.29 0.19
bash scripts/sizing/verify_cell.sh xnor2x4 4.20 4.20 0.29 0.19
bash scripts/sizing/verify_cell.sh aoi3x4 4.20 5.04 0.26 0.20
bash scripts/sizing/verify_cell.sh oai3x4 4.20 5.04 0.26 0.20
bash scripts/sizing/verify_cell.sh maoi4x4 3.36 4.20 0.28 0.20
bash scripts/sizing/verify_cell.sh moai4x4 3.36 4.20 0.28 0.20
bash scripts/sizing/verify_seq.sh dlx4 1.68 0.19 0.42 0.47 2 2 2
bash scripts/sizing/verify_seq.sh dffx4 0.84 0.19 0.42 0.32 2 2 2
```

## Final sizing
W and L in µm; nf = number of 0.84 µm fingers (0.42 = one 0.42 µm finger).

| Cell | Devices | Role | Type | W | nf | L |
|---|---|---|---|---|---|---|
| INV1X4 | NMOS | pull-down | nfet | 0.84 | 1 | 0.29 |
| INV1X4 | PMOS | pull-up | pfet | 1.68 | 2 | 0.21 |
| NAND2X4 | NMOS (both, series) | pull-down | nfet | 3.36 | 4 | 0.26 |
| NAND2X4 | PMOS (both, parallel) | pull-up | pfet | 5.04 | 6 | 0.22 |
| NOR2X4 | NMOS (both, parallel) | pull-down | nfet | 2.52 | 3 | 0.26 |
| NOR2X4 | PMOS (both, series) | pull-up | pfet | 4.20 | 5 | 0.20 |
| AND2X4 | XM1, XM2 | NAND | nfet | 3.36 | 4 | 0.26 |
| AND2X4 | XM3, XM4 | NAND | pfet | 5.04 | 6 | 0.22 |
| AND2X4 | XM5 | output inverter | nfet | 2.52 | 3 | 0.29 |
| AND2X4 | XM6 | output inverter | pfet | 5.04 | 6 | 0.21 |
| OR2X4 | XM1, XM2 | NOR | nfet | 2.52 | 3 | 0.26 |
| OR2X4 | XM3, XM4 | NOR | pfet | 4.20 | 5 | 0.20 |
| OR2X4 | XM6 | output inverter | nfet | 2.52 | 3 | 0.29 |
| OR2X4 | XM5 | output inverter | pfet | 5.04 | 6 | 0.21 |
| XOR2X4, XNOR2X4 | XM1–XM4 | core (series pairs) | nfet | 4.20 | 5 | 0.29 |
| XOR2X4, XNOR2X4 | XM5–XM8 | core (series pairs) | pfet | 4.20 | 5 | 0.19 |
| XOR2X4, XNOR2X4 | XM9, XM11 | input inverters | nfet | 0.84 | 1 | 0.29 |
| XOR2X4, XNOR2X4 | XM10, XM12 | input inverters | pfet | 1.68 | 2 | 0.21 |
| AOI3X4 | XM4, XM6 | A, B (series) | nfet | 4.20 | 5 | 0.26 |
| AOI3X4 | XM5 | C | nfet | 2.52 | 3 | 0.26 |
| AOI3X4 | XM1, XM2, XM3 | A, B, C | pfet | 5.04 | 6 | 0.20 |
| OAI3X4 | XM4, XM5, XM6 | A, B, C | nfet | 4.20 | 5 | 0.26 |
| OAI3X4 | XM1, XM2 | A, B (series) | pfet | 5.04 | 6 | 0.20 |
| OAI3X4 | XM3 | C | pfet | 2.52 | 3 | 0.20 |
| MAOI4X4 | XM1–XM4 | core (series pairs) | nfet | 3.36 | 4 | 0.28 |
| MAOI4X4 | XM5–XM8 | core (shared node) | pfet | 4.20 | 5 | 0.20 |
| MAOI4X4 | XM9, XM11 | input inverters | nfet | 0.84 | 1 | 0.29 |
| MAOI4X4 | XM10, XM12 | input inverters | pfet | 1.68 | 2 | 0.21 |
| MOAI4X4 | XM3–XM6 | core (shared node) | nfet | 3.36 | 4 | 0.28 |
| MOAI4X4 | XM1, XM2, XM7, XM8 | core (series pairs) | pfet | 4.20 | 5 | 0.20 |
| MOAI4X4 | XM9, XM12 | input inverters | nfet | 0.84 | 1 | 0.29 |
| MOAI4X4 | XM10, XM11 | input inverters | pfet | 1.68 | 2 | 0.21 |
| DLX4 | XM4 / XM3 | clock inverter | nfet / pfet | 1.68 / 3.36 | 2 / 4 | 0.29 / 0.21 |
| DLX4 | XM2 / XM1 | input TG | nfet / pfet | 1.68 / 3.36 | 2 / 4 | 0.19 |
| DLX4 | XM10 / XM7 | feedback TG | nfet / pfet | 0.42 / 0.84 | 1 / 1 | 0.47 |
| DLX4 | XM8 / XM9 | QB driver | nfet / pfet | 1.68 / 3.36 | 2 / 4 | 0.29 / 0.21 |
| DLX4 | XM6 / XM5 | output inverter | nfet / pfet | 1.68 / 3.36 | 2 / 4 | 0.29 / 0.21 |
| DFFX4 | XM4 / XM3 | clock inverter | nfet / pfet | 1.68 / 3.36 | 2 / 4 | 0.29 / 0.21 |
| DFFX4 | XM2, XM5 / XM1, XM18 | input TGs (master, slave) | nfet / pfet | 0.84 / 1.68 | 1 / 2 | 0.19 |
| DFFX4 | XM16, XM14 / XM15, XM13 | feedback TGs (master, slave) | nfet / pfet | 0.42 / 0.84 | 1 / 1 | 0.32 |
| DFFX4 | XM8, XM6 / XM7, XM17 | master inverters | nfet / pfet | 0.84 / 1.68 | 1 / 2 | 0.29 / 0.21 |
| DFFX4 | XM10 / XM9 | QB driver | nfet / pfet | 1.68 / 3.36 | 2 / 4 | 0.29 / 0.21 |
| DFFX4 | XM12 / XM11 | output inverter | nfet / pfet | 1.68 / 3.36 | 2 / 4 | 0.29 / 0.21 |
