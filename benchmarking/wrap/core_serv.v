// Top level that gets synthesised: SERV (bit-serial, W=1) without CSRs, compressed ISA or multiplier.
// Unused outputs are left open and unused inputs tied to 0.

module core_serv (
  input  wire        clk,
  input  wire        i_rst,
  output wire [31:0] o_ibus_adr,
  output wire        o_ibus_cyc,
  input  wire [31:0] i_ibus_rdt,
  input  wire        i_ibus_ack,
  output wire [31:0] o_dbus_adr,
  output wire [31:0] o_dbus_dat,
  output wire [3:0]  o_dbus_sel,
  output wire        o_dbus_we,
  output wire        o_dbus_cyc,
  input  wire [31:0] i_dbus_rdt,
  input  wire        i_dbus_ack
);
  serv_rf_top #(
    .RESET_PC(32'd0),
    .COMPRESSED(1'b0),
    .MDU(1'b0),
    .PRE_REGISTER(1),
    .RESET_STRATEGY("MINI"),
    .WITH_CSR(0),
    .W(1)
  ) u_core (
    .clk(clk), .i_rst(i_rst), .i_timer_irq(1'b0),
    .o_ibus_adr(o_ibus_adr), .o_ibus_cyc(o_ibus_cyc), .i_ibus_rdt(i_ibus_rdt), .i_ibus_ack(i_ibus_ack),
    .o_dbus_adr(o_dbus_adr), .o_dbus_dat(o_dbus_dat), .o_dbus_sel(o_dbus_sel), .o_dbus_we(o_dbus_we),
    .o_dbus_cyc(o_dbus_cyc), .i_dbus_rdt(i_dbus_rdt), .i_dbus_ack(i_dbus_ack),
    .o_ext_rs1(), .o_ext_rs2(), .o_ext_funct3(), .i_ext_rd(32'd0), .i_ext_ready(1'b0), .o_mdu_valid()
  );
endmodule
