from math import inf, log10, degrees

from control import *
from control.matlab import step, pzmap, bode
from numpy.ma import arctan, mean
from mpmath import pi, exp
import matplotlib.pyplot as plt
from src.Lab3.Scheme import Scheme_body

"""
Class let work with transition function(get_trans_func), analyzing of poles(get_poles_analyze),
                    godoghraph plotting(get_godoghraph)
"""


class Regulator_analyzer:

    def __init__(self, w_f=Scheme_body()):
        self.w = w_f.get_scheme_solving()
        self.t = np.linspace(0, stop=100, num=2000)

    def get_trans_func(self):

        """
        definition for analyzing regulator quality by step responce.
        parameters in research:
        - regulation time
        - hesistation
        - overshoot
        - degree of attenuation
        :return: keys for handle changing regulator quality
        """

        # ключи для оценки регулирования
        key_koleb = 0
        key_reg = 0
        key_per = 0

        counter = 0
        regulation_time = inf
        t_vr_reg = 0
        integral_mean = 0

        print(self.w)

        y1, t1 = step(self.w, self.t)

        max_y = max(y1)
        last_y = y1[-1]

        overshoot = (max_y - last_y) / last_y * 100
        print("*" * 20, "\n"
                        "Перерегулирование составляет: " + str(overshoot) + " %")

        if overshoot > 27:
            print("Полученная величина выше оптимальной области регулирования")
            key_per = -1
        elif overshoot < 10:
            print("Полученная величина ниже оптимальной области регулирования")
            key_per = 1
        else:
            print("Показатель в норме")

        y2 = list(y1)
        y3 = list(y1)

        print("*" * 20, "\n"
                        "Величина: " + str(max(y2)) + " и время достижения первого максимума: "
              + str(self.t[y2.index(max(y2))]))

        # ******************************
        # костыль, который помогает найти максимум второй вершины переходной характеристики
        del y2[0:y2.index(max(y2))]
        del y2[0:y2.index(min(y2))]
        # ******************************

        degree_of_attenuation = 1 - max(y2) / max(y1)
        print("*" * 20, "\n"
                        "Степень затухания составляет: ", degree_of_attenuation)

        for i in range(len(y1)):
            if 0.95 * last_y < y1[i] < 1.05 * last_y:
                """
                counter - счетчик входящих в диапазон установившегося значения точек
                устраняет вероятность ошибки попадания условия в нулевой промежуток колебательной
                функции
                """
                counter += 1
                if counter == 20:  # функция внутри диапазона, удовл. достаточности уст. режима.
                    regulation_time = self.t[i]
                    # номер нахождения в массиве t значения времени регулирования
                    t_vr_reg = i
                    print("*" * 20, "\n"
                                    "Время регулирования: " + str(regulation_time) + " c")
                    break
            else:  # функция еще не в установившемся значении
                counter = 0

        print("Полученная величина выше оптимальной области регулирования" if regulation_time > 17
              else "Отлично")

        if regulation_time > 17:
            key_reg = -1

        hills = 0

        # грубый счетчик вершин
        while True:
            if max(y3) > 1.05 * last_y:  # нашел вершину и срезал массив до нее
                del y3[0:y3.index(max(y3))]
                hills += 1  # добавляет вершину
            else:
                break
            if 0.95 * last_y > min(y3):  # нашел впадину и срезал массив до нее
                del y3[0:y3.index(min(y3))]
            else:  # больше нет ни вершин, ни впадин
                break
            if hills > 10:  # аномально большая выборка, нет смысла идти дальше
                break

        print("*" * 20, "\n"
                        "Колебательность составляет: ", hills, " вершин"
                                                               " или ", max(y2) / max(y1) * 100, "%")

        if hills > 2:
            print("Полученная величина колебаний выше оптимальной области регулирования")
            key_koleb = -1
        else:
            print("Отлично")


        for i in range(0, t_vr_reg):
            integral_mean = integral_mean + abs(y1[t_vr_reg] - y1[i]) * self.t[1]

        print("*" * 20, "\n"
                        "Интеграл составил: ", integral_mean)


        plt.plot(self.t, y1, "r")
        plt.title('Step Response')
        plt.ylabel('Amplitude  h(t)')
        plt.xlabel('Time(sec)')
        plt.grid(True)
        plt.show()

        return [key_koleb, key_reg, key_per]

    def get_poles_analyze(self, poles):

        """
        definition for analyzing by graph poles:
        - regulation time
        - hesistation
        - overshoot
        - degree of attenuation
        :param poles: mean of poles transmission function
        :return:  keys for handle changing regulator quality
        """

        # ключи для оценки регулирования
        key_koleb = 0
        key_reg = 0
        key_per = 0

        degree_max = 0
        a = True
        counter = 1

        print("Полюса плоскости: ")
        for i in poles:
            if i.real >= 0:  # корень в левой полуплоскости
                a = False
            print("Полюс ", counter, " : ", i)
            counter += 1

        print("СИСТЕМА НЕ ПРОХОДИТ ПРОВЕРКУ ПО УСТОЙЧИВОСТИ!" if not a else
              "По критерию полюсов система устойчива")

        regulation_time = 1.0 / abs(max(poles.real))
        print("\nВремя регулирования: " + str(regulation_time))

        print("Полученная величина выше оптимальной области регулирования" if regulation_time > 17
              else "Отлично")

        if regulation_time > 17:
            key_reg = -1

        for a in poles:
            degree = arctan(abs(a.imag) / abs(a.real))
            degree_max = (degree if (a.imag != 0) & (degree_max < degree) else degree_max)

        print("*" * 20, "\n"
                        "Колебательность составляет: " + str(degree_max))
        if degree_max >= 1.57:
            print("Колебательность выше оптимального диапазона")
            key_koleb = -1

        overshoot = exp(- pi / degree_max) * 100

        print("*" * 20, "\n"
                        "Перерегулирование: " + str(overshoot) + " %")

        if overshoot > 27:
            print("Полученная величина выше оптимальной области регулирования")
            key_per = -1
        elif overshoot < 10:
            print("Полученная величина ниже оптимальной области регулирования")
            key_per = 1
        else:
            print("Отлично")

        degree_of_attenuation = 1 - exp(- 2 * pi / degree_max)

        print("*" * 20, "\n"
                        "Степень затухания: " + str(degree_of_attenuation))

        plt.title('Graph of poles')
        plt.plot()
        plt.show()

        return [key_koleb, key_reg, key_per]

    def get_bode_func(self):
        """
        definition for plotting "AFC" and "LAFC" and analyzing parameters:
        - hesitation
        - regulation time
        - phase margin
        - amplitude margin
        :return:  keys for handle changing regulator quality
        """

        key_koleb = 0
        key_reg = 0
        key_phase = 0
        key_mag = 0

        mag, phase, omega = bode(self.w, dB=False)

        hesitation = max(mag) / mag[0]
        print("Показатель колебательности M: " + str(hesitation))
        if hesitation > 1.5:
            print("Степень затухания выше оптимального регулировочного диапазона")
            key_koleb = -1
        elif hesitation < 1.1:
            print("Степень затухания ниже оптимального регулировочного диапазона")
            key_koleb = 1

        c = [i for i in range(1, len(mag))
             if (mag[0] - 0.1) < mag[i] < (mag[0] + 0.1)]

        regulation_time = 2 * 2 * pi / omega[c[-1]]

        print("Время регулирования: ", str(regulation_time))
        if regulation_time > 17:
            print("Полученная величина выше оптимальной области регулирования")
            key_reg = -1
        else:
            print("Отлично")

        plt.title("Frequency Response", y=2.2)
        plt.plot()
        plt.show()

        mag, phase, omega = bode(self.w, dB=True)

        # перевод в Дб
        mag = [20 * log10(i) for i in mag]

        #!!!!!!!!!
        # костыль для точности нахождения запаса
        mag1 = list(mag)
        for i in range(0, mag1.index(max(mag1))):
            mag1[i] = inf

        # перевод из радиан в градусы
        phase = [degrees(i) for i in phase]

        #!!!!!!!!!
        # костыль для точности нахождения запаса
        phase1 = list(phase)
        for i in range(phase1.index(min(phase1)), len(phase1)):
            phase1[i] = -inf

        a = []
        b = []

        for i in range(len(mag1)):
            if -5 < mag1[i] < 5 and len(a) <= 1:
                a.append(i)
            if -190 < phase1[i] < -170 and len(b) <= 1:
                b.append(i)

        if a:
            phase_margin = phase[int(round(mean(a)))] + 180
            print("*" * 20, "\n"
                            "Запас по фазе: " + str(phase_margin))
            if phase_margin <= 0:
                print("Запаса по фазе недостаточно")
                key_phase = 1
            else:
                print("Запас достаточен")
        else:
            print("Запаса по фазе недостаточно")
            key_phase = 1

        if b:
            print(b)

            amplitude_margin = - mag[int(round(mean(b)))]
            print("*" * 20, "\n"
                            "Запас по амплитуде: " + str(amplitude_margin))
            if amplitude_margin <= 0:
                print("Запаса по амплитуде недостаточно")
                key_mag = 1
            else:
                print("Запас достаточен")
        else:
            print("Запаса по амплитуде недостаточно")
            key_mag = 1

        plt.title("Frequency Response", y=2.2)
        plt.plot()
        plt.show()

        return [key_koleb, key_reg, key_phase, key_mag]

    def full_analyze(self):
        """
        complex research definition
        :return:  keys for handle changing regulator quality
        """

        k = []

        print("\n", "*" * 40, "\n"
                              "STEP RESPONCE:\n")
        k.extend(self.get_trans_func())

        print("\n", "*" * 40, "\n"
                              "POLES ANALYZE:\n")

        poles, zeros = pzmap(self.w)
        if poles != []:
            k.extend(self.get_poles_analyze(poles))
        else:
            print("Корней нет!!!")

        print("\n", "*" * 40, "\n"
                              "BODE FUNCTION:\n")
        k.extend(self.get_bode_func())

        return k
