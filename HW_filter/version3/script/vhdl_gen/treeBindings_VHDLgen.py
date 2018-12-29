#!/usr/bin/python3
# script to auto generate VHDL for bindings
import copy
#----------------------------------------------
# VARIABLES - only if it is launched as a script
#----------------------------------------------
# fileName: the name of the file on which we want to produce the VHDL
# fileMode: mode for file opening ("w" or "a")
# srcMtx: string - the name of the source matrix
# dstMtx: string - the name of the destination matrix
# srcMtxRows: number - #rows of the srcMtx
# destMtxRows: number - #rows of the destMtx
# mtxCols: number - #columns of each matrix
# numElmArr: array of numbers with dimension mtxCols - each cell keeps the number of elements in that column
# faArr: array of numbers with dimension mtxCols - each cell keeps the number of FA to be instantiated for that column
# haArr: array of numbers with dimension mtxCols -each cell keeps the number of HA to be instantiated for that column
# daddaLevel: number, only for the welcome comment

#----------------------------------------------
# FUNCTIONs DEFINITIONS
#----------------------------------------------

# fileObj is the file object of the file on which we want to write
# inVector, outVector are the vector signals to be connected with the in/out of the compressor block
# actualColumn: the number of the column
# nCompressor: the index of the current FA
def wr4To2ApproxCompressor(fileObj, i0, i1, i2, i3, out0, out1, actualColumn, nCompressor, daddaLevel):

	entityName = "approx_comp_4to2"

	line = ["-- 4 to 2 lossy compressor c" + str(actualColumn) + ", number " + str(nCompressor) + "\n"]
	line += ["lv" + str(daddaLevel) + "_c" + str(actualColumn) + "_CMPRS_" + str(nCompressor) + ": " + entityName + "\n"]
	line += ["\t" + "port map (" + "\n"]
	line += ["\t\t" + "i0 => " + i0 + "," + "\n"]
	line += ["\t\t" + "i1 => " + i1 + "," + "\n"]
	line += ["\t\t" + "i2 => " + i2 + "," + "\n"]
	line += ["\t\t" + "i3 => " + i3 + "," + "\n"]
	line += ["\t\t" + "out0 => " + out0 + "," + "\n"]
	line += ["\t\t" + "out1 => " + out1 + " );" + "\n"]
	line += ["\n"]

	for i in range(0, 10):
		fileObj.write(line[i])

# fileObj is the file object of the file on which we want to write
# i0 ... co are the signals to be connected with the in/out of the adder block
# actualColumn: the number of the column
# the index of the current FA
def wrFA(fileObj, i0, i1, ci, s, co, actualColumn, nFA, daddaLevel):

	entityName = "fullAdder"

	line = ["-- full adder c" + str(actualColumn) + ", number " + str(nFA) + "\n"]
	line += ["lv" + str(daddaLevel) + "_c" + str(actualColumn) + "_FA_" + str(nFA) + ": " + entityName + "\n"]
	line += ["\t" + "port map (" + "\n"]
	line += ["\t\t" + "i0 => " + i0 + "," + "\n"]
	line += ["\t\t" + "i1 => " + i1 + "," + "\n"]
	line += ["\t\t" + "ci => " + ci + "," + "\n"]
	line += ["\t\t" + "s => " + s + "," + "\n"]
	line += ["\t\t" + "co => " + co + " );" + "\n"]
	line += ["\n"]

	for i in range(0, 9):
		fileObj.write(line[i])

# fileObj is the file object of the file on which we want to write
# i0 ... co are the signals to be connected with the in/out of the adder block
# actualColumn: the number of the column
# the index of the current HA
def wrHA(fileObj, i0, i1, s, co, actualColumn, nHA, daddaLevel):

	entityName = "halfAdder"

	line = ["-- half adder c" + str(actualColumn) + ", number " + str(nHA) + "\n"]
	line += ["lv" + str(daddaLevel) + "_c" + str(actualColumn) + "_HA_" + str(nHA) + ": " + entityName + "\n"]
	line += ["\t" + "port map (" + "\n"]
	line += ["\t\t" + "i0 => " + i0 + "," + "\n"]
	line += ["\t\t" + "i1 => " + i1 + "," + "\n"]
	line += ["\t\t" + "s => " + s + "," + "\n"]
	line += ["\t\t" + "co => " + co + " );" + "\n"]
	line += ["\n"]

	for i in range(0, 8):
		fileObj.write(line[i])

