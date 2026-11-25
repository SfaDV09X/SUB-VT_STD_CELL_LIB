// Top level that gets synthesised: FemtoRV32 Quark (RV32I) with reset at address 0 and a 24-bit address space.
// Unused outputs are left open and unused inputs tied to 0.

module core_femto (
  input  wire        clk,
  input  wire        reset,
  output wire [31:0] mem_addr,
  output wire [31:0] mem_wdata,
  output wire [3:0]  mem_wmask,
  input  wire [31:0] mem_rdata,
  output wire        mem_rstrb,
  input  wire        mem_rbusy,
  input  wire        mem_wbusy
);
  FemtoRV32 #(
    .RESET_ADDR(32'h0000_0000),
    .ADDR_WIDTH(24)
  ) u_core (
    .clk(clk), .mem_addr(mem_addr), .mem_wdata(mem_wdata), .mem_wmask(mem_wmask),
    .mem_rdata(mem_rdata), .mem_rstrb(mem_rstrb), .mem_rbusy(mem_rbusy), .mem_wbusy(mem_wbusy),
    .reset(reset)
  );
endmodule
