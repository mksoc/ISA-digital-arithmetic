cd /home/isa22/lab2/syn
		source /software/scripts/init_synopsys
		mkdir work logs reports saif netlist
		dc_shell-xg-t -f synth-filter.tcl
		mv netlist/* ../version3
		mv saif/NangateOpenCellLibrary.saif ../sim