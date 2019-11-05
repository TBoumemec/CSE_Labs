from control import *
import matplotlib.pyplot as plt
from control.matlab import step
from numpy.linalg import det
from numpy.ma import arange

from src.Lab2 import initPamsLab2
from src.Lab2 import dictionary


class newToolBox:

    def __init__(self, w_f = initPamsLab2.calc_w()):
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

    def get_bode_func(self):
        print(self.w)
        mag, phase, omega = bode(self.w, dB=False)
        plt.title("Frequency Response", y=2.2)
        plt.plot()
        plt.show()

        return

    def get_nyquist_diagram(self):
        real, imag, freq = nyquist(self.w, labelFreq=10, color='g')
        plt.title('Nyquist Diagram')
        plt.plot()
        plt.show()
        #
        return

    def get_poles_analyze(self):
        from control import pole

        poles = pole(self.w)
        print(poles)
        pole, zeros = pzmap(self.w)
        plt.title('Graph of poles')
        plt.plot()
        plt.show()

    def all_of_them(self):
        newToolBox(self).get_trans_func()
        newToolBox(self).get_nyquist_diagram()
        newToolBox(self).get_bode_func()
        newToolBox(self).get_poles_analyze()
