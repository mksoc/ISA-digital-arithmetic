import os
import subprocess
from elaboration import message, cmd, generateMultiplier
import settings as s
import isa
from fileHandling import mkdir, removeTree, cleanServer

# connect to the server
message('Connecting to the server...')
session = isa.ssh_session(s.username, s.server, s.port)
message('Connection established.')

# clear folders on server
message('Cleaning server folders...')
cleanServer(session)
message('Cleaning completed.')

# clear folders in local
message('Removing the work tree...')
removeTree(s.workPath)
message('Operation completed.')

# prepare local tree
message('Creating a new working tree...')
buildTree()
message('Done. Let\'s go!')

# gen sim scripts and copy them to the server
with isa.cd(s.scriptPath):
	message('Generating the scripts for my dark purposes... keep calm and no one will be harmed.')
	genScripts()
	message('Everything as I planned...')
	# copy scripts to the server
	message('Copying the scripts to the server.')
	uploadScripts(session)
	message('Let\'s go on.')

# generate samples and transfer to the server
message('Generating samples for the filter and for the multiplier.')
with isa.cd(s.inputPath):
	genSamples()
	message('Done. Trasferring to the server...')
	uploadSamples(session)
	message('We are working well today!')

# calculate SW output for the generated samples
message('Calculating the SW outputs for the filter.')
with isa.cd(s.cFilterPath):
	compileCfilter()
    message('Running C model on the samples.')
	Cfilter()
	message('Done.')

# upload the common src and tb files
message('Common files will be uploaded now. Look at this!!')
uploadSrcTb(session)
message('And now we can enter the loop... it will take a while, so keep calm.')

# loop
for compressionLevel in s.compressionList:
	for startingDirection in s.directionList:
		
		# create the multiplier
		message('Creating the multiplier with a compression level of {comp}. The binding is begun from {dir}'.format(
			comp=compressionLevel,
			dir=startingDirection))
		with isa.cd(s.multiplierPath):
			generateMultiplier(s.delimiter, s.srcMultPath, s.multBaseName, compressionLevel, startingDirection)
			# transfer the multiplier
			message('Uploading all the multiplier related files...')
			uploadMultiplier(session)
			message('Ok Houston, no problems.')
			# rename the local multiplier
			message('Renaming the multiplier file...')
			newName = '{base_name}.{cmp}{dir}'.format(base_name=s.multBaseName, cmp=compressionLevel, dir=startingDirection)
			os.rename(s.multBaseName, newName)
			message('It was a breeze.')
	
		# sim the mult
		message('Starting the simulation of the mult, baby!')
		performSim(session, s.remote_root, s.mult_sim_tcl_name)
		message('It\'s important to keep these brittle results in a safe place.')
	
		# synth the mult
		message('Starting the synthesis of the mult, baby!')
		performSynth(session, remote_root, s.mult_synth_tcl_name)
		message('Synthesized.')
	
		# generate power, area, timing reports
	
		# sim the synth mult
		message('Starting the simulation of the synth mult, baby!')
		performSim(session, s.remote_root, s.filter_sim_tcl_name)
		message('It\'s important to keep these breakable results in a safe place.')
	
		# sim the filter
		message('Starting the simulation of the synth mult, baby!')
		performSim(session, s.remote_root, s.sMult_sim_tcl_name)
		message('It\'s important to keep these delicate results in a safe place.')
	
		# synth the filter
		message('Starting the synthesis of the filter, baby!')
		performSynth(session, remote_root, s.filter_synth_tcl_name)
		message('Synthesized.')
	
		# generate power, area, timing reports
	
		# sim the synth filter
		message('Starting the simulation of the synth mult, baby!')
		performSim(session, s.remote_root, s.sFilter_sim_tcl_name)
		message('It\'s important to keep these frail results in a safe place.')

		# take back, rename and store the results and reports
		storeResultsReports(session)

		message('Finished a loop step: cleaning common and re-uploading the same Samples')
		# clean the common folder from output files
		cleanCommon(session)
		# re-upload samples
		uploadSamples(session)
		message('Let\'s go on!')

# elaborate the results 