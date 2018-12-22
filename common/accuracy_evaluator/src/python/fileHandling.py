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