import sys
import os
bin_lib_path='/home/clmcasino/Desktop/ISA/Lab2/ISA-digital-arithmetic/HW_filter/version2/script/py_model'
sys.path.append(bin_lib_path)
from bin_lib import twos_comp

# extractTotalArea(area_rep_file):
#
# DESCRIPTION
#    Returns TOTAL CELL AREA out of a synopsys area report.
# INPUT
#    Needs as inputs:
#       pointer to the area report file
# OUTPUT
#    Returns area as integer
def extractTotalArea(area_rep_file):
    with open(area_rep_file,"r") as rep_pointer:
        for line in rep_pointer:
            if "Total cell area:" in line:
                strings=line.split()
                return float(strings[3])
        print ("Total cell area not found. Please check if {} is a Synopsys area report file.".format(area_rep_file.name))
        exit (1)

# extractSlackTime(timing_rep_file):
#
# DESCRIPTION
#    Returns SLACK TIME out of a synopsys timing report.
# INPUT
#    Needs as inputs:
#       pointer to the timing report file
# OUTPUT
#    Returns slack time as integer
def extractSlackTime(timing_rep_file):
    with open(timing_rep_file,"r") as rep_pointer
        for line in rep_pointer:
            if "slack" in line:
                strings=line.split()
                return float(strings[2])
            print ("Slack time not found. Please check if {} is a Synopsys timing report file.".format(timing_rep_file.name))
        exit (1)

# arithRelDiff(infile1,infile2,outfile):
#
# DESCRIPTION
#    Computes the arithmetic distance between the data (expressed as 2's compl string) into two different input file.
#    Computation is done line by line. Eg outfile.line(n)=infile1.line(n)-infile2.line(n)
# INPUT
#    Needs as inputs:
#       infile1,infile2: name or path (rel. or abs.) of two input files to be differed.
#       outfile:         name or path (rel. or abs.) of output file
#       num_line:        for how many lines we have to compute the distance
#    NOTE1: infile1 is used as reference in order to comput relative distance
# OUTPUT
#    No returns.
def arithRelDiff(infile1,infile2,outfile,num_line):
    with open(infile1,"r") as fin1_pointer, open(infile2,"r") as fin2_pointer, open(outfile, "w") as fout_pointer:
        for i in range(0,num_line):
            line1=fin1_pointer.readline()
            line2=fin2_pointer.readline()
            num1=twos_comp(int(line1,2),len(line1))
            num2=twos_comp(int(line2,2),len(line2))
            abs_dist=num1-num2
            rel_dist=abs_dist/num1
            fout_pointer.write(str(rel_dist)+'\n')

# maxValue(infile):
#
# DESCRIPTION
#    Computes the max value of a list of numers in a file.
# INPUT
#    Needs as inputs:
#       infile: name or path (rel. or abs.) of the input file to be checked.
# OUTPUT
#    Returns max value.
def maxValue(infile):
    with open(infile,"r") as fin_pointer:
        max=0;
        for line in fin_pointer:
            num=float(line[0:len(line)-1])
            if abs(num)>abs(max):
                max=num
        return (max)

# avgValue(infile):
#
# DESCRIPTION
#    Computes the average value of a list of numbers ina file.
# INPUT
#    Needs as inputs:
#       infile: name or path (rel. or abs.) of the input file to be checked.
# OUTPUT
#    Returns average value.
def avgValue(infile):
    with open(infile,"r") as fin_pointer:
        sum=0
        j=0
        for line in fin_pointer:
            sum+=float(line[0:len(line)-1])
            j+=1
        avg=sum/j
        return (avg)

# basicAnalysis(ref_file,comp_file):
#
# DESCRIPTION
#    Computes the maximum and the average relative distance between the data contained into two files
# INPUT
#    Needs as inputs:
#       ref_file: name or path (rel. or abs.) of the reference file, whose data are used as reference for relative distance.
#       comp_file: name or path (rel. or abs.) of the file to be compered.
# OUTPUT
#    Returns list containing at pos zero the max value and at pos 1 the avg value.
def basicAnalysis(ref_file,comp_file):
    result=[]
    temp_file_path="tempFile"
    arithRelDiff(ref_file,comp_file,temp_file_path)
    result+=[maxValue(temp_file_path)]
    result+=[avgValue(temp_file_path)]
    os.remove(temp_file_path)
    return result

# extractFileList(path,ID):
#
# DESCRIPTION
#    Returns a file names list, in which every name matches an ID string
# INPUT
#    Needs as inputs:
#       path: directory where to extract file names.
#       ID  : string to identify which files.
# OUTPUT
#    Returns list of file names.
def extractFileList(path,ID):
    filelist=[]
    res_file_list=[]
    for (dirpath, dirnames, filenames) in walk(path):
        filelist.extend(filenames)
        break
    for x in filelist:
        if ID in x:
            res_file_list+=[x]
    return res_file_list

# sortFileList(file_list):
#
# DESCRIPTION
#    Sorts file name list
# INPUT
#    Needs as inputs:
#       file_list: generic list of strings (file names)
# OUTPUT
#    No return.
def sortFileList(file_list):
    file_list.sort()
    file_list.sort(key=len)

# extractTruncLSBs(file_name):
#
# DESCRIPTION
#    Extracts how many LSBs have been truncated in the multiplier architecture
# INPUT
#    Needs as inputs:
#       file_name: string representig the file name where we haveto extract
#                  which architecture we are referring to
# OUTPUT
#    Returns how many LSBs have been truncated in the multiplier architecture
def extractTruncLSBs(file_name):
    print("To be implemented")

# extractRepType(file_name):
#
# DESCRIPTION
#    Extracts the type of report from the name of the file we're referring to
# INPUT
#    Needs as inputs:
#       file_name: string representig the file name where we have to extract
#                  which report we are referring to
# OUTPUT
#    Returns the type of report from the name of the file we're referring to
def extractRepType(file_name):
    print("To be implemented")


# checkResult(file1,file2):
#
# DESCRIPTION
#    Checks if two files are identically the same or how may lines are different
# INPUT
#    Needs as inputs:
#       file1,file2: names of two files to be checked
# OUTPUT
#    Returns how many lines differ.
def checkResult(file1,file2):
    i=0
    with open(file1, "r") as f1_pointer, open(file2, "r") as f2_pointer:
        for line1 in f1_pointer:
            line2=f2_pointer.readline()
            if line1!=line2:
                i+=1
    return i

# message(string):
#
# DESCRIPTION
#    Redirects string to a certain output
# INPUT
#    Needs as inputs:
#       string: the list of char to be redirected to output
# OUTPUT
#    No return.
def message(string):
    print(string)

def printBasicAnalysisRes(log_pointer,analysis_res,ID):
    log_pointer.write("{}\n".format(ID))
    log_pointer.write("MaxValue: {}\tAvgValue: {}".format(analysis_res[0],analysis_res[1]))
