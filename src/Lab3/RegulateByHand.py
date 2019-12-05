from src.Lab3.Analyzer import RegulatorAnalyzer
from src.Lab3.Regulator import PIDRegulator, ProportionalRegulator
from src.Lab3.Scheme import SchemeBody


def regulator_customization():
    """
    main analyzing function
    """

    boop = True
    actual_keys = []
    regs_w = 0
    p_regulator = ProportionalRegulator()
    pid_regulator = PIDRegulator()

    # начальные значения коэффициентов
    k, Td, Tu = 1, 1, 1
    """
    Ввести PID или Prop в зависимости от желаемого исследования
    Для пропорционального регулятора оптимально: Kп = 0.1
    Для ПИД- регулятора: Kп = 1, Кд = 3, Ки = 3
    """
    Reg_type = "PID"

    while boop:

        if Reg_type == "PID":

            print("k = ", k, " Td = ", Td, "Tu = ", Tu)
            k = float(input("\nВведите коэфф k: "))
            Td = float(input("Введите коэфф Td: "))
            Tu = float(input("Введите коэфф Tu: "))

            pid_regulator.set_regs(k, Td, Tu)
            regs_w = pid_regulator.PID_reg()

        elif Reg_type == "Prop":

            print("k = ", k)
            k = float(input("\nВведите коэфф k: "))

            p_regulator.set_regs(k)
            regs_w = p_regulator.Prop_reg()


        grand_gear_function = SchemeBody(regs_w=regs_w)

        analyzer = RegulatorAnalyzer(w_f=grand_gear_function)

        actual_keys.append(analyzer.full_analyze())

        for key in actual_keys:
            print(key)


regulator_customization()
