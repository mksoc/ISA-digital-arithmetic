#!/usr/bin/python3
################################################################
# Automatic DADDA binding of a tree and related VHDL generator #
################################################################
# Before executing this program, be aware of the settings in the settings.py file.
###

#----------------------------------------------
# MODULES
#----------------------------------------------
from treeBindings_VHDLgen import wrFA, wrHA, vhdlDaddaLevel, autoBind
import settings as s

#----------------------------------------------
# CONSTANTS and VARIABLES
#----------------------------------------------

fileName = s.fileName
mtxCols = s.mtxCols
numElmArr = s.numElmArr
daddaLevels = s.daddaLevels
daddaRows = [2, 3, 4, 6, 9, 13]

#----------------------------------------------
# PROGRAM
#----------------------------------------------

for currentLevel in range(daddaLevels, 0, -1):

	nextLevel = currentLevel-1

	if (currentLevel < daddaLevels):
		fileMode = "a"
	else:
		fileMode = "w"
	srcMtx = s.mtxName + str(currentLevel)
	dstMtx = s.mtxName + str(nextLevel)
	srcMtxRows = daddaRows[currentLevel]
	dstMtxRows = daddaRows[nextLevel]

	faArr, haArr, nextNumElmArr = autoBind(numElmArr, daddaRows[nextLevel], s.mtxCols)

	vhdlDaddaLevel(fileName, fileMode, srcMtx, dstMtx, srcMtxRows, dstMtxRows, mtxCols, numElmArr, faArr, haArr, nextLevel)
	
	numElmArr = nextNumElmArr
