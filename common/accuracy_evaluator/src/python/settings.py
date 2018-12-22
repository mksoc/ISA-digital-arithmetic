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
repo_root = isa.get_root(s.repo_name)
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
# path of the handwritten part of the multiplier
srcMultPath = '{}/HW_filter/version1/vhdl/src/src_handWrittenMult/srcMult.vhd'.format(repo_root)
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
filter_synth_tcl_name = 'synth-mult.tcl'

multSamples_name = 'multSample.txt'
filterSamples_name = 'filterSamples.txt'

c_exe_name = 'iir_filter'
c_resultFile_name = 'filter_SW-output.txt'

multResult_name = 'mult_HW-output.txt'
filterResult_name = 'filter_HW-output.txt'
powReport_name = 'power.txt'
areaReport_name = 'area.txt'
timingReport_name = 'timing.txt'

multBaseName = 'mbeDadda_mult'

resultFilesList = ['mult_HW-output.txt', 'filter_HW-output.txt']
reportFilesList = ['power.txt' ,'area.txt', 'timing.txt']

# --------------------------------- PARAM --------------------------------- 

n_samples = 10000

compressionList = list(range(0, 100, 5))
directionList = ['right', 'left']

delimiter = '--- DELIMITER ---'