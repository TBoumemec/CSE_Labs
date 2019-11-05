from control import *
import matplotlib.pyplot as plt
from src.Lab2 import initPamsLab2



"""
Class let work with nyquist diagram(def get_nyquist_diagram) and bode func(def get_bode_func)
"""
class NyquistBode:

    def __init__(self, w_f = initPamsLab2.calc_nyquist()):
        self.w = w_f
        self.t = np.linspace(0, stop=50, num=1000)

    def get_nyquist_diagram(self):

        real, imag, freq = nyquist(self.w, labelFreq=10, color='g')

        # print(real, imag)
        # for i in range(len(imag)):
        #     print("real:", imag[i]) if -0.001 <= real[i] <= 0.001 else "no"

        plt.title('Nyquist Diagram')
        plt.plot()
        # plt.Circle((0, 0), 1, color='r')
        # plt.plot()
        plt.show()

        return

    def get_bode_func(self):

        mag, phase, omega = bode(self.w, dB=False)
        plt.title("Frequency Response", y=2.2)
        plt.plot()
        plt.show()

        return

    def all_of_them(self):
        NyquistBode(self).get_nyquist_diagram()
        NyquistBode(self).get_bode_func()