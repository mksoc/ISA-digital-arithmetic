import random
from bin_lib import twos_comp, printer_2s

# binStimGen(fname,lineNum,stimInLine,bitDyn,nBit):
#
# DESCRIPTION
#    Creates a file with <stimNum> stimuli.
# INPUT
#    Needs as inputs:
#       fname:      string with complete output file path nameself.
#       lineNum:    amount of lines.
#       stimInLine: how many stimuli in a line.
#       bitDyn:     real dynamic of output numb.
#       nBit:       number of output bit in the string.
#       delimiter:  delimiter character between two consecutive stimuli.
# OUTPUT
#    Creates a file of stimuli in the specified path.
def binStimGen(fname,lineNum,stimInLine,bitDyn,nBit,delimiter):
    with open(fname,"w") as fout_pointer:
        i=0
        while i<lineNum:
            j=0
            string=""
            while j<stimInLine:
                num=random.randint(-2**(bitDyn-1)+1,2**(bitDyn-1)-1)
                string+=printer_2s(num,nBit)
                string+=delimiter
                j+=1
            fout_pointer.write(string+"\n")
            i+=1
