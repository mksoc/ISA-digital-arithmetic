import random

fileName = "./fileIn.txt"
howManyNums = 10000
nBit = 24

def num2bin(num, nBit):

	binNum = []

	for exp in range(nBit-1, -1, -1):
		quot = num / 2**(exp)
		if quot >= 1:
			num = num % 2**(exp)
			binNum += ['1']
		else:
			binNum += ['0']
	return ''.join(binNum)

# open the file
fileIn = open(fileName, "w")

for randNum in range(howManyNums):
	xDec = random.randint(0, 2**(nBit)-1) # for debug
	yDec = random.randint(0, 2**(nBit)-1) # for debug
	x = num2bin(xDec, nBit)
	y = num2bin(yDec, nBit)
	line = x + " " + y
	fileIn.write(line + "\n")
