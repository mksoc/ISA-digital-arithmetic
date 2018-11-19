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
#
# fileName = "./vhdlOut.vhd"
# fileMode = "w"
# srcMtx = "grid5"
# dstMtx = "grid4"
# srcMtxRows = 13
# dstMtxRows = 9
# mtxCols = 46
# numElmArr = [12] * 46  
# faArr = [2] * 46
# haArr = [1] * 46
# daddaLevel = 1

#----------------------------------------------
# FUNCTIONs DEFINITIONS
#----------------------------------------------

# fileObj is the file object of the file on which we want to write
# i0 ... co are the signals to be connected with the in/out of the adder block
# actualColumn: the number of the column
# the index of the current FA
def wrFA(fileObj, i0, i1, ci, s, co, actualColumn, nFA):

	entityName = "fullAdder"

	line = ["-- full adder c" + str(actualColumn) + ", number " + str(nFA) + "\n"]
	line += ["c" + str(actualColumn) + "_FA_" + str(nFA) + ": " + entityName + "\n"]
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
def wrHA(fileObj, i0, i1, s, co, actualColumn, nHA):

	entityName = "halfAdder"

	line = ["-- half adder c" + str(actualColumn) + ", number " + str(nHA) + "\n"]
	line += ["c" + str(actualColumn) + "_HA_" + str(nHA) + ": " + entityName + "\n"]
	line += ["\t" + "port map (" + "\n"]
	line += ["\t\t" + "i0 => " + i0 + "," + "\n"]
	line += ["\t\t" + "i1 => " + i1 + "," + "\n"]
	line += ["\t\t" + "s => " + s + "," + "\n"]
	line += ["\t\t" + "co => " + co + " );" + "\n"]
	line += ["\n"]

	for i in range(0, 8):
		fileObj.write(line[i])

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
			co = dstMtx + "(" + str(nextCin) + ")(" + str(actualColumn+1) + ")" 
			wrFA(fileObj, i0, i1, ci, s, co, actualColumn, nFA);
			nFA += 1
			nextCin += 1
		# write the HAs
		for i in range(0, haArr[actualColumn]):
			i0 = srcMtx + "(" + str(3*nFA+2*nHA) + ")(" + str(actualColumn) + ")" 
			i1 = srcMtx + "(" + str(3*nFA+2*nHA+1) + ")(" + str(actualColumn) + ")" 
			s = dstMtx + "(" + str(nextCin+actualCin) + ")(" + str(actualColumn) + ")" 
			co = dstMtx + "(" + str(nextCin) + ")(" + str(actualColumn+1) + ")" 
			wrHA(fileObj, i0, i1, s, co, actualColumn, nHA);
			nHA += 1
			nextCin += 1
		# move the other elements of the column
		fileObj.write("-- move the other elements of the column\n")
		fileObj.write("")
		offset = nextCin + actualCin
		for i in range(3*nFA+2*nHA, numElmArr[actualColumn]):
			line = dstMtx + "(" + str(offset) + ")(" + str(actualColumn) + ") <= " + srcMtx + "(" + str(i) + ")(" + str(actualColumn) + ");" 
			fileObj.write(line)
			fileObj.write("\n")
			offset += 1;

		fileObj.write("\n")

		actualCin = nextCin
		nextCin = 0
		nFA = 0
		nHA = 0
