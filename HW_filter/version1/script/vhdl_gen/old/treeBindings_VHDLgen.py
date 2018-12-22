#!/usr/bin/python3
# script to auto generate VHDL for bindings

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
def vhdlDaddaLevel(fileName, fileMode, srcMtx, dstMtx, srcMtxRows, dstMtxRows, mtxCols, numElmArr, faArr, haArr, daddaLevel):

	# open the file
	fileObj = open(fileName, fileMode)

	# write the VHDL
	actualCin = 0;
	nextCin = 0;
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
		for i in range(3*nFA+2*nHA, numElmArr[actualColumn]):
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
		nFA = 0
		nHA = 0

# autoBind function
# provide an automatic binding for FA and HA for each column of the tree, given a target maximum number of rows to be obtained
#
# INPUT #
# numElmArr: each cell of this list keeps the number of elements of the current column (wrt the current level)
# nextMaxRows: maximum number of elements allowed per column in the next level 
# mtxCols: number of column of the matrix. It must be equal to len(numElmArr)
#
def autoBind(numElmArr, nextMaxRows, mtxCols):

	import copy

	if (len(numElmArr) != mtxCols):
		print("Error in autoBind(numElmArr, nextMaxRows, mtxCols): len(numElmArr) != mtxCols")
		return None # error!

	faArr = [0] * mtxCols
	haArr = [0] * mtxCols

	nextNumElmArr = copy.deepcopy(numElmArr)
	checkNumElmArr = copy.deepcopy(numElmArr) # be sure not to assign adders where there are not enough elements

	for actualColumn in range(mtxCols):
		while nextNumElmArr[actualColumn] > nextMaxRows+1 and checkNumElmArr[actualColumn] >= 3:
			if (nextNumElmArr[actualColumn] >= nextMaxRows+2):
				nextNumElmArr[actualColumn] -= 2
				checkNumElmArr[actualColumn] -= 3
				faArr[actualColumn] += 1
				if (actualColumn < mtxCols-1):
					nextNumElmArr[actualColumn+1] += 1
		if (nextNumElmArr[actualColumn] == nextMaxRows+1  and checkNumElmArr[actualColumn] >= 2):
			nextNumElmArr[actualColumn] -= 1
			checkNumElmArr[actualColumn] -= 2
			haArr[actualColumn] += 1
			if (actualColumn < mtxCols-1):
					nextNumElmArr[actualColumn+1] += 1

	return faArr, haArr, nextNumElmArr