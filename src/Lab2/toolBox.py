from control import *
import matplotlib.pyplot as plt
from control.matlab import step
from numpy.linalg import det
from numpy.ma import arange

from src.Lab2 import initPamsLab2
from src.Lab2 import dictionary


# old but not forgotten

# t = np.linspace(0, stop=50, num=1000)
#
#
# w = initPamsLab2.calc_w()
#
#
# def trans_func(self, ww):
#
#     self.w = ww
#
#
#     print(w)
#     y1, t1 = step(w, t)
#     plt.plot(t, y1, "r")
#     plt.title('Step Response')
#     plt.ylabel('Amplitude  h(t)')
#     plt.xlabel('Time(sec)')
#     plt.grid(True)
#     plt.show()
#
#     return
#
#
# def bode_func():
#
#     print(w)
#     mag, phase, omega = bode(w, dB=False)
#     plt.title("Frequency Response", y=2.2)
#     plt.plot()
#     plt.show()
#
#     return
#
#
# def nyquist_diagram():
#
#
#     real, imag, freq = nyquist(w, labelFreq=10, color='g')
#     plt.title('Nyquist Diagram')
#     plt.plot()
#     plt.show()
#     #
#     return
#
# def poles_analaze():
#
#     from control import pole
#
#     poles = pole(w)
#     print(poles)
#     pole, zeros = pzmap(w)
#     plt.title('Graph of poles')
#     plt.plot()
#     plt.show()
#
#
#
#
# def all_of_them():
#     trans_func()
#     bode_func()
#     nyquist_diagram()
#     poles_analaze()

