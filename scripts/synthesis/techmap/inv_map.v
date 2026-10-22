// 1:1 inverter mapping, used for the cov_inv1x1 leaf only.
// ABC's "map" cannot process a network that contains no AND node (a bare inverter).
module \$_NOT_ (input A, output Y);
  inv1x1 _TECHMAP_REPLACE_ (.A(A), .Y(Y));
endmodule
