import random

from control import *
from control.matlab import step
from numpy.ma import arange, count, arctan
from control import tf
from mpmath import re, im, sqrt
import matplotlib.pyplot as plt

from src.Lab3 import initPamsLab3

"""
Class let work with transition function(get_trans_func), analyzing of poles(get_poles_analyze),
                    godoghraph plotting(get_godoghraph)

"""


class newToolBox:

    def __init__(self, w_f=initPamsLab3.calc_nyquist()):
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
        print("Перерегулирование составляет: " + str(perereg) + " %")

        y2 = list(y1)

        print("Величина: " + str(max(y2)) + " и время достижения первого максимума: " + str(self.t[y2.index(max(y2))]))
        del y2[0:y2.index(max(y2))]
        del y2[0:y2.index(min(y2))]

        koleb = max(y2) / max(y1)
        print("Колебательность составляет: " + str(koleb) + " %")
        step_zat = 1 - max(y1)/max(y2)
        print("Степень затухания составляет: ", step_zat)


        numnum = 0

        for i in range(len(y1)):
            if 0.95 * last < y1[i] < 1.05 * last:
                num = i
                numnum += 1
                if numnum == 20:
                    print("Время регулирования: " + str(self.t[i]) + " c")
                    break
            else:
                numnum = 0




        plt.plot(self.t, y1, "r")
        plt.title('Step Response')
        plt.ylabel('Amplitude  h(t)')
        plt.xlabel('Time(sec)')
        plt.grid(True)
        plt.show()

        # yUst = y1[-1]
        # yMax = max(y1)

        return

    def get_poles_analyze(self):
        from control import pole

        pole, zeros = pzmap(self.w)
        print(pole)

        # print("Время регулирования: " + str(1.0 / abs(max(pole.real))))
        print(min(pole))

        degree_max = 0

        for i in range(len(pole)):
            if (pole[i].imag != 0) & (degree_max < arctan(abs(pole[i].imag) / abs(pole[i].real))):
                 degree_max = arctan(abs(pole[i].imag)/abs(pole[i].real))
        print("Колебательность составляет: " + str(degree_max))
        plt.title('Graph of poles')
        plt.plot()
        plt.show()