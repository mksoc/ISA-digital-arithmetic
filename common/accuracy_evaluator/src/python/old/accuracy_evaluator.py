# -------------------------------------- IMPORT MODULES AND FUNCTIONS -------------------------------------

import settings as s
import elaboration as e
import isa

# --------------------------------------- FUNCTION DEFINITION ----------------------------------------------

def accuracy_evaluator(wholeDesign1_multiplierOnly0):
    
    # --------------------------------------- IMPORT CONSTANTS AND SETTINGS ------------------------------------

    # set repo root path
    repo_root = isa.get_root(s.repo_name)
    
    # ------------------------------------- CONNECT TO THE SERVER -----------------------------------------------
    
    print('Connecting to the server...\n')
    session = isa.ssh_session(s.username, s.server, s.port)
    print('Connection established.\n')
    
    # ---------------------------------------- GENERATE SAMPLES -------------------------------------------------
    
    if (wholeDesign1_multiplierOnly0):
    	with isa.cd('{}/common'.format(repo_root)):
    	    gen_samples()
    	    os.rename('py-samples.txt', 'samples.txt')
    	
    	# transfer samples.txt to the server
    	print('\nCopy samples to server.')
    	session.copy_to('{}/common/samples.txt'.format(repo_root), '{}/common/'.format(s.remote_root))
    else:
    	with isa.cd('{}/HW_filter/version1/script/common_gen'.format(repo_root)):
    		cmd = './in_gen.py'
    		subprocess.call(cmd)
    		fh.renameFile("./fileIn.txt", "./multiplierInputs.txt")
    		print('\nCopying multiplier inputs to the server.')
    		session.copy_to("./multiplierInputs.txt", '{}/common/'.format(s.remote_root))
			fh.copyFile("./multiplierInputs.txt", '{}/HW_filter/version1/common'.format(repo_root))
    		fh.moveFile("./multiplierInputs.txt", s.inputPath)
    
    # ---------------------------------------- RUN THE SW MODEL --------------------------------------------------
    
    if (wholeDesign1_multiplierOnly0):
    # compile C model if not already there and run it
    with isa.cd('{}/C_filter'.format(repo_root)):
        c_exe_name = 'iir_filter.o'
        if not os.path.isfile(c_exe_name):
            print('\nNo executable for C model found. Will compile C file.')
            os.system('g++ iir_filter.c -o {}'.format(c_exe_name))
        print('\nRun C model on selected samples.')
        os.system('./{} ../common/samples.txt ../common/results-c.txt'.format(c_exe_name))
        print()
    else:
    	with isa.cd('{}/HW_filter/version1/sim'.format(repo_root))
    		cmd = 'vsim -c do ./script/multTest.tcl'
    		subprocess.call(cmd.split())
    		
    
    # ------------------------------------- GENERATE SCRIPTS FOR SIM ----------------------------------------------
    
    if (wholeDesign1_multiplierOnly0):
    	prepareSimScripts(session, s.remote_root)
    
    # ------------------------------------- GENERATE SCRIPT FOR SYNTH --------------------------------------------
    
    if (wholeDesign1_multiplierOnly0):
	    prepareSynthScript(session, repo_root, s.remote_root)
    
    # ------------------------------------------ LOOP: -----------------------------------------------------------
    
    label = 0
    for multVhdl in :
        # generate the next vhdl
        e.generateMultiplier(s.srcMultPath, completeMultPath, compression, startingDirection);
    
        # trasfer the vhdl to the server
        # transfer mbeDadda_mult.vhd to the server
        print('\nCopying mbeDadda_mult.vhd to server.')
        session.copy_to(completeMultPath, s.remote_srcPath)
    
        # sim -> call simulator.py
        e.performSim(session, remote_root, 0)
    
        # synth + sim + reports -> call pynthesizer
        e.performSynth(session, s.remote_root)
        e.performSim(session, remote_root, 1)
    
        # copy the results and the reports to local
        print('\nCopying results to local folder.')
        session.copy_from(remote_resultsPath, local_resultsFolder)
        print('\nCopying reports to local folder.')
        session.copy_from(remote_resultsPath, local_reportsFolder)
    
        # store the current vhdl and branch to LOOP until all the multipliers have been tested
        e.renameAndStoreMult(srcFilePath, destFolder, label)
    
        # increment the label
        label += 1
    
    # ------------------------------------- MATLAB ELABORATION ----------------------------------------------
    
    e.matlabScript()

if __name__ == "__main__":
    accuracy_evaluator()