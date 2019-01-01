#!/usr/bin/python3

import settings_analysis as s
import sys
sys.path.append("../")
from os import walk
import os
from analysis_lib import extractApproxCompr,extractFileList,sortFileList,extractTruncLSBs,checkResult,message, basicAnalysis, printBasicAnalysisRes

res_file_list=extractFileList(s.res_approxCompr_mult_path,s.res_approxCompr_mult_ID)
sortFileList(res_file_list)
with open(s.log_stat_approxCompr_mult_fpath,"w") as log_pointer:
    for res_file in res_file_list:
        trunc_lsbs=int(extractApproxCompr(res_file))
        if trunc_lsbs!=0:
            analysis_res=basicAnalysis(s.sw_mult_result_fpath,s.res_approxCompr_mult_path+'/'+res_file,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,trunc_lsbs)
