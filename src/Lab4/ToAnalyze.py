from control.matlab import step
from control import *


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
        if actual < ideal:
            return 5
        elif ideal < actual < 6 / 5 * ideal:
            return 4
        elif 6 / 5 * ideal < actual < 7 / 5 * ideal:
            return 3
        elif 7 / 5 * ideal < actual < 8 / 5 * ideal:
            return 2
        elif 8 / 5 * ideal < actual < 9 / 5 * ideal:
            return 1
        return 0

    t = np.linspace(0, stop=100, num=2000)

    counter = regulation_time = t_vr_reg = integral_mean = 0

    y1, t1 = step(w, t)

    max_y = max(y1)
    last_y = y1[-1]

    """перерегулирование и его оценка"""
    overshoot = (max_y - last_y) / last_y
    key_per = get_degree(10, overshoot)

    y2 = list(y1)

    """величина и время достижения первого максимума и их оценка"""
    key_vel_max = get_degree(1.0914, max(y2))
    key_vr_max = get_degree(0.8, t[y2.index(max(y2))])

    # ******************************
    # костыль, который помогает найти максимум второй вершины переходной характеристики
    del y2[0:y2.index(max(y2))]
    del y2[0:y2.index(min(y2))]
    # ******************************

    """степень затухания и ее оценка"""
    degree_of_attenuation = 1 - max(y2) / max(y1) * 100
    key_deg = get_degree(1 / 6.5, 1 / degree_of_attenuation)

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
    key_reg = get_degree(5, regulation_time)

    koleb = max(y2) / max(y1) * 100

    """оценка показателя колебательности"""
    key_koleb = get_degree(0.8, koleb)
    """интеграл и его оценка"""
    for i in range(0, t_vr_reg):
        integral_mean = integral_mean + abs(y1[t_vr_reg] - y1[i]) * t[1]
    key_int = get_degree(0.25, integral_mean)


    # проверка системы на устойчивость
    poles, zeros = pzmap(w, Plot=False)
    if not is_sustainable(poles):
        return [0]

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