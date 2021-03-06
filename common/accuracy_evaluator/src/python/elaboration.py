import sys
import os
import subprocess
import fileHandling as fh
import settings as s
sys.path.append('{}/HW_filter/version3/script/vhdl_gen'.format(s.repo_root))
from wrDaddaTree import wrDaddaTree
sys.path.append('{}/HW_filter/version2/script/py_model'.format(s.repo_root))
from in_gen import binStimGen
sys.path.append('{}/common'.format(s.repo_root))
from samples_generator import gen_samples_core

def generateMultiplier(delimiter, srcPath, outPath, compression, startingDirection, dummyCol):

	tempPath = outPath+".tempFile"

	wrDaddaTree(tempPath, compression, startingDirection, dummyCol)

	with open(outPath, "w") as outFile, open(srcPath, "r") as srcFile, open(tempPath, "r") as tempFile:
		for srcLine in srcFile:
			if (srcLine != delimiter):
				outFile.write(srcLine.format(nBit=dummyCol))
			else:
				for tempLine in tempFile:
					outFile.write(tempLine)

	os.remove(tempPath)

def genScripts():
	# gen sim script for multiplier
	tclGen('sim', s.mult_sim_tcl_name, False, 'multiplier') # (tclType, synthesized, design, tcl_name) 
	# gen sim script for the whole filter
	tclGen('sim', s.filter_sim_tcl_name, False, 'filter')
	# gen sim script for synth multiplier
	tclGen('sim', s.sMult_sim_tcl_name, True, 'multiplier')
	# gen sim script for the synth whole filter
	tclGen('sim', s.sFilter_sim_tcl_name, True, 'filter')
	# gen synth script for the multiplier
	tclGen('synth', s.mult_synth_tcl_name, False, 'multiplier')
	# gen synth script for the whole filter
	tclGen('synth', s.filter_synth_tcl_name, False, 'filter')

def genSamples():
	binStimGen(s.multSamples_name, s.n_samples, 2, s.NB_extended-1, s.NB_extended, " ")
	gen_samples_core(s.filterSamples_name, s.NB, s.n_samples_iir, s.n_samples_iir_mode)

def performSim(session, remote_root, tclName, entity):
	session.run_commands("""cd {root}/sim
	    source /software/scripts/init_msim6.2g
	    rm vsim.wlf
	    if [ ! -d work ]; then vlib work; fi
	    vsim -c -do {tclName}
	    mv {ent}_back.saif ../version{ver}""".format(root=remote_root, tclName=tclName, ent=entity, ver=3))

def performSynth(session, remote_root, tclName):
    session.run_commands("""cd {root}/syn
		source /software/scripts/init_synopsys
		mkdir work logs reports saif netlist
		dc_shell-xg-t -f {tclName}
		mv netlist/* ../version{ver}
		mv saif/NangateOpenCellLibrary.saif ../sim""".format(root=remote_root, tclName=tclName, ver=3))

def message(string):
	print(string+'\n')

def cmd(string):
	subprocess.run(string.split())

