# =================================================================
# *****************************************************************
# *************** GENERATED USING sim_script_gen.py ***************
# ************           2018-11-12 10:06:17           ************
# *****************************************************************
# The script was generated starting from these values of variables:
# run_remote = 1
# cli_mode = 1
# version = 0
# design = 2
# =================================================================

puts "Running in command line mode. No waveforms will be available."

# compile source files
vcom -93 -work ./work ../src/filter_pkg.vhd
vlog -work ./work ../version0/*.v

# compile testbench
vcom -93 -work ./work ../tb/*.vhd
vlog -work ./work +define+SYN=1+NO_GUI=1 ../tb/iir_filterTB.v

# load design
vsim -L /software/dk/nangate45/verilog/msim6.2g -sdftyp /iir_filterTB/UUT=../version0/iir_filter.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so   work.iir_filterTB

# run simulation
run -all