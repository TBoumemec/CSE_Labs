from src.Lab3.Scheme import SchemeBody
from src.Lab4.Population import PopulationBody
import pylab
from mpl_toolkits.mplot3d import Axes3D
from src.Lab4.AnalyzingTools import do_direct_method, find_sustainability, find_T
from src.Lab3.Regulator import ProportionalRegulator,PIDRegulator
from control.matlab import pzmap

"""
Главное тело программы
"""


def genetic_method():
    """
    Генетический способ подбора параметров регулятора
    """

    def target_function(population):
        """
        здесь будет происходить оценка каждой особи
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

    # сортировка и отбор лучшей особи
    best_person, deg = group.sort_and_take_best(grades)
    best_of_the_best.append(best_person)

    while max(grades) <= 34:

        # процесс селекции, мутации и скрещивания
        group.set_pop_list(group.pop_selection()
                           + group.pop_mutation() + group.pop_breeding())

        grades = target_function(group)
        print(grades)

        best_person, deg = group.sort_and_take_best(grades)
        best_of_the_best.append(best_person)
        print("Поколение: ", len(best_of_the_best))
        print("Лучший результат поколения: Оценка-", deg[0],
              "Коэффициенты Кп, Кд, Ки-", best_person.get_regulator_coefficients())

        if len(best_of_the_best) % 10 == 0:  # неудачный вид
            print("неуд.вид")
            group.create_new_population()
        if len(best_of_the_best) >= 100:
            break

    # вывод лучших особей на график
    Kp = Kd = Ku = [0 for i in range(len(best_of_the_best))]
    for i in range(len(best_of_the_best)):
        Kp[i], Kd[i], Ku[i] = best_of_the_best[i].get_regulator_coefficients()

    fig = pylab.figure()
    axes = Axes3D(fig)
    axes.scatter(Kp, Kd, Ku)
    pylab.show()


def ZN_Method():
    """
    Метод подбора параметров регулятора Зиглера-Николса
    :return:
    """
    k = 0

    flag = True
    # создаем объект пропорционального регулятора с начальными параметрами
    regulator = ProportionalRegulator()
    regulator.set_regulator_coefficients(k=k)
    # объект класса САУ
    grand_gear_function = SchemeBody(regs_w=regulator.get_TrFunc_proportional_regulator())
    # передаточная функция САУ с регулятором
    w = grand_gear_function.get_scheme_solving()

    # калибровка регулятора, поиск критического состояния САУ
    while flag:
        poles, zeros = pzmap(w)
        if poles != []:
            # есть ли корень на границе устойчивости
            flag = find_sustainability(poles)
        else:  # poles=[]
            print("Корней нет!")
        if not flag: break
        k += 0.1

        regulator.set_regulator_coefficients(k=k)
        grand_gear_function = SchemeBody(regs_w=regulator.get_TrFunc_proportional_regulator())
        # передаточная функция САУ с регулятором
        w = grand_gear_function.get_scheme_solving()

    # находим период переходной характеристики
    T = find_T(w)
    # создаем новый объект ПИД-регулятора
    regulator = PIDRegulator()
    # устанавливаем параметры по методу Зиглера-Николса
    regulator.set_regulator_coefficients(k=0.6 / k, Td=0.5 * T / k, Tu=0.125 * T / k)
    grand_gear_function = SchemeBody(regs_w=regulator.get_TrFunc_pid_regulator())
    # передаточная функция САУ с регулятором
    w = grand_gear_function.get_scheme_solving()

    print("Оценка регулярования составляет: ", sum(do_direct_method(w)))

    pass


genetic_method()
