# RISC-V core benchmark: X4 vs sky130_fd_sc_hd at FO4

Workloads: sortcrc (6298 instructions), gemm (9949 instructions), stencil (4879 instructions), kmp (8541 instructions), spmv (9147 instructions).
Suite values are totals over all workloads: CPI = cycles / instructions, energy per instruction = energy / instructions, energy per cycle = energy / cycles.

## Suite summary

| Core | Library | Cells | Area (mm²) | Fmax | CPI | Instructions/s | Power at Fmax | Leakage | Energy/cycle | Energy/instr | Energy/instr vs hd |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SERV | X4, 0.40 V | 7777 | 0.260 | 8.83 kHz | 57.95 | 152 | 45.3 nW | 12.4 nW | 5.13 pJ | 297 pJ | 11.3× lower |
| SERV | hd, 1.80 V | 8408 | 0.058 | 394 MHz | 57.95 | 6.79 M | 22.7 mW | 29 nW | 57.8 pJ | 3.35 nJ | reference |
| FemtoRV32 Quark | X4, 0.40 V | 13582 | 0.403 | 5.39 kHz | 8.82 | 612 | 38.4 nW | 19.4 nW | 7.13 pJ | 62.8 pJ | 7.6× lower |
| FemtoRV32 Quark | hd, 1.80 V | 13589 | 0.081 | 234 MHz | 8.82 | 26.5 M | 12.6 mW | 42.9 nW | 54.1 pJ | 477 pJ | reference |
| PicoRV32 | X4, 0.40 V | 16579 | 0.477 | 8.31 kHz | 6.38 | 1.3 k | 63.2 nW | 22.5 nW | 7.61 pJ | 48.6 pJ | 9.0× lower |
| PicoRV32 | hd, 1.80 V | 16456 | 0.097 | 302 MHz | 6.38 | 47.3 M | 20.7 mW | 56.3 nW | 68.5 pJ | 437 pJ | reference |
| DarkRISCV | X4, 0.40 V | 15750 | 0.447 | 4.49 kHz | 1.26 | 3.56 k | 59 nW | 21.2 nW | 13.1 pJ | 16.6 pJ | 6.0× lower |
| DarkRISCV | hd, 1.80 V | 14993 | 0.087 | 204 MHz | 1.26 | 161 M | 16.2 mW | 48 nW | 79.4 pJ | 100 pJ | reference |

## Energy per instruction by workload

| Core | Library | sortcrc | gemm | stencil | kmp | spmv |
|---|---|---|---|---|---|---|
| SERV | X4, 0.40 V | 312 pJ | 313 pJ | 281 pJ | 258 pJ | 315 pJ |
| SERV | hd, 1.80 V | 3.48 nJ | 3.5 nJ | 3.16 nJ | 2.95 nJ | 3.56 nJ |
| SERV | X4 saving | 11.1× | 11.2× | 11.3× | 11.5× | 11.3× |
| FemtoRV32 Quark | X4, 0.40 V | 82.4 pJ | 72 pJ | 42.7 pJ | 32.5 pJ | 78.4 pJ |
| FemtoRV32 Quark | hd, 1.80 V | 621 pJ | 549 pJ | 321 pJ | 244 pJ | 600 pJ |
| FemtoRV32 Quark | X4 saving | 7.5× | 7.6× | 7.5× | 7.5× | 7.7× |
| PicoRV32 | X4, 0.40 V | 54 pJ | 51.9 pJ | 42.9 pJ | 38.8 pJ | 53.4 pJ |
| PicoRV32 | hd, 1.80 V | 483 pJ | 467 pJ | 386 pJ | 349 pJ | 484 pJ |
| PicoRV32 | X4 saving | 8.9× | 9.0× | 9.0× | 9.0× | 9.1× |
| DarkRISCV | X4, 0.40 V | 16 pJ | 17.5 pJ | 15.5 pJ | 15.9 pJ | 17.2 pJ |
| DarkRISCV | hd, 1.80 V | 95.8 pJ | 104 pJ | 94.8 pJ | 98.3 pJ | 103 pJ |
| DarkRISCV | X4 saving | 6.0× | 6.0× | 6.1× | 6.2× | 6.0× |

## Energy per cycle by workload

| Core | Library | sortcrc | gemm | stencil | kmp | spmv |
|---|---|---|---|---|---|---|
| SERV | X4, 0.40 V | 5.24 pJ | 5.21 pJ | 5.11 pJ | 4.95 pJ | 5.12 pJ |
| SERV | hd, 1.80 V | 58.3 pJ | 58.3 pJ | 57.6 pJ | 56.7 pJ | 57.8 pJ |
| SERV | X4 saving | 11.1× | 11.2× | 11.3× | 11.5× | 11.3× |
| FemtoRV32 Quark | X4, 0.40 V | 7.17 pJ | 6.98 pJ | 7.59 pJ | 7.68 pJ | 6.93 pJ |
| FemtoRV32 Quark | hd, 1.80 V | 54 pJ | 53.2 pJ | 56.9 pJ | 57.6 pJ | 53 pJ |
| FemtoRV32 Quark | X4 saving | 7.5× | 7.6× | 7.5× | 7.5× | 7.7× |
| PicoRV32 | X4, 0.40 V | 7.68 pJ | 7.55 pJ | 7.72 pJ | 7.76 pJ | 7.49 pJ |
| PicoRV32 | hd, 1.80 V | 68.6 pJ | 68 pJ | 69.4 pJ | 69.7 pJ | 67.9 pJ |
| PicoRV32 | X4 saving | 8.9× | 9.0× | 9.0× | 9.0× | 9.1× |
| DarkRISCV | X4, 0.40 V | 13.6 pJ | 13.6 pJ | 12.4 pJ | 12.3 pJ | 13.5 pJ |
| DarkRISCV | hd, 1.80 V | 81.3 pJ | 81.2 pJ | 76 pJ | 76 pJ | 81.2 pJ |
| DarkRISCV | X4 saving | 6.0× | 6.0× | 6.1× | 6.2× | 6.0× |

## CPI by workload

| Core | sortcrc | gemm | stencil | kmp | spmv |
|---|---|---|---|---|---|
| SERV | 59.61 | 60.11 | 54.96 | 52.05 | 61.57 |
| FemtoRV32 Quark | 11.50 | 10.32 | 5.63 | 4.23 | 11.31 |
| PicoRV32 | 7.04 | 6.87 | 5.56 | 5.00 | 7.13 |
| DarkRISCV | 1.18 | 1.29 | 1.25 | 1.29 | 1.27 |
