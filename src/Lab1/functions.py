"supporting function with graph instruments"

import numpy as np
import matplotlib.pyplot as plt
from control.matlab import *
from src.Lab1 import initPamsLab1
import control.matlab as ctr

numer = initPamsLab1.init_pam()[0]
denumer = initPamsLab1.init_pam()[1]
numer2 = initPamsLab1.init_pam()[2]
denumer2 = initPamsLab1.init_pam()[3]

t = np.linspace(0, stop=50, num=1000)

y1 = 0; y2 = 0;

ln = [y1, y2]



def trans_func(a):
    w = ctr.tf(numer[a], denumer[a])
    w1 = ctr.tf(numer2[a], denumer2[a])
    print(w)
    y1, t1 = step(w, t)
    y2, t2 = step(w1, t)
    ln[0], ln[1] = plt.plot(t, y1, "r", t, y2, "b")
    plt.legend(ln, ['Standart pams', 'x2 pams'])
    plt.title('Step Response')
    plt.ylabel('Amplitude  h(t)')
    plt.xlabel('Time(sec)')

    plt.grid(True)
    plt.show()

    return

def imp_func(a):
    w = tf(numer[a], denumer[a])
    w1 = tf(numer2[a], denumer2[a])
    print(w)
    y1, t1 = impulse(w, t)
    y2, t2 = impulse(w1, t)
    ln[0], ln[1] = plt.plot(t, y1, "r", t, y2, "b")
    plt.legend(ln, ['Standart pams', 'x2 pams'], loc='best')
    plt.title('Impulse Response ')
    plt.ylabel('Amplitude, w(t)')
    plt.xlabel('Time(sec)')
    plt.grid(True)
    plt.show()

    return


def bode_func(a):
    w = tf(numer[a], denumer[a])
    w1 = tf(numer2[a], denumer2[a])
    print(w)
    mag, phase, omega = bode(w, dB=False)
    mag1, phase1, omega1 = bode(w1, dB=False)
    plt.title("Frequency Response", y=2.2)
    plt.plot()
    plt.show()

    return


def all_func(a):
    trans_func(a)
    imp_func(a)
    bode_func(a)

    return

