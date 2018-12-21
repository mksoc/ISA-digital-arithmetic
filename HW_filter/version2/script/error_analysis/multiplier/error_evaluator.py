import sys
import os
from itertools import zip_longest

sys.path.append('/home/clmcasino/Desktop/ISA/Lab2/ISA-digital-arithmetic/HW_filter/version2/script/py_model')

from arithmetic import mult_trunc_pp
from bin_lib    import twos_comp

FIN_NAME="../../py_model/common/samples.txt"
FOUT_NAME="common/pyresult{}.txt"
FLOG_NAME="log_error.txt"
NUM_SAMPLES=1000

def log_writer(log_file,truncating_number,avg_abs,avg_rel,max_abs,max_rel):
    log_file.write("Architecture with {} LSBs truncated.\n".format(truncating_number))
    log_file.write("Max absolute error:{:>15}| Max relative error:{:>12}\n".format(max_abs,max_rel))
    log_file.write("Avg absolute error:{:>15}| Avg relative error:{:>12}\n\n".format(round(avg_abs),avg_rel))

OUTPAR=47
i=0;
while i<OUTPAR-16:
    in_file=open(FIN_NAME,"r")
    out_file=open(FOUT_NAME.format(i),"w")

    for line in in_file:
        nums=line.split()
        out_file.write(mult_trunc_pp(nums[0],nums[1],OUTPAR,i))
    i+=1
in_file.close()
out_file.close()

i=0
log_file=open(FLOG_NAME,"w")
DIRECTORY=os.fsencode("common/")
for F_NAME in os.listdir(DIRECTORY):
    filename=F_NAME.decode("utf-8")
    if (".txt" in filename) and ("pyresult" in filename):
        result_file=open(FOUT_NAME.format(0),"r")
        approx_file=open("common/"+filename,"r")
        max_aerror=0
        max_rerror=0
        avg_asum=0
        avg_rsum=0
        j=0
        while j<NUM_SAMPLES:
            r_line=result_file.readline()
            e_line=approx_file.readline()
            r_num=twos_comp(int(r_line,2),len(r_line))
            e_num=twos_comp(int(e_line,2),len(e_line))

            abs_error=r_num-e_num
            rel_error=abs(abs_error)/r_num

            avg_asum=avg_asum+abs_error
            avg_rsum=avg_rsum+rel_error
            if abs(abs_error)>abs(max_aerror):
                max_aerror=abs_error
            if abs(rel_error)>abs(max_rerror):
                max_rerror=rel_error
            j+=1
        
        avg_abs=avg_asum/j
        avg_rel=avg_rsum/j
        #we want to extract the number of the architecture
        start=filename.find('t')+1
        end=filename.find('.',start)
        iteration=filename[start:end]
        log_writer(log_file,iteration,avg_abs,avg_rel,max_aerror,max_rerror)
    i+=1
    result_file.close()
    approx_file.close()
log_file.close()
