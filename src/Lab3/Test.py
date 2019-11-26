from xmlrpc.client import boolean

from numpy.ma import mean

from src.Lab3.Function_analyzing_tools import My_function
from src.Lab3.Regulator import Regulatorr
from src.Lab3.Initial_parameters import Initialazer

boop = True

# initos = [20, 14, 5, 7, 1, 5]

b = Regulatorr()
c = Initialazer(regs=b.Prop_reg())
a = My_function(w_f=c.get_scheme_solving())

keys = [0 for i in range(10)]
Ks = [1 for i in range(len(keys))]
step =[1 for i in range(len(keys))]

# print(c)
#
# actual_keys = a.full_analyze()
# print(actual_keys)
# print(keys)

while boop:

    print(c)

    actual_keys = a.full_analyze()

    countt = 0
    for i in range(len(keys)):



        if actual_keys[i] != 0:
            if actual_keys[i] > keys[i]:
                step[i] = abs(step[i]/2)
                keys[i] = actual_keys[i]

            elif actual_keys[i] < keys[i]:
                step[i] /= -2
                keys[i] = actual_keys[i]

            elif actual_keys[i] == keys[i]:
                keys[i] = actual_keys[i]

            Ks[i] += step[i]
        else:
            countt +=1

    if countt == len(keys) :
        boop = False


    k = mean(Ks[0:7])
    Td = -mean(Ks[8:9])
    Tu = mean(Ks[8:9])

    b = Regulatorr(k, Td, Tu)
    print(b)
    c = Initialazer(regs=b.PUD_reg())

    a = My_function(w_f=c.get_scheme_solving())
