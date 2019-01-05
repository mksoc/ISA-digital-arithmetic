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
from arithmetic import integerTo2sFileConverter,computeTruncResult, truncResults
from analysis_lib import printString,printBasicRep,extractApproxCompr,extractTotalArea,extractSlackTime,extractRepType,checkResult,extractTruncLSBs,basicAnalysis,extractFileList,sortFileList,message,printBasicAnalysisRes

# 0) Test the results from truncated architecture multiplier.
res_file_list=extractFileList(s.res_trunc_mult_path,s.res_trunc_mult_ID)
sortFileList(res_file_list)
for res_file in res_file_list:
    trunc_lsbs=int(extractTruncLSBs(res_file))
    if trunc_lsbs!=0:
        computeTruncResult(s.input_sample_fname,s.sw_res_fname,s.max_out_par,trunc_lsbs)
        truncResults(s.sw_res_fname,s.sw_res_fname+".truncated",s.mult_out_par)
        check=checkResult(s.res_trunc_mult_path+'/'+res_file,s.sw_res_fname+".truncated")
        if check !=0:
            message("Result for multiplier with {} truncated bit are WRONG! {} wrong result".format(trunc_lsbs,check))
        else:
            message("Result for multiplier with {} truncated bit are OKAY!".format(trunc_lsbs))
        os.remove(s.sw_res_fname)
        os.remove(s.sw_res_fname+".truncated")

# 1) Compute error statistics from truncated multiplier.
res_file_list=extractFileList(s.res_trunc_mult_path,s.res_trunc_mult_ID)
sortFileList(res_file_list)
with open(s.log_stat_trunc_mult_fpath,"w") as log_pointer, open(s.matlab_trunc_values,"w") as matlab_trunc_values_pointer, open(s.matlab_trunc_mult_statMax,"w") as matlab_mult_statMax_pointer, open(s.matlab_trunc_mult_statAvg,"w") as matlab_mult_statAvg_pointer:
    for res_file in res_file_list:
        trunc_lsbs=int(extractTruncLSBs(res_file))
        if trunc_lsbs!=0:
            analysis_res=basicAnalysis(s.sw_mult_result_fpath,s.res_trunc_mult_path+'/'+res_file,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,trunc_lsbs)
            printString(matlab_trunc_values_pointer,trunc_lsbs)
            printString(matlab_mult_statMax_pointer,analysis_res[0])
            printString(matlab_mult_statAvg_pointer,analysis_res[1])

integerTo2sFileConverter(s.sw_filter_result_fpath,s.sw_filter_result_fpath2s,s.filter_out_par)
HW_temp_2sresult="HW_2sresult.temp"

# 2) Compute error statistics from filter with truncated multiplier.
res_file_list=extractFileList(s.res_trunc_filter_path,s.res_trunc_filter_ID)
sortFileList(res_file_list)
with open(s.log_stat_trunc_filter_fpath,"w") as log_pointer, open(s.matlab_trunc_filter_statMax,"w") as matlab_filter_statMax_pointer, open(s.matlab_trunc_filter_statAvg,"w") as matlab_filter_statAvg_pointer:
    for res_file in res_file_list:
        trunc_lsbs=int(extractTruncLSBs(res_file))
        if trunc_lsbs!=0:
            integerTo2sFileConverter(s.res_trunc_filter_path+'/'+res_file,HW_temp_2sresult,s.filter_out_par)
            analysis_res=basicAnalysis(s.sw_filter_result_fpath2s,HW_temp_2sresult,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,trunc_lsbs)
            printString(matlab_filter_statMax_pointer,analysis_res[0])
            printString(matlab_filter_statAvg_pointer,analysis_res[1])
            os.remove(HW_temp_2sresult)

# 3) Collect synthesis results from truncated multiplier.
rep_file_list=extractFileList(s.rep_trunc_mult_path,s.rep_trunc_mult_ID)
sortFileList(rep_file_list)
rep_tuple_list=[]
for rep_file in rep_file_list:
    trunc_lsbs=int(extractTruncLSBs(rep_file))
    if trunc_lsbs!=0:
        rep_type=extractRepType(rep_file)
        if rep_type=="area":
            value=extractTotalArea(s.rep_trunc_mult_path+'/'+rep_file)
        if rep_type=="timing":
            value=extractSlackTime(s.rep_trunc_mult_path+'/'+rep_file)
        rep_tuple_list+=[(trunc_lsbs,rep_type,value)]
with open(s.log_rep_trunc_mult_fpath,"w") as log_pointer, open(s.matlab_trunc_mult_areas,"w")  as matlab_trunc_mult_areas_pointer, open(s.matlab_trunc_mult_timing,"w") as matlab_trunc_mult_timing_pointer:
    for rep_tuple in rep_tuple_list:
        printBasicRep(log_pointer,rep_tuple)
        if rep_tuple[1]=="area":
            printString(matlab_trunc_mult_areas_pointer,rep_tuple[2])
        if rep_tuple[1]=="timing":
            printString(matlab_trunc_mult_timing_pointer,rep_tuple[2])

