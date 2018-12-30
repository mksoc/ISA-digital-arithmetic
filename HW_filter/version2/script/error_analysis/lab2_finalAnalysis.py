#!/usr/bin/python3

# This script should:
#       0) Test the results from truncated architecture multiplier.
#       1) Compute error statistics from truncated multiplierself.
#       2) Compute error statistics from filter with truncated multiplier.
#       3) Collect synthesis results from truncated multiplier.
#       4) Collect synthesis results from filter with truncated multiplier.
#       5) Compute error statistics from multiplier with approx compressors.
#       6) Compute error statistics from filter with multiplier with approx compressors.
#       7) Collect synthesis results from multiplier with approx compressors.
#       8) Collect synthesis results from filter with multiplier with approx compressors.

# Importing all functions I Needs
import settings_analysis as s
from os import walk
import os
import sys
sys.path.append(s.arith_path)
from arithmetic import computeTruncResult
from analysis_lib import basicAnalysis,extractFileList,sortFileList,message

# 0) Test the results from truncated architecture multiplier.
res_file_list=extractFileList(s.res_trunc_mult_path,s.res_trunc_mult_ID)
sortFileList(res_file_list)
for res_file in res_file_list:
    trunc_lsbs=extractTruncLSBs(res_file)
    computeTruncResult(s.input_sample_fname,s.sw_res_fname,s.max_out_par,trunc_lsbs)
    # I have to truncate results HERE (maybe)
    check=checkResult(s.res_trunc_mult_path+'/'+res_file,s.sw_res_fname)
    if check !=0:
        message("Result for multiplier with {} truncated bit are WRONG!".format(trunc_lsbs))
    else:
        message("Result for multiplier with {} truncated bit are OKAY!".format(trunc_lsbs))

# 1) Compute error statistics from truncated multiplier.
res_file_list=extractFileList(s.res_trunc_mult_path,s.res_trunc_mult_ID)
sortFileList(res_file_list)
with open(s.log_stat_trunc_mult_fpath,"w") as log_pointer:
    for res_file in res_file_list:
        trunc_lsbs=extractTruncLSBs(res_file)
        analysis_res=basicAnalysis(s.sw_mult_result_fpath,s.res_trunc_mult_path+'/'+res_file)
        printBasicAnalysisRes(log_pointer,analysis_res,trunc_lsbs)

# 2) Compute error statistics from filter with truncated multiplier.
res_file_list=extractFileList(s.res_trunc_filter_path,s.res_trunc_filter_ID)
sortFileList(res_file_list)
with open(s.log_stat_trunc_filter_fpath,"w") as log_pointer:
    for res_file in res_file_list:
        trunc_lsbs=extractTruncLSBs(res_file)
        analysis_res=basicAnalysis(s.sw_filter_result_fpath,s.res_trunc_filter_path+'/'+res_file)
        printBasicAnalysisRes(log_pointer,analysis_res,trunc_lsbs)

# 3) Collect synthesis results from truncated multiplier.
rep_file_list=extractFileList(s.rep_trunc_mult_path,s.rep_trunc_mult_ID)
sortFileList(rep_file_list)
rep_tuple_list=[]
for rep_file in rep_file_list:
    trunc_lsbs=extractTruncLSBs(rep_file)
    rep_type=extractRepType(rep_file)
    if rep_type=="area":
        value=extractTotalArea(s.rep_trunc_mult_path+'\'+rep_file)
    else:
        value=extractSlackTime(s.rep_trunc_mult_path+'\'+rep_file)
    rep_tuple_list+=[(trunc_lsbs,rep_type,value)]
#DEVO ORDINARE LE TOUPLES E POI STAMPARE A FILE
with open(s.log_rep_trunc_mult_fpath,"w") as log_pointer:
