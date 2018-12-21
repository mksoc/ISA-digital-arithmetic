
from operator import xor

def twos_comp(value, bits):
    if (value & (1<<(bits-1))) != 0:
        value=value - (1<<bits)
    return value

def FH(A,B,C):
    propagate=xor(A,B)
    sum=xor(propagate,C)
    carry=((A and B) or (C and propagate))
    res=str(sum)+str(carry)
    return res

def printer_2s(value,bits):
    if value>=0:
        sign_flag=True
        string=format(value,'b')
    else:
        sign_flag=False
        temp=format(value,'b')
        i=len(temp)-1
        inv=""
        while i>0:
            if (temp[i]=='1'):
                inv='0'+inv
            else:
                inv='1'+inv
            i-=1
        if len(inv)<bits:
            inv='1'+inv
        out=FH(int(inv[len(inv)-1]),0,1)
        string=""
        string=out[0]+string
        for bit in range(len(inv)-2,0,-1):
            out=FH(int(inv[bit]),0,int(out[1]))
            string=out[0]+string
        if out[1]=='1':
            string=out[1]+string
    while len(string)<bits:
        if sign_flag:
            string='0'+string
        else:
            string='1'+string
    return string