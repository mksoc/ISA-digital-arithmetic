#######################################
# SETTINGS for wrDaddaTree.py program #
#######################################
# daddaLevels: the number of transformations required to reduce to 2 the number of rows (last level, just before the final 
############## addition)
# numElmArr: list in which each cell keeps the number of elements of the relative column of the tree
############
# mtxName: the VHDL root name of each matrix (it will be added an index at the end of the word)  
##########
# srcMtxRows: the maximum number of rows of the source matrix (max level)
#############
# mtxCols: the number of columns of the tree
##########
# approxCovering: percentage of columns which can be processed with the approx compressors (from 0 to 100 included)
#################
# startApprox: if approxCovering != 100 and approxCovering != 0, it sets the direction from which the approx is done 
# (can be "left" or "right"). For example: if only one column is interested in the approximation, it will be the 
# first from left or from right
##############

fileName = "./autoGeneratedDaddaTree.vhd"

daddaLevels = 5

mtxName = "grid"
srcMtxRows = 13
mtxCols = 46

numElmArr = []
for i in range(2, 14):
	numElmArr += [i]
	numElmArr += [i-1]
numElmArr += [12] * 3
numElmArr += [11]
for i in range(0, 9):
	numElmArr += [10-i] * 2

approxCovering = 100

startApprox = "right"