#!/usr/bin/python3

import settings_analysis as s
import sys
sys.path.append(s.arith_path)
sys.path.append("../")
from os import walk
import os
from analysis_lib import extractFileList,sortFileList,extractTruncLSBs,checkResult,message, basicAnalysis, printBasicAnalysisRes
from arithmetic import integerTo2sFileConverter

integerTo2sFileConverter(s.sw_filter_result_fpath,s.sw_filter_result_fpath2s,s.filter_out_par)
HW_temp_2sresult="HW_2sresult.temp"
res_file_list=extractFileList(s.res_trunc_filter_path,s.res_trunc_filter_ID)
sortFileList(res_file_list)
with open(s.log_stat_trunc_filter_fpath,"w") as log_pointer:
    for res_file in res_file_list:
        trunc_lsbs=int(extractTruncLSBs(res_file))
        if trunc_lsbs!=0:
            integerTo2sFileConverter(s.res_trunc_filter_path+'/'+res_file,HW_temp_2sresult,s.filter_out_par)
            analysis_res=basicAnalysis(s.sw_filter_result_fpath2s,HW_temp_2sresult,s.numSamples)
            printBasicAnalysisRes(log_pointer,analysis_res,trunc_lsbs)
            os.remove(HW_temp_2sresult)