# automatic VHDL generator
def vhdlDaddaLevel(fileName, fileMode, srcMtx, dstMtx, srcMtxRows, dstMtxRows, mtxCols, numElmArr, cmprsArr, faArr, haArr, daddaLevel):

	# open the file
	with open(fileName, fileMode) as fileObj:

		# write the VHDL
		actualCin = 0
		nextCin = 0
		nCompressor = 0
		nFA = 0
		nHA = 0

		# initial comment
		fileObj.write("----------------------------- \n")
		fileObj.write("-- DADDA TREE " + "LEVEL" + str(daddaLevel) + "\n")
		fileObj.write("----------------------------- \n\n")

		for actualColumn in range(0, mtxCols):
		    # comment
			fileObj.write("----------------------------- \n")
			fileObj.write("-- COLUMN " + str(actualColumn) + "\n")
			fileObj.write("----------------------------- \n")
			# write the COMPRESSORS
			for i in range(0, cmprsArr[actualColumn]):
				i0 = srcMtx + "(" + str(4*nCompressor) + ")(" + str(actualColumn) + ")"
				i1 = srcMtx + "(" + str(4*nCompressor+1) + ")(" + str(actualColumn) + ")"
				i2 = srcMtx + "(" + str(4*nCompressor+2) + ")(" + str(actualColumn) + ")"
				i3 = srcMtx + "(" + str(4*nCompressor+3) + ")(" + str(actualColumn) + ")"
				out0 = dstMtx + "(" + str(nextCin+actualCin) + ")(" + str(actualColumn) + ")"
				if actualColumn != mtxCols-1:
					out1 = dstMtx + "(" + str(nextCin) + ")(" + str(actualColumn+1) + ")"
				else:
					out1 = "open"
				wr4To2ApproxCompressor(fileObj, i0, i1, i2, i3, out0, out1, actualColumn, nCompressor, daddaLevel);
				nCompressor += 1
				nextCin += 1
			# write the FAs
			for i in range(0, faArr[actualColumn]):
				i0 = srcMtx + "(" + str(3*nFA) + ")(" + str(actualColumn) + ")"
				i1 = srcMtx + "(" + str(3*nFA+1) + ")(" + str(actualColumn) + ")"
				ci = srcMtx + "(" + str(3*nFA+2) + ")(" + str(actualColumn) + ")"
				s = dstMtx + "(" + str(nextCin+actualCin) + ")(" + str(actualColumn) + ")"
				if actualColumn != mtxCols-1:
					co = dstMtx + "(" + str(nextCin) + ")(" + str(actualColumn+1) + ")"
				else:
					co = "open"
				wrFA(fileObj, i0, i1, ci, s, co, actualColumn, nFA, daddaLevel);
				nFA += 1
				nextCin += 1
			# write the HAs
			for i in range(0, haArr[actualColumn]):
				i0 = srcMtx + "(" + str(3*nFA+2*nHA) + ")(" + str(actualColumn) + ")"
				i1 = srcMtx + "(" + str(3*nFA+2*nHA+1) + ")(" + str(actualColumn) + ")"
				s = dstMtx + "(" + str(nextCin+actualCin) + ")(" + str(actualColumn) + ")"
				if actualColumn != mtxCols-1:
					co = dstMtx + "(" + str(nextCin) + ")(" + str(actualColumn+1) + ")"
				else:
					co = "open"
				wrHA(fileObj, i0, i1, s, co, actualColumn, nHA, daddaLevel);
				nHA += 1
				nextCin += 1
			# move the other elements of the column
			fileObj.write("-- move the other elements of the column\n")
			offset = nextCin + actualCin
			for i in range(4*nCompressor+3*nFA+2*nHA, numElmArr[actualColumn]):
				line = dstMtx + "(" + str(offset) + ")(" + str(actualColumn) + ") <= " + srcMtx + "(" + str(i) + ")(" + str(actualColumn) + ");"
				fileObj.write(line)
				fileObj.write("\n")
				offset += 1;
			# if we are in the level 0, we have to check that the two rows are full. If something is missing it means that
			# it was already missing at the top level (it means that there was a '0' in that position)
			if (daddaLevel == 0):
				if (numElmArr[actualColumn] == 0):
					fileObj.write("\n")
					fileObj.write("-- fix missing assignments in the last level \n")
					for i in range(2):
						line = dstMtx + "(" + str(i) + ")(" + str(actualColumn) + ") <= " + "'0';"
						fileObj.write(line)
					fileObj.write("\n")
				else:
					if (numElmArr[actualColumn] == 1):
						fileObj.write("\n")
						fileObj.write("-- fix missing assignments in the last level \n")
						line = dstMtx + "(" + str(1) + ")(" + str(actualColumn) + ") <= " + "'0';"
						fileObj.write(line)
						fileObj.write("\n")
			fileObj.write("\n")

			actualCin = nextCin
			nextCin = 0
			nCompressor = 0
			nFA = 0
			nHA = 0

