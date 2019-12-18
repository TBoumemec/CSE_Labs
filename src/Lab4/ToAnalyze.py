from control.matlab import step
from control import *
from src.Lab4.ToPlot import plot_trans_func


def do_direct_method(w):
    """
    definition for analyzing regulator quality by step responce.
    parameters in research:
    - regulation time
    - hesistation
    - overshoot
    - degree of attenuation
    :return: keys for handle changing regulator quality
    """

    def get_degree(ideal, actual):
        """
        функция оценивает полученное значение по пятибальной шкале
        :param ideal: идеальное значение
        :param actual: реальное значение
        :return: оценка
        """
        mas = [0, 1, 1.2, 1.4, 1.6, 1.8, 2]
        for i in range(len(mas) - 1):
            if mas[i] * ideal <= actual < mas[i + 1] * ideal:
                return len(mas) - 2 - i
            elif actual > mas[-1] * ideal:
                return 0

    t = np.linspace(0, stop=100, num=2000)

    counter = regulation_time = t_vr_reg = integral_mean = 0

    y1, t1 = step(w, t)

    y1 = list(y1)
    max_y = max(y1)
    last_y = y1[-1]

    """перерегулирование и его оценка"""
    overshoot = (max_y - last_y) / last_y
    key_per = get_degree(27, overshoot)

    """величина и время достижения первого максимума и их оценка"""
    key_vel_max = get_degree(1.1, max(y1))
    key_vr_max = get_degree(1, t[y1.index(max(y1))])

    two_maxes = []

    for num in range(len(y1[1:-1])):
        if y1[num - 1] < y1[num] > y1[num + 1]:
            two_maxes.append(y1[num])
        if len(two_maxes) == 10: break

    """степень затухания и ее оценка"""
    if len(two_maxes) <= 1:
        key_deg = 5.0
    else:
        degree_of_attenuation = (1 - two_maxes[1] / two_maxes[0]) * 100
        if degree_of_attenuation <=0:
            key_deg = -1
        else: key_deg = get_degree(1 / 6.6, 1 / degree_of_attenuation)


    for i in range(len(y1)):
        if 0.95 * last_y < y1[i] < 1.05 * last_y:
            """
            counter - счетчик входящих в диапазон установившегося значения точек
            устраняет вероятность ошибки попадания условия в нулевой промежуток колебательной
            функции
            """
            counter += 1
            if counter == 20:  # функция внутри диапазона, удовл. достаточности уст. режима.
                regulation_time = t[i]
                # номер нахождения в массиве t значения времени регулирования
                t_vr_reg = i
                break
        else:  # функция еще не в установившемся значении
            counter = 0

    """оценка времени регулирования"""
    key_reg = get_degree(15, regulation_time)

    """оценка показателя колебательности"""
    if len(two_maxes) <= 1:
        key_koleb = 5.0
    else:
        koleb = two_maxes[1] / two_maxes[0] * 100
        key_koleb = get_degree(1.19, koleb)



    """интеграл и его оценка"""
    for i in range(0, t_vr_reg):
        integral_mean = integral_mean + abs(y1[t_vr_reg] - y1[i]) * t[1]
    key_int = get_degree(0.3, integral_mean)


    # проверка системы на устойчивость
    poles, zeros = pzmap(w, Plot=False)
    if not is_sustainable(poles):
        return [-100]

    return [key_koleb, key_reg, key_per, key_deg,
            key_vel_max, key_vr_max, key_int]


def is_sustainable(poles):
    """
    функция определения устойчивости АСУ
    :param poles: полюса системы
    :return: true/false
    """

    boo = True

    for pole in poles:
        if pole.real > 0:
            boo = False
            break

    return boo