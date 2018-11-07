# =================================================================
# *****************************************************************
# ************ GENERATED USING sim_script_generator.py ************
# ************           2018-11-06 23:23:56           ************
# *****************************************************************
# =================================================================


puts "Running in command line mode. No waveforms will be available."

# compile source files
vcom -93 -work ./work ../src/filter_pkg.vhd
vcom -93 -work ./work "../version3/*.v"

# compile testbench
vcom -93 -work ./work ../tb/*.vhd
vlog -work ./work +define+SYN=1+NO_GUI=1 ../tb/iir_filterTB.v

# load design
vsim -L /software/dk/nangate45/verilog/msim6.2g -sdftyp /iir_filterTB/UUT=../netlist/iir_filter.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so work.iir_filterTB