# compile source files
vcom -93 -work ./work ../src/multV3_pkg.vhd
vcom -93 -work ./work ../src/*.vhd

# compile testbench
vcom -93 -work ./work ../tb/*.vhd
# load design
vsim work.mbeDadda_mult_wRegsTB

# run simulation
run -all

quit -f
