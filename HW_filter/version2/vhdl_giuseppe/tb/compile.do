vlib work

vcom ../multV2_pkg.vhd
vcom ../*.vhd
vcom tb.vhd

vsim -c work.mult_tb


#add list -decimal clk -notrigger a b c cout sum
#add wave sim:/mult_tb/UUT/*
run 1ms
quit -f
#write list counter.lst

