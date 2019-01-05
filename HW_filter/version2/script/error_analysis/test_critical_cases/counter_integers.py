
fpointer=open("tempFile1","r")
i=0
j=0

for line in fpointer:
    num=float(line)
    if abs(num)>1:
        i+=1
fpointer.close()
fpointer=open("tempFile1","r")
for line in fpointer:
    num=float(line)
    if num<0:
        j+=1
fpointer.close()
print(i)
print(j)
