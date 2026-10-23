(* keep_hierarchy *) module cov_inv1x1  (input a,       output y); assign y = ~a;                        endmodule
(* keep_hierarchy *) module cov_nand2x1 (input a, b,    output y); assign y = ~(a & b);                  endmodule
(* keep_hierarchy *) module cov_nor2x1  (input a, b,    output y); assign y = ~(a | b);                  endmodule
(* keep_hierarchy *) module cov_and2x1  (input a, b,    output y); assign y = a & b;                     endmodule
(* keep_hierarchy *) module cov_or2x1   (input a, b,    output y); assign y = a | b;                     endmodule
(* keep_hierarchy *) module cov_xor2x1  (input a, b,    output y); assign y = a ^ b;                     endmodule
(* keep_hierarchy *) module cov_xnor2x1 (input a, b,    output y); assign y = ~(a ^ b);                  endmodule
(* keep_hierarchy *) module cov_aoi3x1  (input a, b, c, output y); assign y = ~((a & b) | c);            endmodule
(* keep_hierarchy *) module cov_oai3x1  (input a, b, c, output y); assign y = ~((a | b) & c);            endmodule
(* keep_hierarchy *) module cov_moai4x1 (input a, b, c, d, output y); assign y = (a & b) | (~c & ~d);    endmodule
(* keep_hierarchy *) module cov_maoi4x1 (input a, b, c, d, output y); assign y = (a | b) & ~(c & d);     endmodule

module demo (
    input        clk,
    input        rst,
    input        set,
    input        ld,
    input        en_l,
    input  [3:0] a, b, c, d,
    input        cin,
    output [3:0] a_n,
    output       y_nand,
    output       y_nor,
    output       y_and,
    output       y_or,
    output [3:0] x_ab,
    output [3:0] xn_ab,
    output       y_aoi,
    output       y_oai,
    output       y_moai,
    output       y_maoi,
    output reg [4:0] sum_q,
    output reg       eq_q,
    output reg       par_q,
    output reg [3:0] sr_q  
    output reg [3:0] lat_q     
);
    genvar i;
    generate for (i = 0; i < 4; i = i + 1) begin : g
        cov_inv1x1  u_inv  (.a(a[i]),            .y(a_n[i]));
        cov_xor2x1  u_xor  (.a(a[i]), .b(b[i]),  .y(x_ab[i]));
        cov_xnor2x1 u_xnor (.a(a[i]), .b(b[i]),  .y(xn_ab[i]));
    end endgenerate

    cov_nand2x1 u_nand (.a(a[0]), .b(b[0]), .y(y_nand));
    cov_nor2x1  u_nor  (.a(a[1]), .b(b[1]), .y(y_nor));
    cov_and2x1  u_and  (.a(a[2]), .b(b[2]), .y(y_and));
    cov_or2x1   u_or   (.a(a[3]), .b(b[3]), .y(y_or));
    cov_aoi3x1  u_aoi  (.a(c[0]), .b(d[0]), .c(cin),  .y(y_aoi));
    cov_oai3x1  u_oai  (.a(c[1]), .b(d[1]), .c(cin),  .y(y_oai));
    cov_moai4x1 u_moai (.a(a[0]), .b(c[2]), .c(b[2]), .d(d[2]), .y(y_moai));
    cov_maoi4x1 u_maoi (.a(a[1]), .b(c[3]), .c(b[3]), .d(d[3]), .y(y_maoi));

    always @(posedge clk) begin
        sum_q <= a + b + cin;
        eq_q  <= (a == b);
        par_q <= ^c;
        if (rst)      sr_q <= 4'b0000;
        else if (set) sr_q <= 4'b1111;
        else if (ld)  sr_q <= c;
        else          sr_q <= sr_q ^ d;
    end

    always @* if (en_l) lat_q = d;
endmodule
