	
				# compile source files
				
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/multV3_pkg.vhd
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/src/reg.vhd
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/*.vhd 
				
				# compile testbench
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/tb/mbeDadda_mult_wRegsTB.vhd
				
				# load design
				vsim  work.mbeDadda_mult_wRegsTB
				
				# run simulation
				run 300us 