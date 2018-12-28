import sys
bin_lib_path='/home/clmcasino/Desktop/ISA/Lab2/ISA-digital-arithmetic/HW_filter/version2/script/py_model'
sys.path.append(bin_lib_path)

from bin_lib    import twos_comp

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

    for line in area_rep_file:
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

    for line in timing_rep_file:
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
            fout_pointer.write(rel_dist+'\n')

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
            num=int(line)
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
            sum+=int(line)
            j+=1
        avg=sum/j
        return (avg)
