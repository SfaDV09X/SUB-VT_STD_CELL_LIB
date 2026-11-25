// Testbench for DarkRISCV, used for both the RTL (default) and the gate netlist (-DGATE).
// 8 KB memory loaded from +hex=<file>; the program ends by storing its result to 0x00800000,
// which is checked against +expect=<hex>. Every store is printed as "W cycle addr data mask"
// for the comparison with the ISS. Optional +vcd=<file> dumps the core's ports and internal
// nets (only while the program runs) and +maxcyc=<n> sets the timeout.

`timescale 1ns/1ps
module tb_dark;
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
  wire idreq, ddreq, drd, dwr;
  wire [31:0] iaddr, daddr, datao;
  wire [3:0] dbe;
  reg [31:0] idata, datai;
  reg [3:0] dtack = 4'd0;
  wire ddack = (dtack == 4'd1) | (ddreq & dwr);
`ifdef GATE
  core_dark_gate gate (
`else
  core_dark gate (
`endif
    .clk(clk), .res(rst), .idreq(idreq), .iaddr(iaddr), .idata(idata), .idack(idreq),
    .ddreq(ddreq), .daddr(daddr), .dbe(dbe), .drd(drd), .dwr(dwr), .datao(datao),
    .datai(datai), .ddack(ddack));
  // Memory model: separate instruction and data ports; instruction fetch always acked, loads acked one cycle later, stores at once.
  always @(posedge clk) begin
    idata <= mem[iaddr[12:2]];
    datai <= mem[daddr[12:2]];
    dtack <= rst ? 4'd0 : (dtack != 4'd0) ? dtack - 4'd1 : (ddreq & drd) ? 4'd1 : 4'd0;
    if (~rst & ddreq & dwr) begin
      $display("W %0d %h %h %b", cyc - start, daddr, datao, dbe);
      if (daddr == 32'h0080_0000) finish_run(datao);
      if (dbe[0]) mem[daddr[12:2]][7:0]   <= datao[7:0];
      if (dbe[1]) mem[daddr[12:2]][15:8]  <= datao[15:8];
      if (dbe[2]) mem[daddr[12:2]][23:16] <= datao[23:16];
      if (dbe[3]) mem[daddr[12:2]][31:24] <= datao[31:24];
    end
  end
endmodule
