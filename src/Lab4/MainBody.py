from numpy import size
from src.Lab3.Scheme import SchemeBody
from src.Lab4.Population import PopulationBody
from src.Lab4.ToAnalyze import do_direct_method, is_sustainable
from src.Lab4.ToPlot import plot_trans_func, plot_3d
from src.Lab3.Regulator import ProportionalRegulator, PIDRegulator
from control.matlab import pzmap
from control.matlab import step
from control import *

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
    best_of_the_best = []

    while len(best_of_the_best) < 2000:

        grades = target_function(group)
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

    def second_var():
        """
        Второй способ релизации метода Зиглера-Никольса
        :return: время западнывания tet, постоянную времени T и коэффициент передачи k
        """
        # получает передаточную функцию объекта управления
        w = SchemeBody().get_scheme_solving()

        t = np.linspace(0, stop=100, num=2000)

        y1, t1 = step(w, t)

        y1 = list(y1)
        max_dif = 0
        # номер элемента в списке, имеющего максимальную разницу с предыдущим
        nmd = 0

        for num, yy in enumerate(y1[1:]):
            if (yy - y1[num]) > max_dif:
                max_dif, nmd = (yy - y1[num]), (num + 1)
                if y1[num - 1] < y1[num] > y1[num + 1]: # дошли до первого максимума, отбой
                    break

        # находим время запаздывания и постоянную времени через уравенение прямой
        tet = -y1[nmd] / (y1[nmd] - y1[nmd - 1]) * (t[nmd] - t[nmd - 1]) + t[nmd]
        T = (y1[-1] - y1[nmd]) / (y1[nmd] - y1[nmd - 1]) * (t[nmd] - t[nmd - 1]) + t[nmd]

        return tet, T, y1[num]


    Kk = 0
    flag = True
    # создаем объект пропорционального регулятора с начальными параметрами
    regulator = ProportionalRegulator()

    # калибровка регулятора, поиск критического состояния САУ
    while flag:
        regulator.set_regulator_coefficients(k=Kk)
        # объект класса САУ
        grand_gear_function = SchemeBody(regs_w=regulator.get_TrFunc_proportional_regulator())
        # передаточная функция САУ с регулятором
        w = grand_gear_function.get_scheme_solving()

        poles, zeros = pzmap(w, Plot=False)
        if size(poles) > 0:
            # есть ли корень на границе устойчивости
            flag = is_on_border(poles)
        if not flag: break
        Kk += 0.1

    print("Кп: ", round(Kk, 3))
    # находим период переходной характеристики
    Tt = plot_trans_func(w, toPlotTrans=True, toFindT=True)
    print("Период колебательной переходной характеристики: ", round(Tt, 6))

    # создаем новый объект ПИД-регулятора
    regulator = PIDRegulator()
    # устанавливаем параметры по методу Зиглера-Николса
    regulator.set_regulator_coefficients(k=0.6* Kk, Td=3/40 * Tt * Kk, Tu=1.2 * Kk / Tt)
    grand_gear_function = SchemeBody(regs_w=regulator.get_TrFunc_pid_regulator())
    # передаточная функция САУ с регулятором
    w = grand_gear_function.get_scheme_solving()

    poles, zeros = pzmap(w, Plot=False)
    if is_sustainable(poles):
        plot_trans_func(w, toPlotTrans=True)
        print("Оценка регулирования составляет: ", sum(do_direct_method(w)))
        return
    else:
        print("Система неустойчива! применим другой метод")

    """ переходим к оценке по второму методу Зиглера-Никольса"""
    tet, Tt, Kk = second_var()

    # создаем новый объект ПИД-регулятора
    regulator2 = PIDRegulator()
    # устанавливаем параметры по методу Зиглера-Николса
    regulator2.set_regulator_coefficients(k=1.2 * Tt / (Kk * tet), Td=1.2 * Tt / Kk, Tu=0.6 * Tt / (Kk * tet ** 2))
    grand_gear_function = SchemeBody(regs_w=regulator2.get_TrFunc_pid_regulator())
    # передаточная функция САУ с регулятором
    w = grand_gear_function.get_scheme_solving()

    poles, zeros = pzmap(w, Plot=False)
    if is_sustainable(poles) and (0.15 < tet / Tt < 0.6):
        plot_trans_func(w, toPlotTrans=True)
        print("Оценка регулирования составляет: ", sum(do_direct_method(w)))
    else:
        print("Опять неудача!")

genetic_method()