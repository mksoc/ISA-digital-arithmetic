#!/bin/python3

FIN_NAME="common/samples.txt"
FOUT_NAME="common/pyresult_V2.txt"
DADDALEVELS=13

import sys

def twos_comp(value, bits):
    if (value & (1<<(bits-1))) != 0:
        value=value - (1<<bits)
    return value

def pp_calculator(multiplicand, recode_bits,i):
    recode_str=format(recode_bits,'b')
    _recode=recode_str[0:3]
    if len(_recode)==1:
        recode="00"+_recode
    elif len(_recode)==2:
        recode="0"+_recode
    else:
        recode=_recode
    
    print("RECODE:\n"+recode)
    if   recode=='000' or recode=='111':
        return(0)
    elif recode=='001' or recode=='010':
        return(multiplicand)
    elif recode=='101' or recode=='110':
        return(~multiplicand)
    elif recode=='011':
        return(2*multiplicand)
    else:
        return(2*(~multiplicand))
    
def inv_evaluator(recode_bits):
    recode_str=format(recode_bits,'b')
    _recode=recode_str[0:3]
    if len(_recode)==1:
        recode="00"+_recode
    elif len(_recode)==2:
        recode="0"+_recode
    else:
        recode=_recode
        
    if recode==int('101',2) or recode==int('110',2) or recode==int('011',2):
        return(1) 
    else:
        return(0) 
    
in_file=open(FIN_NAME,"r")
out_file=open(FOUT_NAME,"w")

for line in in_file:
    
# Reading operands
    nums=line.split()
    multiplicand=int(nums[0],2)
    multiplicand=twos_comp(multiplicand,len(nums[0]))
    multiplier=int(nums[1],2)
    multiplier=twos_comp(multiplier,len(nums[1]))
    print(format(multiplier,'b'))
# Initialize pp
    pp=[]
    i=0
    highliter=3
    
# 1st pp calculation
    pp.append(pp_calculator(multiplicand,(multiplier&highliter)<<1))
    invert = (inv_evaluator((multiplier&highliter)<<1))
    print("1stRE:\n"+format((multiplier&highliter)<<1,'b'))
    highliter=7<<1
    i+=1
    
# Calculating all the other product
    while i < DADDALEVELS:
        pp.append(pp_calculator(multiplicand,multiplier&highliter)<<(2*i)+invert)
        invert = (inv_evaluator(multiplier&highliter))<<i
        print("actualRE:\n"+format(multiplier&highliter,'b'))
        highliter=highliter<<2
        i+=1
        if i==12:
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
