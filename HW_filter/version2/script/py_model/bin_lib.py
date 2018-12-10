def twos_comp(value, bits):
    if (value & (1<<(bits-1))) != 0:
        value=value - (1<<bits)
    return value

def printer_2s(value,bits):
    if value>=0:
        string=format(value,'b')
        if len(string)<=bits:
            sign_ext=bits-len(string)
            return ('0'*sign_ext+string)
        else:
            return string
    else:
        value=value + (1<<len(bin(value))-3)
        string=format(value,'b')
        if len(string)<=bits:
            sign_ext=bits-len(string)
            return (string[0]*sign_ext+string)
        else:
            return string
