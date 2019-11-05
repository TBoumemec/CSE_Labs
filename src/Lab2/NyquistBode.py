from control import *
import matplotlib.pyplot as plt
from control.matlab import step
from numpy.linalg import det
from numpy.ma import arange

from src.Lab2 import initPamsLab2
from src.Lab2 import dictionary

class Nyquist:

    def __init__(self, w_f = initPamsLab2.calc_nyquist()):
        self.w = w_f
        self.t = np.linspace(0, stop=50, num=1000)

    def get_nyquist_diagram(self):
        print(self.w)
        real, imag, freq = nyquist(self.w, labelFreq=10, color='g')
        plt.title('Nyquist Diagram')
        plt.plot()
        plt.show()
        #
        return

    def get_bode_func(self):
        print(self.w)
        mag, phase, omega = bode(self.w, dB=False)
        plt.title("Frequency Response", y=2.2)
        plt.plot()
        plt.show()

        return

    def all_of_them(self):
        Nyquist(self).get_nyquist_diagram()
        Nyquist(self).get_bode_func()