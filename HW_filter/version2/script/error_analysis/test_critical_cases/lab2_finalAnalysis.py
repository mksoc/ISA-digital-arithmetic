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
sys.path.append("../")
from arithmetic import integerTo2sFileConverter,computeTruncResult, truncResults
from analysis_lib import printBasicRep,extractApproxCompr,extractTotalArea,extractSlackTime,extractRepType,checkResult,extractTruncLSBs,basicAnalysis,extractFileList,sortFileList,message,printBasicAnalysisRes

HW_temp_2sresult="HW_2sresult.temp"

# 5) Compute error statistics from multiplier with approx compressors.
res_file_list=extractFileList(s.res_approxCompr_mult_path,s.res_approxCompr_mult_ID)
sortFileList(res_file_list)
with open(s.log_stat_approxCompr_mult_fpath,"w") as log_pointer:
    for res_file in res_file_list:
        compr_level=int(extractApproxCompr(res_file))
        if compr_level!=0:
            analysis_res=basicAnalysis(s.sw_mult_result_fpath,s.res_approxCompr_mult_path+'/'+res_file,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,compr_level)
os.rename("tempFile","tempFile1")

# 6) Compute error statistics from filter with multiplier with approx compressors.
res_file_list=extractFileList(s.res_approxCompr_filter_path,s.res_approxCompr_filter_ID)
sortFileList(res_file_list)
with open(s.log_stat_approxCompr_filter_fpath,"w") as log_pointer:
    for res_file in res_file_list:
        compr_level=int(extractApproxCompr(res_file))
        if compr_level!=0:
            integerTo2sFileConverter(s.res_approxCompr_filter_path+'/'+res_file,HW_temp_2sresult,s.filter_out_par)
            analysis_res=basicAnalysis(s.sw_filter_result_fpath2s,HW_temp_2sresult,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,compr_level)
            os.remove(HW_temp_2sresult)
