from numpy import size

from src.Lab3.Scheme import SchemeBody
from src.Lab4.Population import PopulationBody
from src.Lab4.ToAnalyze import do_direct_method, is_sustainable
from src.Lab4.ToPlot import plot_trans_func, plot_3d
from src.Lab3.Regulator import ProportionalRegulator, PIDRegulator
from control.matlab import pzmap

"""
Главное тело программы
"""


def genetic_method():
    """
    Функция исполнения метода генетического подбора параметров регулятора
    """

    def target_function(population):
        """
        функция оценки каждой особи популяции
        :param population: популяция особей
        :return: лист оценок
        """
        degree = [0 for i in range(len(population.pop_list))]
        for i in range(len(population.pop_list)):
            # передаточная функция регулятора
            regs_w = population.pop_list[i].get_TrFunc_pid_regulator()
            # объект класса САУ
            grand_gear_function = SchemeBody(regs_w=regs_w)
            # передаточная функция САУ с регулятором
            w = grand_gear_function.get_scheme_solving()
            # оценка регулирования
            degree[i] = sum(do_direct_method(w))

        return degree

    # создание популяции
    group = PopulationBody()
    group.create_new_population()

    # оценка особей популяции
    grades = target_function(group)
    best_of_the_best = []

    while max(grades) <= 34:

        grades = target_function(group)
        if len(best_of_the_best) >= 500:
            break
        # сортировка и отбор лучшей особи
        best_person, deg = group.sort_and_take_best(grades)
        best_of_the_best.append(best_person)
        print("Поколение: ", len(best_of_the_best))
        print("Лист особей: ", grades)
        print("Лучший результат поколения: Оценка-", deg[0],
              "Коэффициенты Кп, Кд, Ки-", best_person.get_regulator_coefficients())

        if len(best_of_the_best) % 10 == 0:  # неудачный вид
            print("Вид получился неудачным! Создадим новый...")
            group.create_new_population()
            continue

        # процесс селекции, мутации и скрещивания
        group.set_pop_list(group.pop_selection()
                           + group.pop_mutation() + group.pop_breeding())

    # вывод лучших особей на график
    Kp = [0 for i in range(len(best_of_the_best))]
    Kd = [0 for i in range(len(best_of_the_best))]
    Ku = [0 for i in range(len(best_of_the_best))]
    for i, regulator in enumerate(best_of_the_best):
        [Kp[i], Kd[i], Ku[i]] = regulator.get_regulator_coefficients()

    plot_3d(Kp, Kd, Ku)


def ZN_Method():
    """
    Функция исполнения метода Зиглера-Николса для подбора параметров регулятора
    :return:
    """

    def is_on_border(poles):
        """
        функция выявляет, есть ли во входящем массиве полюсов такие, которые находятся
        на границе устойчивости
        :param poles: полюса
        :return: true/false
        """

        a = True
        counter = 1

        print("Полюса плоскости: ")
        for pole in poles:
            if -0.001 < pole.real < 0:  # корень в левой полуплоскости
                a = False
            print("Полюс ", counter, " : ", pole)
            counter += 1

        print("Система на границе устойчивости" if not a else
              "По критерию полюсов система устойчива")

        return a

    k = 0
    flag = True
    # создаем объект пропорционального регулятора с начальными параметрами
    regulator = ProportionalRegulator()

    # калибровка регулятора, поиск критического состояния САУ
    while flag:
        regulator.set_regulator_coefficients(k=k)
        # объект класса САУ
        grand_gear_function = SchemeBody(regs_w=regulator.get_TrFunc_proportional_regulator())
        # передаточная функция САУ с регулятором
        w = grand_gear_function.get_scheme_solving()

        poles, zeros = pzmap(w, Plot=False)
        # ПОПРОБОВАТЬ УПРОСТИТЬ ЧЕРЕЗ TRY****************
        if size(poles) > 0:
            # есть ли корень на границе устойчивости
            flag = is_on_border(poles)
        if not flag: break
        k += 0.1

    print("Кп: ", round(k,3))
    # находим период переходной характеристики
    T = plot_trans_func(w, toPlotTrans=True, toFindT=True)
    print("Период колебательной переходной характеристики: ", round(T,6))

    # создаем новый объект ПИД-регулятора
    regulator = PIDRegulator()
    # устанавливаем параметры по методу Зиглера-Николса
    regulator.set_regulator_coefficients(k=0.6 / k, Td=0.5 * T / k, Tu=0.125 * T / k)
    grand_gear_function = SchemeBody(regs_w=regulator.get_TrFunc_pid_regulator())
    # передаточная функция САУ с регулятором
    w = grand_gear_function.get_scheme_solving()

    poles, zeros = pzmap(w, Plot=False)
    if is_sustainable(poles):
        plot_trans_func(w, toPlotTrans=True)
        print("Оценка регулирования составляет: ", sum(do_direct_method(w)))

    else: print("Система неустойчива!")



genetic_method()
