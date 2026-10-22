// Maps Yosys generic latches onto DLX1 (transparent while CLK = 1, outputs Q / QB).
// dfflibmap in Yosys does not map latches, so this is done with techmap.
// Used after: dfflegalize -cell $_DLATCH_P_ x -cell $_DLATCH_N_ x
module \$_DLATCH_P_ (input E, input D, output Q);
  dlx1 _TECHMAP_REPLACE_ (.CLK(E), .D(D), .Q(Q), .QB());
endmodule

// Active-low enable: invert E with INV1X1 and feed DLX1.
module \$_DLATCH_N_ (input E, input D, output Q);
  wire en_p;
  inv1x1 en_inv (.A(E), .Y(en_p));
  dlx1 _TECHMAP_REPLACE_ (.CLK(en_p), .D(D), .Q(Q), .QB());
endmodule
