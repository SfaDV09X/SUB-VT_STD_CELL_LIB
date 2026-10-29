`timescale 1ns/1ps
module tb_counter8;
    reg        clk, rst, en;
    wire [7:0] q_g, q_n;
    counter8      gold (.clk(clk), .rst(rst), .en(en), .q(q_g));
    counter8_gate gate (.clk(clk), .rst(rst), .en(en), .q(q_n));
    reg [7:0] model;
    integer n, checks, errors;
    always #5 clk = ~clk;
    always @(posedge clk) begin
        if (rst)     model <= 8'd0;
        else if (en) model <= model + 8'd1;
    end
    initial begin
        clk = 0; rst = 1; en = 0; checks = 0; errors = 0;
        repeat (3) @(negedge clk);
        for (n = 0; n < 800; n = n + 1) begin
            rst = (n >= 300 && n < 303);
            en  = (($random & 3) != 0);
            @(negedge clk);
            checks = checks + 1;
            if (q_g !== model || q_n !== model) begin
                errors = errors + 1;
                if (errors <= 10)
                    $display("MISMATCH cycle=%0d model=%0d gold=%0d gate=%0d", n, model, q_g, q_n);
            end
        end
        $display("%s  checks=%0d mismatches=%0d", errors == 0 ? "PASS" : "FAIL", checks, errors);
        $finish;
    end
endmodule
