	
				# compile source files
				
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/multV3_pkg.vhd
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/src/reg.vhd
				vlog -work /home/isa22/lab2/sim/work /home/isa22/lab2/version3/*.v 
				
				# compile testbench
				vcom -93 -work /home/isa22/lab2/sim/work /home/isa22/lab2/tb/mbeDadda_mult_wRegsTB.vhd
				
				# load design
				vsim -L /software/dk/nangate45/verilog/msim6.2g -sdftyp /mbeDadda_mult_wRegsTB/UUT=/home/isa22/lab2/version3/mbeDadda_mult_wRegs.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so work.mbeDadda_mult_wRegsTB
				
				# run simulation
				run 300us 