from src.Lab3.Function_analyzing_tools import Regulator_analyzer
from src.Lab3.Regulator import Regulator_body
from src.Lab3.Initial_parameters import Initialazer

def regulator_customization():

    boop = True

    regulator = Regulator_body()
    grand_gear_function = Initialazer(regs=regulator.Prop_reg())
    analyzer = Regulator_analyzer(w_f=grand_gear_function.get_scheme_solving())
    actual_keys = []
    k, Td, Tu = 1, 1, 1

    while boop:

        actual_keys.append(analyzer.full_analyze())
        # actual_keys = a.full_analyze()

        print("k = ", k, " Td = ", Td, "Tu = ", Tu)

        for i in range(len(actual_keys)):
            print(actual_keys[i])

        k = float(input("\nВведите коэфф k: "))
        Td = float(input("Введите коэфф Td: "))
        Tu = float(input("Введите коэфф Tu: "))

        regulator = Regulator_body(k, Td, Tu)
        print(regulator)
        # c = Initialazer(regs = b)
        grand_gear_function = Initialazer(regs=regulator.PUD_reg())
        # c = Initialazer(regs=b).get_scheme_solving()

        analyzer = Regulator_analyzer(w_f=grand_gear_function.get_scheme_solving())

        # cc = c.get_scheme_solving()
        # print(cc)
        # 0 0 1

        # boop = input("1 или 0: ")


regulator_customization()