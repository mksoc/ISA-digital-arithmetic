#!/bin/python3

FIN_NAME="common/samples.txt"
FOUT_NAME="common/pyresult.txt"

OUTPAR=47

in_file=open(FIN_NAME,"r")
out_file=open(FOUT_NAME,"w")

from bin_lib import twos_comp, printer_2s

for line in in_file:
    nums=line.split()
    multiplicand=int(nums[0],2)
    multiplicand=twos_comp(multiplicand,len(nums[0]))
    multiplier=int(nums[1],2)
    multiplier=twos_comp(multiplier,len(nums[1]))
    product=multiplicand*multiplier
    out_file.write(printer_2s(product,OUTPAR)+'\n')
