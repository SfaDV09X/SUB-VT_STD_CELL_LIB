# RISC-V benchmark sources

Four open-source RV32I cores at fixed commits, their wrappers (`wrap/`), testbenches (`tb/`), five workloads (`prog/`) and the committed results (`results/`).

| Core | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
| SERV | github.com/olofk/serv | `f200eb2e` | ISC | none |
| FemtoRV32 Quark | github.com/BrunoLevy/learn-fpga | `f5ada24a` | BSD-3-Clause | `cores/femtorv32/asic.patch` (x0 reads 0, shift counter reset) |
| PicoRV32 | github.com/YosysHQ/picorv32 | `ef203c2b` | ISC | none |
| DarkRISCV | github.com/darklife/darkriscv | `bb6b483c` | BSD-3-Clause | own `rtl/config.vh` (3-stage, reset PC 0) |

Workloads: `sortcrc`, `gemm`, `stencil`, `kmp`, `spmv` (C in `prog/src/`, built `.hex` in `prog/`, rebuild with `prog/build.sh`).
