#!/bin/python3

FIN_NAME="common/samples.txt"
FOUT_NAME="common/pyresult.txt"

in_file=open(FIN_NAME,"r")
out_file=open(FOUT_NAME,"w")

for line in in_file:
    nums=line.split()
    multiplicand=int(nums[0],2)
    multiplier=int(nums[1],2)
    product=multiplicand*multiplier
    out_file.write(bin(product)+'\n')
