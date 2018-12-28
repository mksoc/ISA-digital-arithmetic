#!/usr/bin/python3
from arithmetic import mult_trunc_pp

INFILE="common/samples.txt"
OUTFILE="common/pyresult_v2_a6.txt"
OUTFILE="common/pyresult_v3_a6.txt"

with open(INFILE,"r") as fin_pointer, open(OUTFILE,"w") as fout_pointer:
    for line in fin_pointer:
        nums=line.split()
        fout_pointer.write(mult_trunc_pp(nums[0],nums[1],47,6))
with open(INFILE,"r") as fin_pointer, open(OUTFILE,"w") as fout_pointer:
    for line in fin_pointer:
        nums=line.split()
        fout_pointer.write(mult_trunc_pp(nums[1],nums[0],47,6))
