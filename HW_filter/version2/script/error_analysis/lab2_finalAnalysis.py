#!/usr/bin/python3

# This script should:
#       0) Test the results from truncated architecture multiplier.
#       1) Compute error statistics from truncated multiplierself.
#       2) Compute error statistics from filter with truncated multiplier.
#       3) Collect synthesis results from truncated multiplierself.
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
from arithmetic import mult_trunc_pp
from analysis_lib import stdBAnalysis,extractFileList,sortFileList

# 0) Test the results from truncated architecture multiplier.
res_file_list=extractFileList(res_trunc_mult_path,res_trunc_mult_ID)
sortFileList(res_file_list)
for res_file in res_file_list:
    trunc_lsbs=extractTruncLSBs(res_file)
