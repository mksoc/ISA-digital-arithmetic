import shutil
import settings as s
import isa
import os
import subprocess

def removeTree(root):
	if os.path.exists(root):
		shutil.rmtree(root)

def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def cleanServer(session):
	session.clean(s.remote_srcPath)
	session.clean(s.remote_tbPath)
	session.clean(s.remote_simPath)
	session.clean(s.remote_synPath)
	session.clean(s.remote_commonPath)
	session.clean(s.remote_v1Path)
	session.clean(s.remote_v2Path)
	session.clean(s.remote_v3Path)

	cmd = 'cd {synPath}; mkdir netlist'.format(synPath=s.remote_synPath)
	session.run_commands(cmd)

def buildTree():
	mkdir(s.workPath)
	mkdir(s.multiplierPath)
	mkdir(s.inputPath)
	mkdir(s.tmpPath)
	mkdir(s.reportPath)
	mkdir(s.resultPath)
	mkdir(s.scriptPath)

def uploadScripts(session):
	session.copy_to(s.mult_sim_tcl_name, s.remote_simPath)
	session.copy_to(s.filter_sim_tcl_name, s.remote_simPath)
	session.copy_to(s.sMult_sim_tcl_name, s.remote_simPath)
	session.copy_to(s.sFilter_sim_tcl_name, s.remote_simPath)
	session.copy_to(s.mult_synth_tcl_name, s.remote_synPath)
	session.copy_to(s.filter_synth_tcl_name, s.remote_synPath)

def uploadSamples(session):
	session.copy_to(s.multSamples_name, s.remote_commonPath)
	session.copy_to(s.filterSamples_name, s.remote_commonPath)

def uploadSrcTb(session):
	# multiplier related files
	for vhdFile in os.listdir(s.local_srcMult):
		if (vhdFile.endswith('.vhd')):
			if (vhdFile != '{}.vhd'.format(s.multEntity_name)): 
				filePath = '{}/{}'.format(s.local_srcMult, vhdFile)
				session.copy_to(filePath, s.remote_v3Path)

	# project specific files
	for vhdFile in os.listdir(s.local_project):
		if (vhdFile.endswith('.vhd')):
				filePath = '{}/{}'.format(s.local_project, vhdFile)
				session.copy_to(filePath, s.remote_srcPath)

	# generic src files
	for vhdFile in os.listdir(s.local_src):
		if (vhdFile.endswith('.vhd')):
			if (vhdFile != '{}.vhd'.format(s.multEntity_name)): 
				filePath = '{}/{}'.format(s.local_src, vhdFile)
				session.copy_to(filePath, s.remote_srcPath)

	# filter tb files
	for vhd_v_File in os.listdir(s.local_tb):
		if (vhd_v_File.endswith('.vhd') or vhd_v_File.endswith('.v')):
				filePath = '{}/{}'.format(s.local_tb, vhd_v_File)
				session.copy_to(filePath, s.remote_tbPath)

	# mult tb files
	for vhdFile in os.listdir(s.local_tbMult):
		if (vhdFile.endswith('.vhd')):
				filePath = '{}/{}'.format(s.local_tbMult, vhdFile)
				session.copy_to(filePath, s.remote_tbPath)

def uploadMultiplier(session):
	session.copy_to(s.multFileName, s.remote_v3Path)

def uploadMultiplierWRegs(session):
	session.copy_to(s.multWRegsFileName, s.remote_v3Path)

def storeResultsReports(session, synthesized, compressionLevel, startingDirection):
	if synthesized:
		synthString = 'synth'		
		for file in s.reportFilesList:
			oldResultFilePath = '{}/{}'.format(s.remote_commonPath, file)
			resultFilePath = '{}/{}{}{}_{}'.format(s.remote_commonPath, compressionLevel, startingDirection, synthString, file)
			session.run_commands('mv {oldFile} {newFile}'.format(oldFile=oldResultFilePath, newFile=resultFilePath))
			session.copy_from(resultFilePath, s.reportPath)
	else:
		synthString = 'noSynth'

	for file in s.resultFilesList:
		oldResultFilePath = '{}/{}'.format(s.remote_commonPath, file)
		resultFilePath = '{}/{}{}{}_{}'.format(s.remote_commonPath, compressionLevel, startingDirection, synthString, file)
		session.run_commands('mv {oldFile} {newFile}'.format(oldFile=oldResultFilePath, newFile=resultFilePath))
		session.copy_from(resultFilePath, s.resultPath)

def cleanCommon(session):
	session.clean(s.remote_commonPath)
	with isa.cd(s.inputPath):
		for file in os.listdir('./'):
			if (file.endswith('.txt')):
				session.copy_to(file, s.remote_commonPath)

def cleanSyn(session):
	session.clean(s.remote_synPath)