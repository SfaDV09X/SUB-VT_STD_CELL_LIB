// Testbench for SERV, used for both the RTL (default) and the gate netlist (-DGATE).
// 8 KB memory loaded from +hex=<file>; the program ends by storing its result to 0x00800000,
// which is checked against +expect=<hex>. Every store is printed as "W cycle addr data mask"
// for the comparison with the ISS. Optional +vcd=<file> dumps the core's ports and internal
// nets (only while the program runs) and +maxcyc=<n> sets the timeout.

`timescale 1ns/1ps
module tb_serv;
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
  wire [31:0] ibus_adr, dbus_adr, dbus_dat;
  wire ibus_cyc, dbus_cyc, dbus_we;
  wire [3:0] dbus_sel;
  reg [31:0] ibus_rdt, dbus_rdt;
  reg ibus_ack = 1'b0, dbus_ack = 1'b0;
`ifdef GATE
  core_serv_gate gate (
`else
  core_serv gate (
`endif
    .clk(clk), .i_rst(rst),
    .o_ibus_adr(ibus_adr), .o_ibus_cyc(ibus_cyc), .i_ibus_rdt(ibus_rdt), .i_ibus_ack(ibus_ack),
    .o_dbus_adr(dbus_adr), .o_dbus_dat(dbus_dat), .o_dbus_sel(dbus_sel), .o_dbus_we(dbus_we),
    .o_dbus_cyc(dbus_cyc), .i_dbus_rdt(dbus_rdt), .i_dbus_ack(dbus_ack));
  // Memory model: Wishbone-style instruction and data buses, each acked one cycle after a request.
  always @(posedge clk) begin
    ibus_ack <= ibus_cyc & ~ibus_ack & ~rst;
    ibus_rdt <= mem[ibus_adr[12:2]];
    dbus_ack <= dbus_cyc & ~dbus_ack & ~rst;
    dbus_rdt <= mem[dbus_adr[12:2]];
    if (dbus_cyc & ~dbus_ack & dbus_we & ~rst) begin
      $display("W %0d %h %h %b", cyc - start, dbus_adr, dbus_dat, dbus_sel);
      if (dbus_adr == 32'h0080_0000) finish_run(dbus_dat);
      if (dbus_sel[0]) mem[dbus_adr[12:2]][7:0]   <= dbus_dat[7:0];
      if (dbus_sel[1]) mem[dbus_adr[12:2]][15:8]  <= dbus_dat[15:8];
      if (dbus_sel[2]) mem[dbus_adr[12:2]][23:16] <= dbus_dat[23:16];
      if (dbus_sel[3]) mem[dbus_adr[12:2]][31:24] <= dbus_dat[31:24];
    end
  end
endmodule
