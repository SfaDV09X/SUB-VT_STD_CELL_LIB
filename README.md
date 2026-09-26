# Sub-Threshold Standard Cell Library

Open-source sub-threshold digital standard cell library targeting SkyWater 130nm PDK.
Built with the IIC-OSIC-TOOLS open EDA toolchain.

## Naming convention
- Combinational: (FUNCTION)(FANIN)X(FANOUT) — INV1X1, NAND2X1, NOR2X1, AND2X1, OR2X1, XOR2X1,
  XNOR2X1, AOI3X1, OAI3X1, MAOI4X1, MOAI4X1.
- Sequential: (FUNCTION)X(FANOUT) — DLX1, DFFX1, DFFSRX1.

## Toolchain
- Schematic design + analysis: Xschem + ngspice
- Layout: Magic
- Verification: Magic (DRC) + Netgen (LVS) + Magic (PEX)
- Characterization: lctime / charlib
- Synthesis validation: Yosys + OpenROAD
