from bin_lib import printer_2s,twos_comp

# recode_calculator(multiplier,i):
#
# DESCRIPTION
#    Computes recode bits according to the MBE method.
# INPUT
#    Needs as inputs:
#       multiplier as 2's complement number expressed as strings.
#       iterator (integer) expliciting to which partial products recode bits are referred to.
# OUTPUT
#    Returns the recoding bits expressed as a string.

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


# mult mult(op0,op1,outpar):
#
# DESCRIPTION
#    Computes regular muliplication.
# INPUT
#    Needs as inputs:
#       multiplicand
#       multiplier as 2's complement number expressed as strings
#       output parallelism as an integer
# OUTPUT
#    Returns the 2's complement result expressed as a string.

def mult(op0,op1,outpar):
    multiplicand=int(op0,2)
    multiplicand=twos_comp(multiplicand,len(op0))
    multiplier=int(op1,2)
    multiplier=twos_comp(multiplier,len(op1))
    product=multiplicand*multiplier
    return printer_2s(product,outpar)+'\n'

# mult_trunc_pp (multiplier,multiplicand)
# DESCRIPTION
#    Computes regular muliplication.
# INPUT
#    Needs as inputs:
#       multiplicand
#       multiplier as 2's complement number expressed as strings
#       output parallelism as an integer
#       number of LSBs to be truncated
# OUTPUT
#    Returns the 2's complement result expressed as a string.

def mult_trunc_pp (op0,op1,outpar,lsbs):
    if len(op0)!=len(op1):
        DADDALEVELS=int(input("How many DADDALEVELS should I set?\n"))
    else:
        DADDALEVELS=len(op0)/2 + 1
    multiplicand=int(op0,2)
    multiplicand=twos_comp(multiplicand,len(op0))
    multiplier=int(op1,2)
    multiplier=twos_comp(multiplier,len(op1))

    # Initialize pp matrix
    pp=[]
    i=0
    inv=0

    # Calculating partial products
    while i < DADDALEVELS-1:
        recode_ctr=recode_calculator(op1,i)
        pp.append((pp_calculator(multiplicand,recode_ctr)<<(2*i))+inv)
        inv=inv_evaluator(recode_ctr)<<(2*i)
        i+=1
    pp.append(inv)

    # Truncating LSBs if requested

    ending_str='0'*lsbs
    i=0
    while i<DADDALEVELS:
        original_str=printer_2s(pp[i],outpar)
        new_str=original_str[0:len(original_str)-lsbs]+ending_str
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
    return printer_2s(product,outpar)+'\n'

# computeTruncResult(infile,outfile,outpar,lsbs):
# DESCRIPTION
#    Produces a outfile with results from multiplication done with truncated pp (MBE)
# INPUT
#    Needs as inputs:
#       infile  :name/path file with couples of 2's complement numbers.
#       outfile :name/path of output file where result will be written as 2's complement numbers.
#       outpar  :output parallelism as an integer.
#       lsbs    :number of LSBs to be truncated.
# OUTPUT
#    No return
def computeTruncResult(infile,outfile,outpar,lsbs):
    with open(infile,"r") as fin_pointer, open(outfile,"w") as fout_pointer:
        for line in fin_pointer:
            nums=line.split()
            fout_pointer.write(mult_trunc_pp(nums[0],nums[1],outpar,lsbs))

def trunc2sNum(num_str,outpar):
    return(num_str[0:outpar])

def truncResults(infile,outfile,outpar):
    with open(infile,"r") as fin_pointer, open(outfile,"w") as fout_pointer:
        for line in fin_pointer:
            fout_pointer.write(trunc2sNum(line,outpar)+'\n')

def integerTo2sFileConverter(infile,outfile,outpar):
    with open(infile,"r") as fin_pointer, open(outfile,"w") as fout_pointer:
        for line in fin_pointer:
            fout_pointer.write(printer_2s(int(line),outpar)+'\n')
