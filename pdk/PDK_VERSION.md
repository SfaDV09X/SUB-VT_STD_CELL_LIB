# PDK and tool versions

Docker image `hpretl/iic-osic-tools:2026.07`.

| Item | Version |
|---|---|
| PDK | sky130A (open_pdks commit f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7) |
| xschem | 3.4.8RC |
| ngspice | 46 |
| Magic | 8.3.678 |
| Netgen | 1.5.323 |
| lctime | 0.0.26 |
| Yosys | 0.67 |
| Icarus Verilog | 14.0 |

The committed characterization and synthesis results were produced outside the container with ngspice 42, lctime 0.0.26, Yosys 0.33, Icarus Verilog 12.0 and OpenSTA 3.2.0, on the same sky130A models.
