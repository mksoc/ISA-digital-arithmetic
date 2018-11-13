# =================================================================
# *****************************************************************
# *************** GENERATED USING sim_script_gen.py ***************
# ************           2018-11-13 13:11:25           ************
# *****************************************************************
# The script was generated starting from these values of variables:
# run_remote = 1
# cli_mode = 1
# version = 0
# design = 1
# =================================================================

puts "Running in command line mode. No waveforms will be available."

# compile source files
vcom -93 -work ./work ../src/*.vhd
vcom -93 -work ./work ../version0/*.vhd

# compile testbench
vcom -93 -work ./work ../tb/*.vhd
vlog -work ./work +define+NO_GUI=1 ../tb/iir_filterTB.v

# load design
vsim    work.iir_filterTB

# run simulation
run -all