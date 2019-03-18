	
				# compile source files
				
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/src/filter_pkg.vhd
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/multV3_pkg.vhd
				vlog -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/*.v 
				
				# compile testbench
					
			vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/tb/*.vhd
			vlog -work /home/isa22/lab2/sim/work /home/isa22/lab2/tb/iir_filterTB.v 
				
				# load design
				vsim -L /software/dk/nangate45/verilog/msim6.2g -sdftyp /iir_filterTB/UUT=/home/isa22/lab2/version3/iir_filter.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so work.iir_filterTB
				
				# run simulation
				run -all 