def tclGen(tclType, tcl_name, synthesized=False, design=''):

	if s.isComp_ultra:
		compile_str = 'compile_ultra'
	else:
		compile_str = 'compile'

	if design == 'multiplier':
		entity = s.multWRegsEntity_name
		retimingString = ''' 
				set_dont_touch *reg_in*
				set_dont_touch *reg_out*
				optimize_registers'''
		if not synthesized:
			src_compile_str = '''
				vcom -93 -work {sim}/work {v3}/multV3_pkg.vhd
				vcom -93 -work {sim}/work {src}/reg.vhd
				vcom -93 -work {sim}/work {v3}/*.vhd '''.format(
					sim=s.remote_simPath,
					src=s.remote_srcPath,
					v3=s.remote_v3Path)
		else:
			src_compile_str = '''
				vcom -93 -work {sim}/work {v3}/multV3_pkg.vhd
				vcom -93 -work {sim}/work {src}/reg.vhd
				vlog -work {sim}/work {v3}/*.v '''.format(
					sim=s.remote_simPath,
					src=s.remote_srcPath,
					v3=s.remote_v3Path)
		tb_compile_str = 'vcom -93 -work {sim}/work {tb}/{TBentity}.vhd'.format(
			sim=s.remote_simPath, 
			tb=s.remote_tbPath,
			TBentity='{}TB'.format(entity))
		run_str = 'run {simTime}'.format(simTime=s.sim_time)

	elif design == 'filter':
		entity = s.filterEntity_name
		retimingString = ''' 
				set_dont_touch *reg_in*
				set_dont_touch *reg_coeff_fb_i_*
				set_dont_touch *reg_b_i_*
				set_dont_touch *reg_out*
				optimize_registers'''
		if not synthesized:
			src_compile_str = '''
				vcom -93 -work {sim}/work {src}/filter_pkg.vhd
				vcom -93 -work {sim}/work {v3}/multV3_pkg.vhd
				vcom -93 -work {sim}/work {src}/*.vhd
				vcom -93 -work {sim}/work {v3}/*.vhd '''.format(
					sim=s.remote_simPath,
					src=s.remote_srcPath,
					v3=s.remote_v3Path)
		else:
			src_compile_str = '''
				vcom -93 -work {sim}/work {src}/filter_pkg.vhd
				vcom -93 -work {sim}/work {v3}/multV3_pkg.vhd
				vlog -work {sim}/work {v3}/*.v '''.format(
					sim=s.remote_simPath,
					src=s.remote_srcPath,
					v3=s.remote_v3Path)
		tb_compile_str = '''	
			vcom -93 -work {sim}/work {tb}/*.vhd
			vlog -work {sim}/work {tb}/{TBentity}.v '''.format(
			sim=s.remote_simPath,
			tb=s.remote_tbPath,
			TBentity='{}TB'.format(entity))
		run_str = 'run -all'

	else: sys.exit('Error in tclGen, please check the passed design.')

	lib_load_str = 'vsim {library} work.{TBentity}'.format(
		library='' if not synthesized else '-L /software/dk/nangate45/verilog/msim6.2g -sdftyp /{entity}TB/UUT={v3}/{entity}.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so'.format(entity=entity, v3=s.remote_v3Path),
		TBentity='{}TB'.format(entity))

	if tclType == 'sim':
		with open(tcl_name, 'w') as f:
			f.write('''	
				# compile source files
				{src_string}
				
				# compile testbench
				{tb_string}
				
				# load design
				{lib_load_string}
				
				# run simulation
				{run_string} '''.format(
					src_string=src_compile_str,
					tb_string=tb_compile_str, 
					lib_load_string=lib_load_str,
					run_string=run_str))

	elif tclType == 'synth':
		with open(tcl_name, 'w') as f:
			f.write('''
				# there will be a compile ultra command later
				set_ultra_optimization {isCompUltra}'''.format(
					isCompUltra=str(s.isComp_ultra),
					))

			# Analyze 
			src_files = [file for file in os.listdir(s.local_src) if os.path.isfile(os.path.join(s.local_src, file))]
			prj_files = [file for file in os.listdir(s.local_project) if os.path.isfile(os.path.join(s.local_project, file))]
			ver_files = [file for file in os.listdir(s.local_srcMult) if os.path.isfile(os.path.join(s.local_srcMult, file)) and '.vhd' in file]
			if 'filter_pkg.vhd' in src_files:
				f.write('\nanalyze -f vhdl -lib WORK {src}/filter_pkg.vhd'.format(src=s.remote_srcPath))
				src_files.remove('filter_pkg.vhd')
			if 'multV3_pkg.vhd' in ver_files:
				f.write('\nanalyze -f vhdl -lib WORK {v3}/multV3_pkg.vhd'.format(v3=s.remote_v3Path))
				ver_files.remove('multV3_pkg.vhd')
			for file in src_files:
				f.write('\nanalyze -f vhdl -lib WORK {src}/{f}'.format(src=s.remote_srcPath, f=file))
			for file in prj_files:
				f.write('\nanalyze -f vhdl -lib WORK {src}/{f}'.format(src=s.remote_srcPath, f=file))
			for file in ver_files:
				f.write('\nanalyze -f vhdl -lib WORK {v3}/{f}'.format(v3=s.remote_v3Path, f=file))

			f.write('''
				# preserve RTL names
				set power_preserve_rtl_hier_names true

				# elaborate design
				elaborate {ent} -arch structure -lib WORK > ./logs/elaborate-log.txt
				uniquify
				link

				# create symbolic clock signal
				create_clock -name CLOCK -period {clk} clk
				set_dont_touch_network CLOCK
				set_clock_uncertainty 0.07 [get_clocks CLOCK]

				# set input/output delays
				set_input_delay 0.5 -max -clock CLOCK [remove_from_collection [all_inputs] CLOCK]
				set_output_delay 0.5 -max -clock CLOCK [all_outputs]
				
				# set output load capacitance
				set OLOAD [load_of NangateOpenCellLibrary/BUF_X4/A]
				set $OLOAD [all_outputs]

				# flatten hierarchy
				ungroup -all -flatten

				# start synthesis
				{compile}

				# apply retiming to design
				{retiming}

				# reports gen
				report_timing > {common}/{ent}_{t}
				report_area > {common}/{ent}_{a}
				change_names -hierarchy -rules verilog
				write_sdf {syn}/netlist/{ent}.sdf
				write -f verilog -hierarchy -output {syn}/netlist/{ent}.v
				write_sdc {syn}/netlist/{ent}.sdc
				quit'''.format(
					ent=entity,
					clk=0,
					compile=compile_str,
					retiming=retimingString,
					common=s.remote_commonPath,
					t=s.timingReport_name, 
					a=s.areaReport_name,
					syn=s.remote_synPath))

	else: sys.exit('Error in tclGen, please check the passed design.')

def compileCfilter():
	if not os.path.isfile(s.c_exe_name):
		cmd('g++ {Cfilter_src_folder}/iir_filter.c -o {program}'.format(
			Cfilter_src_folder=s.cFilterPath, 
			program=s.c_exe_name))

def Cfilter():
    cmd('./{program} {inputFolder}/{inputFile} {resultPath}/{resultFile}'.format(	
        program=s.c_exe_name, 
        inputFolder=s.inputPath, 
        inputFile=s.filterSamples_name, 
        resultPath=s.resultPath, 
        resultFile=s.c_resultFile_name))

def matlabScript():
	matlab = matlab.engine.start_matlab()
	matlab.calcErr()