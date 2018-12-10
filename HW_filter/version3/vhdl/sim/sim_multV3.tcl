# compile source files
vcom -93 -work ./work ../src/filter_pkg.vhd
vcom -93 -work ./work ../version3/multV3_pkg.vhd
vcom -93 -work ./work ../version3/*.vhd

# compile testbench
vcom -93 -work ./work ../tb/*.vhd
vlog -work ./work ../tb/iir_filterTB.v

# load design
vsim work.iir_filterTB

# run simulation
run -all
