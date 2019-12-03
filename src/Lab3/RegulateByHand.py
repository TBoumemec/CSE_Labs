from src.Lab3.Analyzer import Regulator_analyzer
from src.Lab3.Regulator import Regulator_body
from src.Lab3.Scheme import Scheme_body


def regulator_customization():
    """
    main function
    :return:
    """

    boop = True
    actual_keys = []
    k, Td, Tu = 1, 1, 1
    Reg_type = "Prop"
    regulator = Regulator_body()
    regs_w = 0

    while boop:

        if Reg_type == "PID":

            print("k = ", k, " Td = ", Td, "Tu = ", Tu)
            k = float(input("\nВведите коэфф k: "))
            Td = float(input("Введите коэфф Td: "))
            Tu = float(input("Введите коэфф Tu: "))

            regulator.set_regs(k, Td, Tu)
            regs_w = regulator.PID_reg()

        elif Reg_type == "Prop":

            print("k = ", k)
            k = float(input("\nВведите коэфф k: "))

            regulator.set_regs(k)
            regs_w = regulator.Prop_reg()

        print(regulator)

        grand_gear_function = Scheme_body(regs_w=regs_w)

        analyzer = Regulator_analyzer(w_f=grand_gear_function)

        actual_keys.append(analyzer.get_trans_func())

        for key in actual_keys:
            print(key)


regulator_customization()
