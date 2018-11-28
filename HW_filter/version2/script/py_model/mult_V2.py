#!/bin/python3

FIN_NAME="sample.txt"
FOUT_NAME="pyresult.txt"
DADDALEVELS=13

def pp_calculator(multiplicand, recode_bits):
    if   recode_bits==int('000',2) or recode_bits==int('111',2):
        return(0)
    elif recode_bits==int('001',2) or recode_bits==int('010',2):
        return(multiplicand)
    elif recode_bits==int('101',2) or recode_bits==int('110',2):
        return(not(multiplicand))
    elif recode_bits==int('011',2):
        return(2*multiplicand)
    else:
        return(2*not(multiplicand))
def inv_evaluator(recode_bits):
    
    
in_file=open(FIN_NAME,"r")

while True:
# Reading operands
    line1=in_file.readline()
    line2=in_file.readline()
    multiplicand=int(line1[0:len(line1)-1])
    multiplier=int(line2[0:len(line2)-1])
# Initialize last
    pp=[]
    i=0
    highliter=3
# 1st pp calculation
    pp[i]=pp_calculator(multiplicand,(multiplier&highliter)<<1)
    inv=inv_evaluator((multiplier&highliter)<<1)<<i
    while i < DADDALEVELS:
        #continue
    
