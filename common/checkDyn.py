#!/usr/bin/python3

# scripts to check results of the multiplier and clean SW and HW result files from data which can't be represented on 22 bits
# this is necessary because our multiplier can take in input only one generic Q2.22 and a (Q1.22 less than 1)

import os

outFilePath = 'checkBeforeCleaning.log'
outFilePath2 = 'checkAfterCleaning.log'

cleanedFolder = './cleaned'

txtSWFilesList = [i for i in os.listdir() if i.endswith("mult_SW-output.txt")]
txtSWFilesList.sort()
txtHWFilesLis = [i for i in os.listdir() if i.endswith("mult_HW-output.txt")]
txtHWFilesLis.sort()

# firts dyn check and log
with open(outFilePath, 'w') as fOut:
	for swFile in txtSWFilesList:
		with open(swFile, 'r') as fIn:
			print(swFile + " in elaboration...")
			for line in fIn:
				if(line[0] == line[1] == line[2]):
					pass
				else:
					fOut.write(swFile + ": dynamic error!\n")

# create the folder for cleaned files
if (os.path.isdir(cleanedFolder)):
	pass
else:
	os.mkdir(cleanedFolder)

# clean the files
for swFile, hwFile in zip(txtSWFilesList, txtHWFilesLis):
	with open(swFile, 'r') as fSW, open(hwFile, 'r') as fHW, open(cleanedFolder+'/'+swFile, 'w') as cfSW, open(cleanedFolder+'/'+hwFile, 'w') as cfHW:
		for swLine, hwLine in zip(fSW, fHW):
			if (swLine[0] == swLine[1] == swLine[2]):
				cfSW.write(swLine)
				cfHW.write(hwLine)

# move to the cleaned files folder
os.chdir(cleanedFolder)

# second dyn check and log
with open(outFilePath2, 'w') as fOut:
	for swFile in txtSWFilesList:
		with open(swFile, 'r') as fIn:
			print(swFile + " in elaboration...")
			for line in fIn:
				if(line[0] == line[1] == line[2]):
					pass
				else:
					fOut.write(swFile + ": dynamic error!\n")