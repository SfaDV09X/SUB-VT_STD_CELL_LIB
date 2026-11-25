// Top level that gets synthesised: PicoRV32 as plain RV32I: no counters, IRQ, PCPI, MUL/DIV or compressed ISA.
// Unused outputs are left open and unused inputs tied to 0.

module core_pico (
  input  wire        clk,
  input  wire        resetn,
  output wire        mem_valid,
  output wire        mem_instr,
  input  wire        mem_ready,
  output wire [31:0] mem_addr,
  output wire [31:0] mem_wdata,
  output wire [3:0]  mem_wstrb,
  input  wire [31:0] mem_rdata
);
  picorv32 #(
    .ENABLE_COUNTERS(1'b0),
    .ENABLE_COUNTERS64(1'b0),
    .ENABLE_REGS_16_31(1'b1),
    .ENABLE_REGS_DUALPORT(1'b1),
    .COMPRESSED_ISA(1'b0),
    .ENABLE_MUL(1'b0),
    .ENABLE_DIV(1'b0),
    .ENABLE_IRQ(1'b0),
    .ENABLE_PCPI(1'b0),
    .PROGADDR_RESET(32'h0000_0000)
  ) u_core (
    .clk(clk), .resetn(resetn), .trap(),
    .mem_valid(mem_valid), .mem_instr(mem_instr), .mem_ready(mem_ready),
    .mem_addr(mem_addr), .mem_wdata(mem_wdata), .mem_wstrb(mem_wstrb), .mem_rdata(mem_rdata),
    .mem_la_read(), .mem_la_write(), .mem_la_addr(), .mem_la_wdata(), .mem_la_wstrb(),
    .pcpi_valid(), .pcpi_insn(), .pcpi_rs1(), .pcpi_rs2(),
    .pcpi_wr(1'b0), .pcpi_rd(32'd0), .pcpi_wait(1'b0), .pcpi_ready(1'b0),
    .irq(32'd0), .eoi(), .trace_valid(), .trace_data()
  );
endmodule
