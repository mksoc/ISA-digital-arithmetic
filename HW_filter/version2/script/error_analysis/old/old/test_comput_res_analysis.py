#!/usr/bin/python3
import sys
from os import walk
import os

analysis_lib_path='/home/clmcasino/Desktop/ISA/Lab2/ISA-digital-arithmetic/HW_filter/version2/script/error_analysis'
sys.path.append(analysis_lib_path)

from analysis_lib import arithRelDiff,maxValue,avgValue
RES_DIR="multiplier/common"

def log_writer(log_file,truncating_number,avg_rel,max_rel):
    log_file.write("Architecture with {} LSBs truncated.\n".format(truncating_number))
    log_file.write("Max relative error: {:>12}\n".format(max_rel))
    log_file.write("Avg relative error: {:>12}\n\n".format(avg_rel))


filelist = []
for (dirpath, dirnames, filenames) in walk(RES_DIR):
    filelist.extend(filenames)
    break
filelist.sort()
filelist.sort(key=len)

try:
    os.mkdir('tempDir')
except:
    print("tempDir already exists")

OUTFILE="tempDir/diff{}.txt"
exactRes=RES_DIR+"/"+filelist[0]
for i in range(1,len(filelist)):
    appRes=RES_DIR+"/"+filelist[i]
    outRes=OUTFILE.format(i)
    arithRelDiff(exactRes,appRes,outRes,1000)

difflist = []
for (dirpath, dirnames, filenames) in walk('tempDir'):
    difflist.extend(filenames)
    break
difflist.sort()
difflist.sort(key=len)

LOGFILE="log.txt"
with open(LOGFILE,"w") as  log_pointer:
    i=1
    for fname in difflist:
        diff_path="tempDir/"+fname
        log_writer(log_pointer,i,avgValue(diff_path),maxValue(diff_path))
        i+=1
