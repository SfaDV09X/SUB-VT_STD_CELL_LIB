`timescale 1ns/1ps
module tb_rca8;
    reg  [7:0] a, b;
    reg        cin;
    wire [7:0] s_g, s_n;
    wire       c_g, c_n;
    rca8      gold (.a(a), .b(b), .cin(cin), .sum(s_g), .cout(c_g));
    rca8_gate gate (.a(a), .b(b), .cin(cin), .sum(s_n), .cout(c_n));
    integer i, j, k, checks, errors;
    reg [8:0] expv;
    initial begin
        checks = 0; errors = 0;
        for (i = 0; i < 256; i = i + 1)
            for (j = 0; j < 256; j = j + 1)
                for (k = 0; k < 2; k = k + 1) begin
                    a = i; b = j; cin = k; #1;
                    expv = i + j + k;
                    checks = checks + 1;
                    if ({c_g, s_g} !== expv || {c_n, s_n} !== expv) begin
                        errors = errors + 1;
                        if (errors <= 10)
                            $display("MISMATCH a=%0d b=%0d cin=%0d exp=%0d gold=%0d gate=%0d", i, j, k, expv, {c_g, s_g}, {c_n, s_n});
                    end
                end
        $display("%s  checks=%0d mismatches=%0d", errors == 0 ? "PASS" : "FAIL", checks, errors);
        $finish;
    end
endmodule
