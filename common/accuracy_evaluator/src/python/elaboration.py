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

def prepareSimScripts(session, remote_root):
	print('\nGenerating TCL script for simulation.')
    genSimScript(1) # design
    scriptNewPath = './py-sim-script_noSynth.tcl'
    fh.renameFile('./py-sim-script.tcl', scriptNewPath)
    print('\nMoving script to server.')
    session.copy_to(scriptNewPath, '{}/sim/'.format(remote_root))
    fh.moveFile(scriptNewPath, s.tmpPath)

    print('\nGenerating TCL script for simulation after synthesis.')
    genSimScript(0) # design
    scriptNewPath = './py-sim-script_synth.tcl'
    fh.renameFile('./py-sim-script.tcl', scriptNewPath)
    print('\nMoving script to server.')
    session.copy_to(scriptNewPath, '{}/sim/'.format(remote_root))
    fh.moveFile(scriptNewPath, s.tmpPath)

def prepareSynthScript(session, repo_root, remote_root):
	print('\nGenerating TCL script for synthesis.')
	genSynthScript()
	print('\nMoving script to server.')
    session.copy_to('./py-syn-script.tcl', '{}/syn/'.format(remote_root))
    session.copy_to('{}/HW_filter/syn/.synopsys_dc.setup'.format(repo_root), '{}/syn/'.format(remote_root))
    fh.moveFile('./py-syn-script.tcl', s.tmpPath)

# generate script for simulation
def genSimScript(design):
	print('\nGenerating TCL script for simulation.')
	sim.gen_tcl(1, 1, 3, design) # run_remote, cli_mode, version, design

# generate script for simulation
def genSynthScript():
	print('\nGenerating TCL script for synthesis.')
	synth.gen_tcl(3, s.period, s.adder, s.multiplier, s.compile_cmd) # version, period, adder=None, multiplier=None, compile_cmd='compile'

def performSim(session, remote_root, tclName):
	session.run_commands("""cd {root}/sim
	    source /software/scripts/init_msim6.2g
	    rm vsim.wlf
	    if [ ! -d work ]; then vlib work; fi
	    vsim -c -do {tclName}
	    mv iir_filter_back.saif ../version{ver}""".format(root=remote_root, tclName=tclName, ver=3))

def performSynth(session, remote_root, tclName):
	# run synthesis on server
    print('\nRun synthesis')
    session.run_commands("""cd {root}/syn
            source /software/scripts/init_synopsys
            mkdir work logs reports saif netlist
            dc_shell-xg-t -f {tclName}
            mv netlist/* ../version{ver}
            mv saif/NangateOpenCellLibrary.saif ../sim""".format(root=remote_root, tclName=tclName, ver=3))

def matlabScript():
	matlab = matlab.engine.start_matlab()
	matlab.calcErr()

def renameAndStoreMult(srcFilePath, destFolder, label):
	newSrcFilePath = srcFilePath+"."+label
	fh.renameFile(srcFilePath, newSrcFilePath)
	fh.moveFile(srcFilePath, destFolder)

def message(string)
	print(string+'\n')

def cmd(string)
	subprocess.run(string.split())