# 4) Collect synthesis results from filter with truncated multiplier.
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
with open(s.log_rep_trunc_filter_fpath,"w") as log_pointer, open(s.matlab_trunc_filter_areas,"w")  as matlab_trunc_filter_areas_pointer, open(s.matlab_trunc_filter_timing,"w") as matlab_trunc_filter_timing_pointer:
    for rep_tuple in rep_tuple_list:
        printBasicRep(log_pointer,rep_tuple)
        if rep_tuple[1]=="area":
            printString(matlab_trunc_filter_areas_pointer,rep_tuple[2])
        if rep_tuple[1]=="timing":
            printString(matlab_trunc_filter_timing_pointer,rep_tuple[2])

# 5) Compute error statistics from multiplier with approx compressors.
res_file_list=extractFileList(s.res_approxCompr_mult_path,s.res_approxCompr_mult_ID)
sortFileList(res_file_list)
with open(s.log_stat_approxCompr_mult_fpath,"w") as log_pointer, open(s.matlab_approxCompr_values,"w") as matlab_approxCompr_values_pointer, open(s.matlab_approxCompr_mult_statMax,"w") as matlab_mult_statMax_pointer, open(s.matlab_approxCompr_mult_statAvg,"w") as matlab_mult_statAvg_pointer:
    for res_file in res_file_list:
        compr_level=int(extractApproxCompr(res_file))
        if compr_level!=0:
            analysis_res=basicAnalysis(s.sw_mult_result_fpath,s.res_approxCompr_mult_path+'/'+res_file,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,compr_level)
            printString(matlab_approxCompr_values_pointer,compr_level)
            printString(matlab_mult_statMax_pointer,analysis_res[0])
            printString(matlab_mult_statAvg_pointer,analysis_res[1])

# 6) Compute error statistics from filter with multiplier with approx compressors.
res_file_list=extractFileList(s.res_approxCompr_filter_path,s.res_approxCompr_filter_ID)
sortFileList(res_file_list)
with open(s.log_stat_approxCompr_filter_fpath,"w") as log_pointer, open(s.matlab_approxCompr_filter_statMax,"w") as matlab_filter_statMax_pointer, open(s.matlab_approxCompr_filter_statAvg,"w") as matlab_filter_statAvg_pointer:
    for res_file in res_file_list:
        compr_level=int(extractApproxCompr(res_file))
        if compr_level!=0:
            integerTo2sFileConverter(s.res_approxCompr_filter_path+'/'+res_file,HW_temp_2sresult,s.filter_out_par)
            analysis_res=basicAnalysis(s.sw_filter_result_fpath2s,HW_temp_2sresult,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,compr_level)
            printString(matlab_filter_statMax_pointer,analysis_res[0])
            printString(matlab_filter_statAvg_pointer,analysis_res[1])
            os.remove(HW_temp_2sresult)

# 7) Collect synthesis results from multiplier with approx compressors.
rep_file_list=extractFileList(s.rep_approxCompr_mult_path,s.rep_approxCompr_mult_ID)
sortFileList(rep_file_list)
rep_tuple_list=[]
for rep_file in rep_file_list:
    compr_level=int(extractApproxCompr(rep_file))
    if compr_level!=0:
        rep_type=extractRepType(rep_file)
        if rep_type=="area":
            value=extractTotalArea(s.rep_approxCompr_mult_path+'/'+rep_file)
        if rep_type=="timing":
            value=extractSlackTime(s.rep_approxCompr_mult_path+'/'+rep_file)
        rep_tuple_list+=[(compr_level,rep_type,value)]
with open(s.log_rep_approxCompr_mult_fpath,"w") as log_pointer, open(s.matlab_approxCompr_mult_areas,"w")  as matlab_approxCompr_mult_areas_pointer, open(s.matlab_approxCompr_mult_timing,"w") as matlab_approxCompr_mult_timing_pointer:
    for rep_tuple in rep_tuple_list:
        printBasicRep(log_pointer,rep_tuple)
        if rep_tuple[1]=="area":
            printString(matlab_approxCompr_mult_areas_pointer,rep_tuple[2])
        if rep_tuple[1]=="timing":
            printString(matlab_approxCompr_mult_timing_pointer,rep_tuple[2])

# 8) Collect synthesis results from filter with multiplier with approx compressors.
rep_file_list=extractFileList(s.rep_approxCompr_filter_path,s.rep_approxCompr_filter_ID)
sortFileList(rep_file_list)
rep_tuple_list=[]
for rep_file in rep_file_list:
    compr_level=int(extractApproxCompr(rep_file))
    if compr_level!=0:
        rep_type=extractRepType(rep_file)
        if rep_type=="area":
            value=extractTotalArea(s.rep_approxCompr_filter_path+'/'+rep_file)
        if rep_type=="timing":
            value=extractSlackTime(s.rep_approxCompr_filter_path+'/'+rep_file)
        rep_tuple_list+=[(compr_level,rep_type,value)]
with open(s.log_rep_approxCompr_filter_fpath,"w") as log_pointer, open(s.matlab_approxCompr_filter_areas,"w")  as matlab_approxCompr_filter_areas_pointer, open(s.matlab_approxCompr_filter_timing,"w") as matlab_approxCompr_filter_timing_pointer:
    for rep_tuple in rep_tuple_list:
        printBasicRep(log_pointer,rep_tuple)
        if rep_tuple[1]=="area":
            printString(matlab_approxCompr_filter_areas_pointer,rep_tuple[2])
        if rep_tuple[1]=="timing":
            printString(matlab_approxCompr_filter_timing_pointer,rep_tuple[2])
