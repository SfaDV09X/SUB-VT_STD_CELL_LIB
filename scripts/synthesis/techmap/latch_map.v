module \$_DLATCH_P_ (input E, input D, output Q);
  dlx1 _TECHMAP_REPLACE_ (.CLK(E), .D(D), .Q(Q), .QB());
endmodule

module \$_DLATCH_N_ (input E, input D, output Q);
  wire en_p;
  inv1x1 en_inv (.A(E), .Y(en_p));
  dlx1 _TECHMAP_REPLACE_ (.CLK(en_p), .D(D), .Q(Q), .QB());
endmodule
