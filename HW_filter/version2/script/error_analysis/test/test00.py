#!/usr/bin/python3

import settings_analysis as s
import sys
sys.path.append(s.arith_path)
sys.path.append("../")
from os import walk
import os
from analysis_lib import extractFileList,sortFileList,extractTruncLSBs,checkResult,message
from arithmetic import computeTruncResult,truncResults


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
