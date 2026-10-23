`timescale 1ns/1ps

module tb_demo;
    reg clk = 0, rst = 1, set = 0, ld = 0, en_l = 1, cin = 0;
    reg [3:0] a = 0, b = 0, c = 0, d = 0;

    wire [3:0] g_a_n, g_x_ab, g_xn_ab, g_sr_q, g_lat_q;  wire [4:0] g_sum_q;
    wire       g_y_nand, g_y_nor, g_y_and, g_y_or, g_y_aoi, g_y_oai, g_y_moai, g_y_maoi, g_eq_q, g_par_q;
    wire [3:0] n_a_n, n_x_ab, n_xn_ab, n_sr_q, n_lat_q;  wire [4:0] n_sum_q;
    wire       n_y_nand, n_y_nor, n_y_and, n_y_or, n_y_aoi, n_y_oai, n_y_moai, n_y_maoi, n_eq_q, n_par_q;

    demo            gold (.clk(clk), .rst(rst), .set(set), .ld(ld), .en_l(en_l), .a(a), .b(b), .c(c), .d(d), .cin(cin),
        .a_n(g_a_n), .y_nand(g_y_nand), .y_nor(g_y_nor), .y_and(g_y_and), .y_or(g_y_or), .x_ab(g_x_ab), .xn_ab(g_xn_ab),
        .y_aoi(g_y_aoi), .y_oai(g_y_oai), .y_moai(g_y_moai), .y_maoi(g_y_maoi),
        .sum_q(g_sum_q), .eq_q(g_eq_q), .par_q(g_par_q), .sr_q(g_sr_q), .lat_q(g_lat_q));
    demo_gate       gate (.clk(clk), .rst(rst), .set(set), .ld(ld), .en_l(en_l), .a(a), .b(b), .c(c), .d(d), .cin(cin),
        .a_n(n_a_n), .y_nand(n_y_nand), .y_nor(n_y_nor), .y_and(n_y_and), .y_or(n_y_or), .x_ab(n_x_ab), .xn_ab(n_xn_ab),
        .y_aoi(n_y_aoi), .y_oai(n_y_oai), .y_moai(n_y_moai), .y_maoi(n_y_maoi),
        .sum_q(n_sum_q), .eq_q(n_eq_q), .par_q(n_par_q), .sr_q(n_sr_q), .lat_q(n_lat_q));

    wire [57:0] gv = {g_a_n,g_y_nand,g_y_nor,g_y_and,g_y_or,g_x_ab,g_xn_ab,g_y_aoi,g_y_oai,g_y_moai,g_y_maoi,g_sum_q,g_eq_q,g_par_q,g_sr_q,g_lat_q};
    wire [57:0] nv = {n_a_n,n_y_nand,n_y_nor,n_y_and,n_y_or,n_x_ab,n_xn_ab,n_y_aoi,n_y_oai,n_y_moai,n_y_maoi,n_sum_q,n_eq_q,n_par_q,n_sr_q,n_lat_q};

    always #50 clk = ~clk;

    integer i, errors = 0, checks = 0;
    integer seed = 32'h5eed;
    localparam N = (1 << 17) + 4000;

    initial begin
        repeat (3) @(negedge clk);
        rst = 0;
        for (i = 0; i < N; i = i + 1) begin
            @(negedge clk);
            {cin, d, c, b, a} = (i < (1 << 17)) ? i[16:0] : $random(seed);
            rst  = (($random(seed) & 31) == 0);
            set  = (($random(seed) & 15) == 0);
            ld   = $random(seed);
            en_l = $random(seed);
        end
        $display("%s  checks=%0d mismatches=%0d", errors == 0 ? "PASS" : "FAIL", checks, errors);
        $finish;
    end

    always @(posedge clk) if ($time > 400) begin
        #40;
        checks = checks + 1;
        if (gv !== nv) begin
            errors = errors + 1;
            if (errors <= 10) $display("MISMATCH t=%0t in={cin,d,c,b,a}=%h  gold=%h gate=%h", $time, {cin,d,c,b,a}, gv, nv);
        end
    end
endmodule
