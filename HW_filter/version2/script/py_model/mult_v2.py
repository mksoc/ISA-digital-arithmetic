#!/bin/python3

FIN_NAME="common/samples.txt"
FOUT_NAME="common/pyresult_v2"

DADDALEVELS=13
OUTPAR=47

import sys
from bin_lib import twos_comp, printer_2s

def recode_calculator(multiplier,i):
    if i==0:
        return (multiplier[len(multiplier)-2:len(multiplier)]+'0')
    else:
        return (multiplier[len(multiplier)-(2*i+2):len(multiplier)-(2*i-1)])

def pp_calculator(multiplicand, recode):
    if   recode=='000' or recode=='111':
        return(0)
    elif recode=='001' or recode=='010':
        return(multiplicand)
    elif recode=='101' or recode=='110':
        return(~multiplicand)
    elif recode=='011':
        return(multiplicand<<1)
    else:
        return(~(multiplicand<<1))

def inv_evaluator(recode):
    if recode=='101' or recode=='110' or recode=='100':
        return(1) 
    else:
        return(0) 
        

in_file=open(FIN_NAME,"r")
if len(sys.argv)>1:
    out_file=open(FOUT_NAME+"_a"+sys.argv[1]+".txt","w")
else:
    out_file=open(FOUT_NAME+".txt","w")
for line in in_file:
    
# Reading operands
    nums=line.split()
    multiplicand=int(nums[0],2)
    multiplicand=twos_comp(multiplicand,len(nums[0]))
    multiplier=int(nums[1],2)
    multiplier=twos_comp(multiplier,len(nums[1]))
    
# Initialize pp matrix
    pp=[]
    i=0
    inv=0
    
# Calculating partial products
    while i < DADDALEVELS-1:
        recode_ctr=recode_calculator(nums[1],i)
        pp.append((pp_calculator(multiplicand,recode_ctr)<<(2*i))+inv)  
        inv=inv_evaluator(recode_ctr)<<(2*i)
        i+=1        
    pp.append(inv)
    
# Truncating LSBs if requested
    if len(sys.argv)>1:
        APPROX=int(sys.argv[1])
        ending_str='0'*APPROX
        i=0
        while i<DADDALEVELS:
            original_str=printer_2s(pp[i],OUTPAR)
            new_str=original_str[0:len(original_str)-APPROX]+ending_str
            new_num=int(new_str,2)
            pp[i]=twos_comp(new_num,len(new_str))
            i+=1           
# Summing pp
    i=0
    product=0
    while i<DADDALEVELS:
        product=pp[i]+product
        i+=1

# Writing result
    out_file.write(printer_2s(product,OUTPAR)+'\n')

    
