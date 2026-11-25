# Magic: extract devices and connectivity (no parasitics) into
# verification/lvs/<cell>_layout.spice for netgen. Expects `cell` to be set.

set subvt_root /foss/designs/SUB-VT_STD_CELL_LIB
set cellu [string toupper $cell]
cd $subvt_root/cells/$cellu/layout
load $cell
extract all
ext2spice hierarchy on
# High thresholds drop all parasitic R and C; LVS only needs the devices.
ext2spice cthresh 1000000
ext2spice rthresh 1000000
ext2spice extresist off
ext2spice -o $subvt_root/cells/$cellu/verification/lvs/${cell}_layout.spice
