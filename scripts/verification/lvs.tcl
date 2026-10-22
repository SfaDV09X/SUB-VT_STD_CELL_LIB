# extract
set subvt_root /foss/designs/SUB-VT_STD_CELL_LIB
set cellu [string toupper $cell]
cd $subvt_root/cells/$cellu/layout
load $cell
extract all
ext2spice hierarchy on
ext2spice cthresh 1000000
ext2spice rthresh 1000000
ext2spice extresist off
ext2spice -o $subvt_root/cells/$cellu/verification/lvs/${cell}_layout.spice