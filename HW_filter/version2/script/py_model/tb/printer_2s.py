import sys
sys.path.insert(0, '../')
from bin_lib import twos_comp,printer_2s
for num in range(-2564,15,1):
    string=(printer_2s(num,12))
    print(twos_comp(int(string,2),len(string)))
