from control import *
from control.matlab import step
from numpy.ma import arange
from control import tf
from mpmath import re, im, sqrt
import matplotlib.pyplot as plt

from src.Lab2 import initPamsLab2


"""
Class let work with transition function(get_trans_func), analyzing of poles(get_poles_analyze),
                    godoghraph plotting(get_godoghraph)

"""

class newToolBox:

    def __init__(self, w_f=initPamsLab2.calc_w()):
        self.w = w_f
        self.t = np.linspace(0, stop=50, num=1000)

    def get_trans_func(self):

        print(self.w)

        y1, t1 = step(self.w, self.t)
        plt.plot(self.t, y1, "r")
        plt.title('Step Response')
        plt.ylabel('Amplitude  h(t)')
        plt.xlabel('Time(sec)')
        plt.grid(True)
        plt.show()

        return

    def get_poles_analyze(self):
        from control import pole

        poles = pole(self.w)
        print(poles)
        pole, zeros = pzmap(self.w)
        plt.title('Graph of poles')
        plt.plot()
        plt.show()

    def get_godoghraph(self):
        w_den = tf(self.w.den[0][0], [1])

        array = [];
        x = [];
        y = []

        j = sqrt(-1)
        length_of_array = 2
        for q in arange(0, length_of_array, 0.01):
            array.append(w_den(q * j))

        for i in array:
            x.append(re(i))
            y.append(im(i))

        plt.plot(x, y, "r")
        plt.title('Godograph')
        plt.ylabel('jY')
        plt.xlabel('X')
        plt.grid(True)
        plt.show()

    def all_of_them(self):
        newToolBox(self).get_trans_func()
        newToolBox(self).get_poles_analyze()
        newToolBox(self).get_godoghraph()
