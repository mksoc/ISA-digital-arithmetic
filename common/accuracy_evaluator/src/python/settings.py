import sys
sys.path.append('{}'.format('../../..'))
import isa

# --------------------------------- SERVER ---------------------------------

# ssh connection parameters
username = 'isa22'
server = 'led-x3850-2.polito.it'
port = 10020
# server root for the lab2
remote_root = '/home/isa22/lab2'
# remote VHDL src path
remote_srcPath = '{}/src'.format(remote_root)
# remote VHDL/Verilog tb path
remote_tbPath = '{}/tb'.format(remote_root)
# remote VHDL sim path
remote_simPath = '{}/sim'.format(remote_root)
# remote syn path
remote_synPath = '{}/syn'.format(remote_root)
# remote common path
remote_commonPath = '{}/common'.format(remote_root)
# remote version1 path
remote_v1Path = '{}/version1'.format(remote_root)
# remote version2 path
remote_v2Path = '{}/version2'.format(remote_root)
# remote version3 path
remote_v3Path = '{}/version3'.format(remote_root)

# --------------------------------- LOCAL ---------------------------------

# github repository name
repo_name = 'ISA-digital-arithmetic'
# local github repository root
repo_root = isa.get_root(repo_name)
# local paths for files related to the main script
workPath = '{}/common/accuracy_evaluator/work'.format(repo_root)
tmpPath = '{}/tmp'.format(workPath)
inputPath = '{}/input'.format(workPath)
multiplierPath = '{}/multiplier'.format(workPath)
reportPath = '{}/report'.format(workPath)
resultPath = '{}/result'.format(workPath)
scriptPath = '{}/script'.format(workPath)

local_srcMult = '{}/HW_filter/version3/vhdl/src'.format(repo_root)
local_tbMult = '{}/HW_filter/version3/vhdl/tb'.format(repo_root)
local_project = '{}/HW_filter/version3/vhdl/src/project'.format(repo_root)
local_src = '{}/HW_filter/src'.format(repo_root)
local_tb = '{}/HW_filter/tb'.format(repo_root)
local_syn = '{}/HW_filter/syn'.format(repo_root)
# path of the handwritten part of the multiplier
srcMultPath = '{}/HW_filter/version3/vhdl/src/src_handWrittenMult/srcMult.vhd'.format(repo_root)
srcMultWRegsPath = '{}/HW_filter/version3/vhdl/src/src_handWrittenMult/srcMult_wRegs.vhd'.format(repo_root)
# local useful paths
local_simV1 = '{}/HW_filter/version1/vhdl/sim'.format(repo_root)
local_simV2 = ''
local_simV3 = '{}/HW_filter/version3/vhdl/sim'.format(repo_root)

cFilterPath = '{}/C_filter'.format(repo_root)


# --------------------------------- NAMES --------------------------------- 

# sim script for multiplier
mult_sim_tcl_name = 'sim-mult.tcl'
# sim script for filter
filter_sim_tcl_name = 'sim-filter.tcl'
# sim script for synth multiplier
sMult_sim_tcl_name = 'sim-synthMult.tcl'
# sim script for synth filter
sFilter_sim_tcl_name = 'sim-synthFilter.tcl'
# synth script to synth the mult
mult_synth_tcl_name = 'synth-mult.tcl'
# synth script to synth the filter
filter_synth_tcl_name = 'synth-filter.tcl'
# report script name
report_tcl_name = 'reports-gen.tcl'

multSamples_name = 'multSample.txt'
filterSamples_name = 'filterSamples.txt'

c_exe_name = 'iir_filter'
multEntity_name = 'mbeDadda_mult'
multWRegsEntity_name = 'mbeDadda_mult_wRegs'
filterEntity_name = 'iir_filter'

c_resultFile_name = 'filter_SW-output.txt'

multSWResult_name = 'mult_SW-output.txt'
multResult_name = 'mult_HW-output.txt'
filterResult_name = 'filter_HW-output.txt'
powReport_name = 'power.txt'
areaReport_name = 'area.txt'
timingReport_name = 'timing.txt'

multFileName = 'mbeDadda_mult.vhd'
multWRegsFileName = 'mbeDadda_mult_wRegs.vhd'

resultFilesList = ['mult_HW-output.txt', 'filter_HW-output.txt', 'mult_SW-output.txt']
reportFilesList = ['area.txt', 'timing.txt']

# --------------------------------- PARAM --------------------------------- 

# number of bits of the multiplier operands
NB_extended = 24

# number of fractional bits to be approximated in the truncation after the multiplication
truncatedBits = 22 

# samples for the multiplier
n_samples = 250000

# NB -> number of bits of the input of the iir_filter, needed for the generation of the samples
# parameter used in genSamples(), inside gen_samples_core(fileName, NB, samples, mode) from samples_generator.py
NB = 12

# delimiter for the VHDL
delimiter = '---DELIMITER---\n'

### USUAL PARAMETERS TO BE SET ###

# samples for the iir_filter
n_samples_iir = 250000
# n_samples_iir_mode = 1 -> random samples
# n_samples_iir_mode = 2 -> samples at the extremis
n_samples_iir_mode = 1

# percentage of compression in terms of columns of the multiplier
# it holds the various percentage to be tested
compressionList = list(range(0, 105, 20))

# starting direction for the compression: right, left or (right and left)
directionList = ['right', 'left']

# num of bits to be removed BEFORE the tree of the multiplier, from two bits to the max accepted number of bits (can't remove more bits wrt the final number of removed bits)
approxBitsList = list(range(2, truncatedBits))

# enable compile ultra for the synthesis?
isComp_ultra = False

###                           ###