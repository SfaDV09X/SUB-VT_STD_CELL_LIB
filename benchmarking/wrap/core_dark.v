// Top level that gets synthesised: DarkRISCV (3-stage pipeline, see rtl/config.vh) with the bus error inputs tied off.
// Unused outputs are left open and unused inputs tied to 0.

module core_dark (
  input  wire        clk,
  input  wire        res,
  output wire        idreq,
  output wire [31:0] iaddr,
  input  wire [31:0] idata,
  input  wire        idack,
  output wire        ddreq,
  output wire [31:0] daddr,
  output wire [3:0]  dbe,
  output wire        drd,
  output wire        dwr,
  output wire [31:0] datao,
  input  wire [31:0] datai,
  input  wire        ddack
);
  darkriscv #(.CPTR(0)) u_core (
    .CLK(clk), .RES(res),
    .IDREQ(idreq), .IADDR(iaddr), .IDATA(idata), .IDACK(idack), .IBERR(1'b0),
    .DDREQ(ddreq), .DADDR(daddr), .DLEN(), .DBE(dbe), .DRW(), .DRD(drd), .DWR(dwr),
    .DATAO(datao), .DATAI(datai), .DDACK(ddack), .DBERR(1'b0),
    .DEBUG()
  );
endmodule
