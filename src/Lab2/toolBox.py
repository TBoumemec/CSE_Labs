from control import *
import matplotlib.pyplot as plt
from control.matlab import step
from sympy import det

t = np.linspace(0, stop=50, num=1000)



def trans_func(w):
    print(w)
    y1, t1 = step(w, t)
    plt.plot(t, y1, "r")
    plt.title('Step Response')
    plt.ylabel('Amplitude  h(t)')
    plt.xlabel('Time(sec)')
    plt.grid(True)
    plt.show()

    return


def bode_func(w):

    print(w)
    mag, phase, omega = bode(w, dB=False)
    plt.title("Frequency Response", y=2.2)
    plt.plot()
    plt.show()

    return


def nyquist_diagram(w):
    real, imag, freq = nyquist(w, labelFreq=10, color='g')
    plt.title('Nyquist Diagram')
    plt.plot()
    plt.show()

    return

def poles_analaze(w):

    from control import pole

    poles = pole(w)
    print(poles)
    pole, zeros = pzmap(w)
    plt.title('Graph of poles')
    plt.plot()
    plt.show()


def gurwitz_crit(w):
    num, denum = tfdata(w)
    num = num[0][0][:]
    denum = denum[0][0][:]

    matrix = np.zeros((len(denum) - 1, len(denum) - 1))
    a1 = 0

    for i in range(len(denum) - 1):
        if (i + 1) % 2 != 0:
            a = int((i + 1) // 2)
            a1 = a

        else:
            a = a1

        for j in range(len(denum) - 1):
            if (j % 2) == (i % 2):
                matrix[i][a] = denum[j]
                a += 1

    for i in range((len(matrix)), -1, -1):
        opr = det(matrix[:i, :i])
        print(opr)
        if opr < 0:
            print("ne ust")
            break