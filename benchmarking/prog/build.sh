#!/bin/bash
# Build the workload programs: <name>.hex (memory image for the testbenches and the ISS)
# and <name>.dis (disassembly). RV32I only, no libc; uses the RISC-V GCC if installed,
# otherwise clang/lld. Usage: bash build.sh [workload ...]

set -e
cd "$(dirname "$0")"
W=${*:-sortcrc gemm stencil kmp spmv}
for w in $W; do
  if command -v riscv64-unknown-elf-gcc >/dev/null; then
    riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -O2 -ffreestanding -nostdlib -fno-builtin -T link.ld start.S src/$w.c src/rt.c -o $w.elf
    riscv64-unknown-elf-objcopy -O binary $w.elf $w.bin
    riscv64-unknown-elf-objdump -d $w.elf > $w.dis
  else
    clang --target=riscv32-unknown-elf -march=rv32i -mabi=ilp32 -O2 -ffreestanding -nostdlib -fno-builtin -mno-relax -fuse-ld=lld -T link.ld start.S src/$w.c src/rt.c -o $w.elf
    llvm-objcopy -O binary $w.elf $w.bin
    llvm-objdump -d $w.elf > $w.dis
  fi
  # Raw binary -> one 32-bit little-endian word per line for $readmemh.
  python3 -c "
import struct
d = open('$w.bin', 'rb').read()
d += b'\0' * ((-len(d)) % 4)
w = struct.unpack('<%dI' % (len(d) // 4), d)
open('$w.hex', 'w').write('\n'.join('%08x' % x for x in w) + '\n')
"
  rm -f $w.bin $w.elf
done
