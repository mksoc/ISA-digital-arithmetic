# delete work if it already exists 
if {[file exists work]} {
	vdel -lib work -all
}

# create a rtl_work library
vlib work

# map "work" name to work" folder
vmap work work

# compile src files
vcom -93 -work ./work ../src/multV1_pkg.vhd
vcom -93 -work ./work ../src/*.vhd

# compile tb files
vcom -93 -work ./work ../tb/*.vhd

# set parameters for simulation
#

# simulate
vsim work.mbeDadda_mult_tb

# run the simulation
run -all
