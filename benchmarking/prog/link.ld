/* Everything in one 8 KB RAM starting at 0; start.S code goes first so the reset PC (0) runs it. */

MEMORY { RAM (rwx) : ORIGIN = 0, LENGTH = 8K }
SECTIONS {
  .text : { *(.text.start) *(.text*) } > RAM
  .rodata : { *(.rodata*) *(.srodata*) } > RAM
  .data : { *(.data*) *(.sdata*) } > RAM
  .bss : { *(.bss*) *(.sbss*) *(COMMON) } > RAM
}
