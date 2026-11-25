// Testbench for FemtoRV32 Quark, used for both the RTL (default) and the gate netlist (-DGATE).
// 8 KB memory loaded from +hex=<file>; the program ends by storing its result to 0x00800000,
// which is checked against +expect=<hex>. Every store is printed as "W cycle addr data mask"
// for the comparison with the ISS. Optional +vcd=<file> dumps the core's ports and internal
// nets (only while the program runs) and +maxcyc=<n> sets the timeout.

`timescale 1ns/1ps
module tb_femto;
  reg clk = 1'b0;
  reg rst = 1'b1;
  reg [31:0] mem [0:2047];
  reg [1023:0] hexfile;
  reg [1023:0] vcdfile;
  integer cyc = 0;
  integer start = 0;
  integer maxcyc = 2000000;
  reg done = 1'b0;
  reg [31:0] exp_res = 32'd0;
  always #5 clk = ~clk;
  initial begin
    if (!$value$plusargs("hex=%s", hexfile)) begin $display("FAIL no +hex"); $finish; end
    $readmemh(hexfile, mem);
    if ($value$plusargs("vcd=%s", vcdfile)) begin
      $dumpfile(vcdfile);
      $dumpvars(1, gate);
      $dumpoff;
    end
    if ($value$plusargs("maxcyc=%d", maxcyc)) ;
    if (!$value$plusargs("expect=%h", exp_res)) begin $display("FAIL no +expect"); $finish; end
    repeat (8) @(posedge clk);
    #1 rst = 1'b0;
    start = cyc;
    if (vcdfile != 0) $dumpon;
  end
  always @(posedge clk) begin
    cyc <= cyc + 1;
    if (cyc > maxcyc) begin $display("FAIL timeout cycles=%0d", cyc - start); $finish; end
  end
  // Report result and cycle count, stop the VCD, print PASS/FAIL.
  task finish_run(input [31:0] v);
    begin
      if (vcdfile != 0) $dumpoff;
      $display("RESULT %08x", v);
      $display("CYCLES %0d", cyc - start);
      if (v === exp_res) $display("PASS"); else $display("FAIL result");
      $finish;
    end
  endtask
  wire [31:0] mem_addr, mem_wdata;
  wire [3:0] mem_wmask;
  wire mem_rstrb;
  reg [31:0] mem_rdata;
`ifdef GATE
  core_femto_gate gate (
`else
  core_femto gate (
`endif
    .clk(clk), .reset(~rst), .mem_addr(mem_addr), .mem_wdata(mem_wdata), .mem_wmask(mem_wmask),
    .mem_rdata(mem_rdata), .mem_rstrb(mem_rstrb), .mem_rbusy(1'b0), .mem_wbusy(1'b0));
  // Memory model: read strobe / write mask bus, data back on the next cycle, never busy.
  always @(posedge clk) begin
    if (mem_rstrb) mem_rdata <= mem[mem_addr[12:2]];
    if (~rst & |mem_wmask) begin
      $display("W %0d %h %h %b", cyc - start, mem_addr, mem_wdata, mem_wmask);
      if (mem_addr == 32'h0080_0000) finish_run(mem_wdata);
      if (mem_wmask[0]) mem[mem_addr[12:2]][7:0]   <= mem_wdata[7:0];
      if (mem_wmask[1]) mem[mem_addr[12:2]][15:8]  <= mem_wdata[15:8];
      if (mem_wmask[2]) mem[mem_addr[12:2]][23:16] <= mem_wdata[23:16];
      if (mem_wmask[3]) mem[mem_addr[12:2]][31:24] <= mem_wdata[31:24];
    end
  end
endmodule
