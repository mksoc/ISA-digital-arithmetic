from wrDaddaTree import wrDaddaTree
import matlab.engine
import fileHandling as fh
import as sim
import as synth

def generateMultiplier(delimiter, srcPath, outPath, compression, startingDirection)

	tempPath = outPath+".tempFile"

	wrDaddaTree(tempPath, compression, startingDirection)
	
	with open(outPath, "w") as outFile, open(srcPath, "r") as srcFile, open(tempPath, "r") as tempFile:
		for srcLine in srcFile:
			if (srcLine != delimiter):
				outFile.write(srcLine)
			else:
				for tempLine in tempFile:
					outFile.write(tempLine)

	os.remove(tempPath)

def genScripts():
	# gen sim script for multiplier
	tclGen('sim', False, 'multiplier', s.mult_tcl_name) # (tclType, synthesized, design, tcl_name) 
	# gen sim script for the whole filter
	tclGen('sim', False, 'filter', s.filter_tcl_name)
	# gen sim script for synth multiplier
	tclGen('sim', True, 'multiplier', s.sMult_tcl_name)
	# gen sim script for the synth whole filter
	tclGen('sim', True, 'filter', s.sFilter_tcl_name)
	# gen synth script for the multiplier
	tclGen('synth', 'multiplier', s.mult_synth_tcl_name)
	# gen synth script for the whole filter
	tclGen('synth', 'filter', s.filter_synth_tcl_name)

def genSamples():
	in_gen(s.n_samples) # (samples = 10000)
	os.rename("./fileIn.txt", s.multSamples_name)
	gen_samples()
	os.rename('py-samples.txt', s.filterSamples_name)

def performSim(session, remote_root, tclName):
	session.run_commands("""cd {root}/sim
	    source /software/scripts/init_msim6.2g
	    rm vsim.wlf
	    if [ ! -d work ]; then vlib work; fi
	    vsim -c -do {tclName}
	    mv iir_filter_back.saif ../version{ver}""".format(root=remote_root, tclName=tclName, ver=3))

def performSynth(session, remote_root, tclName):
    session.run_commands("""cd {root}/syn
		source /software/scripts/init_synopsys
		mkdir work logs reports saif netlist
		dc_shell-xg-t -f {tclName}
		mv netlist/* ../version{ver}
		mv saif/NangateOpenCellLibrary.saif ../sim""".format(root=remote_root, tclName=tclName, ver=3))

def message(string)
	print(string+'\n')

def cmd(string)
	subprocess.run(string.split())

def tclGen(tclType, synthesized=False, design='', tcl_name):

	if design == 'multiplier':
		entity = s.multEntity_name
		if !synthesized:
			src_compile_str = '''
				vcom -93 -work {sim}/work {v3}/multV3_pkg.vhd
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
		tb_compile_str = 'vcom -93 -work {sim}/work {tb}/{TBentity}.vhd'.format(
			sim=s.remote_simPath, 
			tb=s.remote_tbPath,
			TBentity='{entity}TB'.format(entity))

	elif design == 'filter':
		entity = s.filterEntity_name
		if !synthesized:
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
			TBentity='{entity}TB'.format(entity))

	else: sys.exit('Error in tclGen, please check the passed design.')

	lib_load_str = 'vsim {library} work.{TBentity}'.format(
		library='' if !synthesized else '-L /software/dk/nangate45/verilog/msim6.2g -sdftyp /iir_filterTB/UUT=../version3/{entity}.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so'.format(entity=entity),
		TBentity='{entity}TB'.format(entity))

	if tclType == 'sim':
		with open(tcl_name, 'w') as f:
			f.write('''	
				# compile source files
				{src_string}
				
				# compile testbench
				{tb_string}
				
				# load design
				{lib_compile_str}
				
				# run simulation
				run -all '''.format(
					src_string=src_compile_str,
					tb_string=tb_compile_str, 
					lib_load_str=lib_compile_str))

	elif tclType == 'synth':
		with open(tcl_name, 'w') as f:
			f.write('''
				# there will be a compile ultra command later
				set ultra optimization true

				# analyze src files
				analyze -f vhdl -lib WORK {src}/filter_pkg.vhd
				analyze -f vhdl -lib WORK {v3}/multV3_pkg.vhd
				analyze -f vhdl -lib WORK {src}/*.vhd
				analyze -f vhdl -lib WORK {v3}/*.vhd

				# preserve RTL names
				set power_preserve_rtl_hier_names true

				# elaborate design
				elaborate {entity} -arch structure -lib WORK > ./logs/elaborate-log.txt
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

				# start synthesis
				compile_ultra

				# apply retiming to design
				set_dont_touch *reg_in*
				set_dont_touch *reg_coeff_fb_i_*
				set_dont_touch *reg_b_i_*
				set_dont_touch *reg_out*
				optimize_registers

				# reports gen
				report_timing > {common}/{entity}_{t}
				report_area > {common}/{entity}_{a}
				ungroup -all -flatten
				change_names -hierarchy -rules verilog
				write_sdf ../netlist/iir_filter.sdf
				write -f verilog -hierarchy -output ../netlist/iir_filter.v
				write_sdc ../netlist/iir_filter.sdc
				quit'''.format(
					src=s.remote_srcPath,
					v3=s.remote_v3Path,
					entity=entity,
					clk=0,
					common=s.remote_commonPath, 
					entity=entity,
					t=s.timingReport_name, 
					a=s.areaReport_name))

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