
				# there will be a compile ultra command later
				set_ultra_optimization True
analyze -f vhdl -lib WORK /home/isa22/lab2/src/filter_pkg.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/multV3_pkg.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/src/reg.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/src/iir_filterCU.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/src/iir_filter.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/src/iir_filterDP.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/approx_comp_4to2.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/halfAdder.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/mbeDadda_mult_wRegs.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/fullAdder.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/mbeDadda_mult.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/mux2.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/r4mbePP_preprocessing.vhd
analyze -f vhdl -lib WORK /home/isa22/lab2/version3/bitwiseInv.vhd
				# preserve RTL names
				set power_preserve_rtl_hier_names true

				# elaborate design
				elaborate iir_filter -arch structure -lib WORK > ./logs/elaborate-log.txt
				uniquify
				link

				# create symbolic clock signal
				create_clock -name CLOCK -period 0 clk
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

				# start synthesis
				compile_ultra

				# apply retiming to design
				 
				set_dont_touch *reg_in*
				set_dont_touch *reg_coeff_fb_i_*
				set_dont_touch *reg_b_i_*
				set_dont_touch *reg_out*
				optimize_registers

				# reports gen
				report_timing > /home/isa22/lab2/common/iir_filter_timing.txt
				report_area > /home/isa22/lab2/common/iir_filter_area.txt
				change_names -hierarchy -rules verilog
				write_sdf /home/isa22/lab2/syn/netlist/iir_filter.sdf
				write -f verilog -hierarchy -output /home/isa22/lab2/syn/netlist/iir_filter.v
				write_sdc /home/isa22/lab2/syn/netlist/iir_filter.sdc
				quit