#!/usr/bin/python3

import settings_analysis as s
import sys
sys.path.append(s.arith_path)
sys.path.append("../")
from os import walk
import os
from analysis_lib import printBasicRep,extractTotalArea,extractSlackTime,extractFileList,sortFileList,extractTruncLSBs,checkResult,message, basicAnalysis, printBasicAnalysisRes,extractRepType
from arithmetic import integerTo2sFileConverter


rep_file_list=extractFileList(s.rep_trunc_filter_path,s.rep_trunc_filter_ID)
sortFileList(rep_file_list)
rep_tuple_list=[]
for rep_file in rep_file_list:
    trunc_lsbs=int(extractTruncLSBs(rep_file))
    if trunc_lsbs!=0:
        rep_type=extractRepType(rep_file)
        if rep_type=="area":
            value=extractTotalArea(s.rep_trunc_filter_path+'/'+rep_file)
        if rep_type=="timing":
            value=extractSlackTime(s.rep_trunc_filter_path+'/'+rep_file)
        rep_tuple_list+=[(trunc_lsbs,rep_type,value)]
with open(s.log_rep_trunc_filter_fpath,"w") as log_pointer:
    for rep_tuple in rep_tuple_list:
        printBasicRep(log_pointer,rep_tuple)
