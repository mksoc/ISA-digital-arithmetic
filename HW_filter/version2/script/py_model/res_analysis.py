
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
