	
				# compile source files
				
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/src/filter_pkg.vhd
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/multV3_pkg.vhd
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/src/*.vhd
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/*.vhd 
				
				# compile testbench
					
			vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/tb/*.vhd
			vlog -work /home/isa22/lab2/sim/work /home/isa22/lab2/tb/iir_filterTB.v 
				
				# load design
				vsim  work.iir_filterTB
				
				# run simulation
				run -all 