#!/usr/bin/python3
import os
import subprocess
import elaboration as el
import settings as s
import fileHandling as fh
sys.path.append('{}/common'.format(s.repo_root))
import isa

# connect to the server
el.message('Connecting to the server...')
session = isa.ssh_session(s.username, s.server, s.port, True)
el.message('Connection established.')

# clear folders on server
el.message('Cleaning server folders...')
fh.cleanServer(session)
el.message('Cleaning completed.')

# clear folders in local
el.message('Removing the work tree...')
fh.removeTree(s.workPath)
el.message('Operation completed.')

# prepare local tree
el.message('Creating a new working tree...')
fh.buildTree()
el.message('Done. Let\'s go!')

# gen sim scripts and copy them to the server
with isa.cd(s.scriptPath):
	el.message('Generating the scripts for my dark purposes... keep calm and no one will be harmed.')
	el.genScripts()
	el.message('Everything as I planned...')
	# copy scripts to the server
	el.message('Copying the scripts to the server.')
	fh.uploadScripts(session)
	el.message('Let\'s go on.')

# generate samples and transfer to the server
el.message('Generating samples for the filter and for the multiplier.')
with isa.cd(s.inputPath):
	el.genSamples()
	el.message('Done. Trasferring to the server...')
	fh.uploadSamples(session)
	el.message('We are working well today!')

# calculate SW output for the generated samples
el.message('Calculating the SW outputs for the filter.')
with isa.cd(s.cFilterPath):
	el.compileCfilter()
	el.message('Running C model on the samples.')
	el.Cfilter()
	el.message('Done.')

# upload the common src and tb files
el.message('Common files will be uploaded now. Look at this!!')
fh.uploadSrcTb(session)
el.message('And now we can enter the loop... it will take a while, so keep calm.')

# loop
for compressionLevel in s.compressionList:
	for startingDirection in s.directionList:
		
		# create the multiplier
		el.message('Creating the multipliers with a compression level of {comp}. The binding is begun from {dir}'.format(
			comp=compressionLevel,
			dir=startingDirection))
		with isa.cd(s.multiplierPath):
			el.generateMultiplier(s.delimiter, s.srcMultPath, s.multFileName, compressionLevel, startingDirection)
			el.generateMultiplier(s.delimiter, s.srcMultWRegsPath, s.multWRegsFileName, compressionLevel, startingDirection)
			# transfer the multiplier
			el.message('Uploading all the multiplier related files...')
			fh.uploadMultiplier(session)
			fh.uploadMultiplierWRegs(session)
			el.message('Ok Houston, no problems.')
			# rename the local multiplier
			el.message('Renaming the multiplier file...')
			newName = '{base_name}.{cmp}{dir}.vhd'.format(base_name=s.multEntity_name, cmp=compressionLevel, dir=startingDirection)
			os.rename(s.multFileName, newName)
			newName = '{base_name}.{cmp}{dir}.vhd'.format(base_name=s.multWRegsEntity_name, cmp=compressionLevel, dir=startingDirection)
			os.rename(s.multWRegsFileName, newName)
			el.message('It was a breeze.')
	
		# sim the mult
		el.message('Starting the simulation of the mult, baby!')
		el.performSim(session, s.remote_root, s.mult_sim_tcl_name, s.multWRegsEntity_name)
		el.message('It\'s important to keep these brittle results in a safe place.')
	
		# upload synth related files and synth the mult
		el.message('Starting the synthesis of the mult, roar!')
		session.copy_to('{}/.synopsys_dc.setup'.format(s.local_syn), '{}/syn/'.format(s.remote_root))
		el.performSynth(session, s.remote_root, s.mult_synth_tcl_name)
		el.message('Synthesized.')

		# clean the syn-work folder
		fh.cleanSyn(session)
		# re-upload scripts
		with isa.cd(s.scriptPath):
			fh.uploadScripts(session)

		# take back, rename and store the sim results
		el.message('Let\'s take back what belongs to us.')
		fh.storeResultsReports(session, s.multWRegsEntity_name, False, compressionLevel, startingDirection)
		# clean the common folder from sim output files
		fh.cleanCommon(session)
		# re-upload samples
		with isa.cd(s.inputPath):
			fh.uploadSamples(session)
		el.message('It would have been impossible for someone. But here we are.')	
	
		# sim the filter
		el.message('Starting the simulation of the filter, baby!')
		el.performSim(session, s.remote_root, s.filter_sim_tcl_name, s.filterEntity_name)
		el.message('It\'s important to keep these delicate results in a safe place.')
	
		# upload synth related files and synth the filter
		el.message('Starting the synthesis of the filter, baby!')
		session.copy_to('{}/.synopsys_dc.setup'.format(s.local_syn), '{}/syn/'.format(s.remote_root))
		el.performSynth(session, s.remote_root, s.filter_synth_tcl_name)
		el.message('Synthesized.')
	
		# clean the syn-work folder
		fh.cleanSyn(session)
		# re-upload scripts
		with isa.cd(s.scriptPath):
			fh.uploadScripts(session)

		# take back, rename and store the results and reports
		fh.storeResultsReports(session, s.filterEntity_name, False, compressionLevel, startingDirection)

		el.message('Finished a loop step: cleaning common and re-uploading the same Samples')
		# clean the common folder from output files
		fh.cleanCommon(session)
		# re-upload samples
		with isa.cd(s.inputPath):
			fh.uploadSamples(session)
		el.message('Let\'s go on!')

el.message('The hard part has been over, relax. It\'s time to analyze the results.')
# elaborate the results 
