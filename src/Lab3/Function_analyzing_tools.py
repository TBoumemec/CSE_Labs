from control import *
from control.matlab import step
from numpy import mean
from numpy.ma import arange, count, arctan
from control import tf
from mpmath import re, im, sqrt, e, pi, exp
import matplotlib.pyplot as plt
from scipy import integrate
from src.Lab3.Initial_parameters import Initialazer

"""
Class let work with transition function(get_trans_func), analyzing of poles(get_poles_analyze),
                    godoghraph plotting(get_godoghraph)

"""
key1 = 0
key2 = 0
key3 = 0
key4 = 0
key5 = 0
key6 = 0
key7 = 0


class My_function:

    def __init__(self, w_f=Initialazer().get_scheme_solving()):
        self.w = w_f
        self.t = np.linspace(0, stop=50, num=1000)

    def get_trans_func(self):

        print(self.w)

        y1, t1 = step(self.w, self.t)

        # print(y1[-1])
        # print(max(y1))
        maxis = max(y1)
        last = y1[-1]

        perereg = (maxis - last) / last * 100
        print("************************\n"
              "Перерегулирование составляет: " + str(perereg) + " %")

        if perereg > 30:
            print("Полученная величина выше оптимальной области регулирования")
            key_per = -1
        elif perereg < 10:
            print("Полученная величина ниже оптимальной области регулирования")
            key_per = 1
        else:
            print("Отлично")

        y2 = list(y1)
        y3 = list(y1)

        print("************************\n"
              "Величина: " + str(max(y2)) + " и время достижения первого максимума: "
              + str(self.t[y2.index(max(y2))]))

        del y2[0:y2.index(max(y2))]
        del y2[0:y2.index(min(y2))]

        step_zat = 1 - max(y2) / max(y1)
        print("************************\n"
              "Степень затухания составляет: ", step_zat)

        if step_zat > 0.95:
            print("Полученная величина выше оптимальной области регулирования")
            key_zat = -1
        elif step_zat < 0.75:
            print("Полученная величина ниже оптимальной области регулирования")
            key_zat = 1
        else:
            print("Отлично")

        numnum = 0

        for i in range(len(y1)):
            if 0.95 * last < y1[i] < 1.05 * last:
                # num = i
                numnum += 1
                if numnum == 20:
                    vr_reg = self.t[i]
                    t_vr_reg = i
                    print("************************\n"
                          "Время регулирования: " + str(vr_reg) + " c")
                    break
            else:
                numnum = 0

        koleb = 0

        while True:
            if max(y3) > 1.05 * last:
                del y3[0:y3.index(max(y3))]
                koleb += 1
            else:
                break
            if 0.95 * last > min(y3):
                del y3[0:y3.index(min(y3))]
            else:
                break

        print("************************\n"
              "Колебательность составляет: ", koleb, " вершин"
                                                     " или ", max(y2) / max(y1) * 100, "%")

        if koleb > 2:
            print("Полученная величина колебаний выше оптимальной области регулирования")
            key_koleb = -1
        else:
            print("Отлично")

        integro = 0

        for i in range(0,t_vr_reg):
            integro = integro + abs(y1[t_vr_reg] - y1[i])

        print("************************\n"
              "Интеграл составил: " , integro)
        # *****************************
        # y = lambda p: self.w
        # print(y)
        # print("Интегральчик: " + str(integrate.quad(self.w,0,vr_reg)))
        # *****************************

        plt.plot(self.t, y1, "r")
        plt.title('Step Response')
        plt.ylabel('Amplitude  h(t)')
        plt.xlabel('Time(sec)')
        plt.grid(True)
        plt.show()

        # yUst = y1[-1]
        # yMax = max(y1)

        # key_per, key_zat, key_koleb
        return

    def get_poles_analyze(self):
        from control import pole

        pole, zeros = pzmap(self.w)

        a = True
        print("Полюса плоскости: ")
        for i in range(len(pole)):
            if pole[i].real >= 0:
                a = False
            print("Полюс ", i + 1, " : ", pole[i])

        if a == False:
            print("СИСТЕМА НЕ ПРОХОДИТ ПРОВЕРКУ ПО УСТОЙЧИВОСТИ!")
        else: print("По критерию полюсов система устойчива")

        print("\nВремя регулирования: " + str(1.0 / abs(max(pole.real))))
        # забыл для чего
        # print(min(pole))

        degree_max = 0

        for i in range(len(pole)):
            if (pole[i].imag != 0) & (degree_max < arctan(abs(pole[i].imag) / abs(pole[i].real))):
                degree_max = arctan(abs(pole[i].imag) / abs(pole[i].real))
        print("************************\n"
              "Колебательность составляет: " + str(degree_max))
        if degree_max >= 1.57:
            print("Колебательность выше оптимального диапазона")
            key_kolebb = -1

        print("************************\n"
              "Перерегулирование: " + str(e + (pi / degree_max)))
        step_zat = 1 - exp(- 2 * pi / degree_max)
        print("************************\n"
              "Степень затухания: " + str(step_zat))
        if step_zat > 0.98:
            print("Степень затухания выше оптимального регулировочного диапазона")
            key_zatt = -1
        elif step_zat < 0.9:
            print("Степень затухания ниже оптимального регулировочного диапазона")
            key_zatt = 1
        else: print("Степень затухания в оптимальном диапазоне")

        plt.title('Graph of poles')
        plt.plot()
        plt.show()

        # key_kolebb, key_zatt
        return

    def get_bode_func(self):

        mag, phase, omega = bode(self.w, dB=False)

        M = max(mag) / mag[0]
        print("Показатель колебательности M: " + str(M))
        if M > 1.5:
            print("Степень затухания выше оптимального регулировочного диапазона")
            key_kolebbb = -1
        elif M < 1.1:
            print("Степень затухания ниже оптимального регулировочного диапазона")
            key_kolebbb = 1
        c = []

        for i in range(1, len(mag)):
            if mag[0] - 0.1 < mag[i] < mag[0] + 0.1:
                c.append(i)

        # print("Частота среза: ", str(omega[c[-1]]))

        print("Время регулирования: ", str(2 * 2 * pi / omega[c[-1]]))

        plt.title("Frequency Response", y=2.2)
        plt.plot()
        plt.show()

        mag, phase, omega = bode(self.w, dB=True)

        a = []
        b = []

        for i in range(len(mag)):
            if -0.000005 < mag[i] < 0.000005:
                a.append(i)
            if -0.005 < phase[i] < 0.005:
                b.append(i)

        zap_a = phase[(round(mean(a)))]
        zap_b = mag[(round(mean(b)))]
        print("************************\n"
              "Запас по фазе: " + str(zap_a))
        if zap_a <= 0:
            print("Запаса по фазе недостаточно")
            key_phase = 1
        else:
            print("Запас достаточен")

        print("************************\n"
              "Запас по амплитуде: " + str(zap_b))
        if zap_b <= 0:
            print("Запаса по амплитуде недостаточно")
            key_mag = 1
        else:
            print("Запас достаточен")

        plt.title("Frequency Response", y=2.2)
        plt.plot()
        plt.show()

        # key_kolebbb, key_phase, key_mag
        return

    def full_analyze(self):
        print("\n****************************************\n"
              "STEP RESPONCE:\n")
        self.get_trans_func()

        print("\n****************************************\n"
              "POLES ANALYZE:\n")
        self.get_poles_analyze()

        print("\n****************************************\n"
              "BODE FUNCTION:\n")
        self.get_bode_func()
