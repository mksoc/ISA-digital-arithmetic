from shutil import copyfile
from in_gen import in_gen
from samples_generator import gen_samples

def removeTree(root):
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

def buildTree():
	mkdir(s.workPath)
	mkdir(s.multiplierPath)
	mkdir(s.inputPath)
	mkdir(s.tmpPath)
	mkdir(s.reportPath)
	mkdir(s.resultPath)

def uploadScripts(session):
	session.copy_to(s.mult_tcl_name, s.remote_simPath)
	session.copy_to(s.filter_tcl_name, s.remote_simPath)
	session.copy_to(s.sMult_tcl_name, s.remote_simPath)
	session.copy_to(s.sFilter_tcl_name, s.remote_simPath)
	session.copy_to(s.mult_synth_tcl_name, s.remote_synPath)
	session.copy_to(s.filter_synth_tcl_name, s.remote_synPath)
	session.copy_to(s.report_tcl_name, s.remote_synPath)

def uploadSamples(session):
	samplesPath = '{}/{}'.format(s.inputPath, s.multSamples_name)
	session.copy_to(samplesPath, s.remote_commonPath)
	samplesPath = '{}/{}'.format(s.inputPath, s.filterSamples_name)
	session.copy_to(samplesPath, s.remote_commonPath)

def uploadSrcTb(session):
	# multiplier related files
	for vhdFile in os.listdir(s.local_srcMult)
		if (vhdFile.endswith('.vhd')):
			if (vhdFile != '{}.vhd'.format(s.multBaseName)): 
				filePath = '{}/{}'.format(s.local_srcMult, vhdFile)
				session.copy_to(filePath, remote_v3Path)

	# project specific files
	for vhdFile in os.listdir(s.local_project)
		if (vhdFile.endswith('.vhd')):
				filePath = '{}/{}'.format(s.local_project, vhdFile)
				session.copy_to(filePath, remote_srcPath)

	# generic src files
	for vhdFile in os.listdir(s.local_src)
		if (vhdFile.endswith('.vhd')):
			if (vhdFile != '{}.vhd'.format(s.multBaseName)): 
				filePath = '{}/{}'.format(s.local_srcMult, vhdFile)
				session.copy_to(filePath, remote_srcPath)

	# filter tb files
	for vhdFile in os.listdir(s.local_tb)
		if (vhdFile.endswith('.vhd')):
				filePath = '{}/{}'.format(s.local_tbMult, vhdFile)
				session.copy_to(filePath, remote_tbPath)

	# mult tb files
	for vhdFile in os.listdir(s.local_tbMult)
		if (vhdFile.endswith('.vhd')):
				filePath = '{}/{}'.format(s.local_tbMult, vhdFile)
				session.copy_to(filePath, remote_tbPath)

def uploadMultiplier(session):
	session.copy_to(s.multBaseName, remote_srcPath)

def storeResultsReports(session, compressionLevel, startingDirection):
	for file in s.resultFilesList:
		oldResultFilePath = '{}/{}'.format(s.remote_commonPath, file)
		resultFilePath = '{}/{}{}_{}'.format(s.remote_commonPath, compressionLevel, startingDirection, file)
		isa.run_commands('mv {oldFile} {newFile}'.format())
		session.copy_from(resultFilePath, s.resultPath)
	for file in s.reportFilesList:
		oldResultFilePath = '{}/{}'.format(s.remote_commonPath, file)
		resultFilePath = '{}/{}{}_{}'.format(s.remote_commonPath, compressionLevel, startingDirection, file)
		isa.run_commands('mv {oldFile} {newFile}'.format())
		session.copy_from(resultFilePath, s.reportPath)

def cleanCommon(session):
	session.clean(s.remote_commonPath)
	with isa.cd(s.inputPath)
		for file in listdir('./')
			if (file.endswith('.txt'))
				session.copy_to(file, s.remote_commonPath)

def cleanSyn(session):
	session.clean(remote_synPath)