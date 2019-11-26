from xmlrpc.client import boolean

from src.Lab3.Function_analyzing_tools import My_function
from src.Lab3.Regulator import Regulatorr
from src.Lab3.Initial_parameters import Initialazer

boop = True

# initos = [20, 14, 5, 7, 1, 5]

b = Regulatorr()
c = Initialazer(regs=b.Prop_reg())
a = My_function(w_f = c.get_scheme_solving())

while boop == True:

    print(c)

    a.full_analyze()

    k = float(input("Введите коэфф k: "))
    Td = float(input("Введите коэфф Td: "))
    Tu = float(input("Введите коэфф Tu: "))

    b = Regulatorr(k, Td, Tu)
    print(b)
    # c = Initialazer(regs = b)
    c = Initialazer(regs=b.PUD_reg())
    # c = Initialazer(regs=b).get_scheme_solving()

    a = My_function(w_f=c.get_scheme_solving())

    # cc = c.get_scheme_solving()
    # print(cc)


    # boop = input("1 или 0: ")
