#!/bin/python3

FIN_NAME="common/samples.txt"
FOUT_NAME="common/pyresult_V2.txt"
DADDALEVELS=13

import sys

def pp_calculator(multiplicand, recode_bits):
    print(multiplicand)
    print(bin(recode_bits))
    if   recode_bits==int('000',2) or recode_bits==int('111',2):
        return(0)
    elif recode_bits==int('001',2) or recode_bits==int('010',2):
        return(multiplicand)
    elif recode_bits==int('101',2) or recode_bits==int('110',2):
        return(~multiplicand)
    elif recode_bits==int('011',2):
        return(2*multiplicand)
    else:
        return(2*(~multiplicand))
    
def inv_evaluator(recode_bits):
    if recode_bits==int('101',2) or recode_bits==int('110',2) or recode_bits==int('011',2):
        return(1) 
    else:
        return(0) 
    
in_file=open(FIN_NAME,"r")
out_file=open(FOUT_NAME,"w")

for line in in_file:
    
# Reading operands
    nums=line.split()
    multiplicand=int(nums[0],2)
    multiplier=int(nums[1],2)
    
# Initialize last
    pp=[]
    i=0
    highliter=3
    
# 1st pp calculation
    pp.append(int(pp_calculator(multiplicand,multiplier&highliter))<<1)
    invert = (inv_evaluator(multiplier&highliter))
    highliter=7<<1
    i+=1
    
# Calculating all the other product
    while i < DADDALEVELS:
        pp.append(pp_calculator(multiplicand,multiplier&highliter)<<(2*i)+invert)
        print(pp[i])
        invert = (inv_evaluator(multiplier&highliter))<<i
        highliter=highliter<<2
        i+=1
        if i == 5:
            exit(0)
# Truncating LSBs if requested
    if len(sys.argv)>1:
        big=bin(pp[DADDALEVELS-1])
        ones="1"*len(big)
        truncator=int(ones,2)<<int(sys.argv[1])
        i=0
        while i<DADDALEVELS:
            pp[i]=pp[i]&truncator
            i+=1

# Summing pp
    i=0
    product=0
    while i<DADDALEVELS:
        product=pp[i]+product
        i+=1
        
# Writing result
    out_file.write(bin(product)+'\n')
