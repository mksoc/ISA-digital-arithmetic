#!/usr/bin/python3

import sys
sys.path.append('/home/clmcasino/Desktop/ISA/Lab2/ISA-digital-arithmetic/HW_filter/version2/script/py_model')
from res_analysis import extractTotalArea, extractSlackTime

with open("area-report.txt","r") as area_file:
    print(extractTotalArea(area_file))
with open("timing-report-fmax.txt","r") as timing_file1:
    print(extractSlackTime(timing_file1))
with open("timing-report.txt","r") as timing_file2:
    print(extractSlackTime(timing_file2))
