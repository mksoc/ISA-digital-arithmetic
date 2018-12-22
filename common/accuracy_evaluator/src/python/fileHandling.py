from shutil import copyfile

def renameFile(oldFilePath, newFilePath):
	exists = os.path.isfile(newFilePath)
	if exists:
		sys.exit("An error occured while renaming or moving a file, because the new file already exists.")
	else:
		os.rename(oldFilePath, newFilePath)

def moveFile(srcFilePath, destFolder):
	fileName = extractFileName(srcFilePath)
	newFilePath = destFolder + fileName
	renameFile(srcFilePath, newFilePath)

def copyFile(srcFilePath, destFolder):
	copyfile

def extractFileName(filePath):
	i = 0
	while(filePath[i] == "/"):
		i -= 1
		filePath = filePath[:i]
	fileName = os.path.basename(filePath)
	while(i < 0):
		i += 1
		fileName = fileName + "/"
	return fileName

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

def uploadSamples(session):
	samplesPath = '{}/{}'.format(s.inputPath, s.multSamples_name)
	session.copy_to(samplesPath, s.remote_commonPath)
	samplesPath = '{}/{}'.format(s.inputPath, s.filterSamples_name)
	session.copy_to(samplesPath, s.remote_commonPath)

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
        resultPath=resultPath, 
        resultFile=s.c_resultFile_name))

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

def storeResultsReports(session):
	for file in s.resultFilesList:
		resultFilePath = '{}/{}'.format(s.remote_commonPath, file)
		session.copy_from(resultFilePath, s.resultPath)
	for file in s.reportFilesList:
		reportFilePath = '{}/{}'.format(s.remote_commonPath, file)
		session.copy_from(resultFilePath, s.reportPath)

def cleanCommon(session):
	session.clean(s.remote_commonPath)
	with isa.cd()