# autoBind function
# provide an automatic binding for COMPRESSORS, FA and HA for each column of the tree, given a target maximum number of rows to be obtained
#
# INPUT #
# numElmArr: each cell of this list keeps the number of elements of the current column (wrt the current level)
# nextMaxRows: maximum number of elements allowed per column in the next level
# mtxCols: number of column of the matrix. It must be equal to len(numElmArr)
# compression: percentage of how many compressors will be bound wrt the maximum possible respecting the DADDA approach
# startingDirection: can be either "right" or "left" and determines the starting direction from where the compressors are bound.

def autoBind(numElmArr, nextMaxRows, mtxCols, compression, startingDirection):
	if (len(numElmArr) != mtxCols):
		print("Error in autoBind(numElmArr, nextMaxRows, mtxCols): len(numElmArr) != mtxCols")
		return None # error!

	nCompressorMax = 0
	cmprsArr = [0] * mtxCols
	faArr = [0] * mtxCols
	haArr = [0] * mtxCols

	nextNumElmArr = copy.deepcopy(numElmArr)
	checkNumElmArr = copy.deepcopy(numElmArr) # be sure not to assign adders where there are not enough elements

	# compute the maximum number of compressors for this level
	for actualColumn in range(mtxCols):
		while (nextNumElmArr[actualColumn] >= nextMaxRows+3 and checkNumElmArr[actualColumn] >= 4):
			nextNumElmArr[actualColumn] -= 3
			checkNumElmArr[actualColumn] -= 4
			nCompressorMax += 1 # +++++++++++++++++ COMPRESSORs COUNTING +++++++++++++++++++
			if (actualColumn < mtxCols-1):
				nextNumElmArr[actualColumn+1] += 1
		while (nextNumElmArr[actualColumn] >= nextMaxRows+2 and checkNumElmArr[actualColumn] >= 3):
			nextNumElmArr[actualColumn] -= 2
			checkNumElmArr[actualColumn] -= 3
			if (actualColumn < mtxCols-1):
				nextNumElmArr[actualColumn+1] += 1
		while (nextNumElmArr[actualColumn] >= nextMaxRows+1 and checkNumElmArr[actualColumn] >= 2):
			nextNumElmArr[actualColumn] -= 1
			checkNumElmArr[actualColumn] -= 2
			if (actualColumn < mtxCols-1):
					nextNumElmArr[actualColumn+1] += 1

	# restore the lists
	nextNumElmArr = copy.deepcopy(numElmArr)
	checkNumElmArr = copy.deepcopy(numElmArr)

	# compute how many approx compressors will be put
	nCompressor = round(compression/100 * nCompressorMax)

	# bind
	for actualColumn in range(mtxCols):
		while (nextNumElmArr[actualColumn] >= nextMaxRows+3 and checkNumElmArr[actualColumn] >= 4 and nCompressor > 0):
			nextNumElmArr[actualColumn] -= 3
			checkNumElmArr[actualColumn] -= 4
			cmprsArr[actualColumn] += 1
			if (startingDirection == 'right'): nCompressor -= 1 # final bind if startingDirection = 'right', else bind with compression = 0% and than go on to the next if
			if (actualColumn < mtxCols-1):
				nextNumElmArr[actualColumn+1] += 1
		while (nextNumElmArr[actualColumn] >= nextMaxRows+2 and checkNumElmArr[actualColumn] >= 3):
			nextNumElmArr[actualColumn] -= 2
			checkNumElmArr[actualColumn] -= 3
			faArr[actualColumn] += 1
			if (actualColumn < mtxCols-1):
				nextNumElmArr[actualColumn+1] += 1
		while (nextNumElmArr[actualColumn] >= nextMaxRows+1 and checkNumElmArr[actualColumn] >= 2):
			nextNumElmArr[actualColumn] -= 1
			checkNumElmArr[actualColumn] -= 2
			haArr[actualColumn] += 1
			if (actualColumn < mtxCols-1):
					nextNumElmArr[actualColumn+1] += 1

	if (startingDirection == 'left'):
		# deleting the compressors from right to left to keep only the ones related to the MSBs
		for actualColumn in range(mtxCols):
			while (cmprsArr[actualColumn] > 0 and nCompressor < nCompressorMax):
				nextNumElmArr[actualColumn] += 3
				checkNumElmArr[actualColumn] += 4
				cmprsArr[actualColumn] -= 1
				nCompressor += 1
				if (actualColumn < mtxCols-1):
					nextNumElmArr[actualColumn+1] -= 1

		# bind with the FAs and with the HAs
		for actualColumn in range(mtxCols):
			while (nextNumElmArr[actualColumn] >= nextMaxRows+2 and checkNumElmArr[actualColumn] >= 3):
				nextNumElmArr[actualColumn] -= 2
				checkNumElmArr[actualColumn] -= 3
				faArr[actualColumn] += 1
				if (actualColumn < mtxCols-1):
					nextNumElmArr[actualColumn+1] += 1
			while (nextNumElmArr[actualColumn] >= nextMaxRows+1 and checkNumElmArr[actualColumn] >= 2):
				nextNumElmArr[actualColumn] -= 1
				checkNumElmArr[actualColumn] -= 2
				haArr[actualColumn] += 1
				if (actualColumn < mtxCols-1):
						nextNumElmArr[actualColumn+1] += 1

	elif (startingDirection != 'right'): print('Error in autoBind() function: the given startingDirection is neither right nor left, can\'t bind the tree.')

	return cmprsArr, faArr, haArr, nextNumElmArr

