# =================================================================
# *****************************************************************
# *************** GENERATED USING syn_script_gen.py ***************
# ************           2018-11-12 15:28:16           ************
# *****************************************************************
# The script was generated starting from these values of variables:
# version = 0
# clock period = 5.8
# compile command = 1
# =================================================================

# compile source files
analyze -f vhdl -lib WORK ../src/filter_pkg.vhd
analyze -f vhdl -lib WORK ../src/iir_filterCU.vhd
analyze -f vhdl -lib WORK ../src/reg.vhd
analyze -f vhdl -lib WORK ../version0/iir_filterDP.vhd
analyze -f vhdl -lib WORK ../version0/iir_filter.vhd

# preserve RTL names
set power_preserve_rtl_hier_names true

# elaborate design
elaborate iir_filter -arch structure -lib WORK > ./logs/elaborate-log.txt
uniquify
link

# create symbolic clock signal
create_clock -name CLOCK -period 5.8 clk
set_dont_touch_network CLOCK
set_clock_uncertainty 0.07 [get_clocks CLOCK]

# set input/output delays
set_input_delay 0.5 -max -clock CLOCK [remove_from_collection [all_inputs] CLOCK]
set_output_delay 0.5 -max -clock CLOCK [all_outputs]

# set output load capacitance
set OLOAD [load_of NangateOpenCellLibrary/BUF_X4/A]
set $OLOAD [all_outputs]

# flatten hierarchy
ungroup -all -flatten

# set implementations
set_implementation DW01_add/pparch [find cell *add_*]
set_implementation DW01_sub/pparch [find cell *sub_*]
set_implementation DW02_mult/pparch [find cell *mult_*]

# start synthesis
compile > ./logs/compile-log.txt

# save results
report_resources > ./reports/resources-report.txt
report_timing > ./reports/timing-report.txt
report_area > ./reports/area-report.txt

# setup Verilog name rules
change_names -hierarchy -rules verilog

# export netlist delay file
write_sdf ./netlist/iir_filter.sdf

# export netlist file
write -f verilog -hierarchy -output ./netlist/iir_filter.v

# export Synopsys Design Constraints file
write_sdc ./netlist/iir_filter.sdc

# convert lib into .saif for modelsim
read_file NangateOpenCellLibrary_typical_ecsm_nowlm.db
lib2saif -out ./saif/NangateOpenCellLibrary.saif NangateOpenCellLibrary

quit