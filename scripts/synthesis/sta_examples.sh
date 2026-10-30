#!/usr/bin/env bash
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
LIB=${LIB:-$ROOT/lib/subvt_sky130_tt_0p40v_27c.lib}
SYNTH=${SYNTH:-/tmp/subvt_examples/synth}
OUT=${OUT:-/tmp/subvt_examples/sta}
mkdir -p "$OUT"
STA=""
for c in sta opensta; do command -v $c >/dev/null 2>&1 && { STA="$c -no_splash -exit"; break; }; done
[ -z "$STA" ] && command -v openroad >/dev/null 2>&1 && STA="openroad -no_splash -exit"
[ -z "$STA" ] && { echo "ERROR: none of sta, opensta, openroad found in PATH"; exit 2; }
[ -f "$LIB" ] || { echo "ERROR: liberty not found: $LIB   (set LIB=...)"; exit 2; }
for t in rca8 counter8; do
  [ -f "$SYNTH/$t/${t}_gate.v" ] || { echo "ERROR: $SYNTH/$t/${t}_gate.v missing (run synth_examples.sh first)"; exit 2; }
done

cat > "$OUT/rca8.tcl" <<TCL
read_liberty $LIB
read_verilog $SYNTH/rca8/rca8_gate.v
link_design rca8_gate
create_clock -name vclk -period 1000000
set_input_delay 0 -clock vclk [all_inputs]
set_output_delay 0 -clock vclk [all_outputs]
report_checks -path_delay max -digits 3 -format full
TCL
cat > "$OUT/counter8.tcl" <<TCL
read_liberty $LIB
read_verilog $SYNTH/counter8/counter8_gate.v
link_design counter8_gate
create_clock -name clk -period 1000000 [get_ports clk]
set_input_delay 0 -clock clk [get_ports {rst en}]
set_output_delay 0 -clock clk [get_ports q*]
report_checks -path_delay max -digits 3 -format full
TCL
for t in rca8 counter8; do
  echo "################ $t ################"
  $STA "$OUT/$t.tcl" 2>&1 | tee "$OUT/$t.rpt"
done
echo; echo "Reports: $OUT/rca8.rpt  $OUT/counter8.rpt"