# routine to draw the tree
def drawTree(mtxRows, mtxCols, numElmArr, cmprsArr, faArr, haArr):
	numElmArr_drawCopy = copy.deepcopy(numElmArr)
	cmprsArr_drawCopy = [i * 4 for i in copy.deepcopy(cmprsArr)]
	faArr_drawCopy = [i * 3 for i in copy.deepcopy(faArr)]
	haArr_drawCopy = [i * 2 for i in copy.deepcopy(haArr)]

	line = '\n'
	drawLine(line)
	for i in range(0, mtxRows):
		line = ''
		for j in range(0, mtxCols):
			if (numElmArr_drawCopy[j] > 0):
				if (cmprsArr_drawCopy[j] > 0):
					line += 'c'
					cmprsArr_drawCopy[j] -= 1
				elif (faArr_drawCopy[j] > 0):
					line += 'f'
					faArr_drawCopy[j] -= 1
				elif (haArr_drawCopy[j] > 0):
					line += 'h'
					haArr_drawCopy[j] -= 1
				else:
					line += 'o'
				numElmArr_drawCopy[j] -= 1
			else:
				line += ' '
		line = line[::-1]
		drawLine(line)
	line = '\n'
	drawLine(line)

# draw the line
def drawLine(line):
	print(line)

# set numElmArr
def setNumElmArr(startElm,maxElm,endElm,dummyCol):
	numElmArr = []
	for i in range(startElm, maxElm+1):
		numElmArr += [i]
		numElmArr += [i-1]
	numElmArr += [maxElm-1] * 3
	numElmArr += [maxElm-2]
	for i in range(0, (maxElm-endElm-3)+1):
		numElmArr += [maxElm-3-i] * 2
	for i in range(0,dummyCol):
		numElmArr[i]=0
	return numElmArr
