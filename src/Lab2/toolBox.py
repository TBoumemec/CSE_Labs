from control import *
import matplotlib.pyplot as plt
from control.matlab import step
from numpy.linalg import det
from numpy.ma import arange

from src.Lab2 import initPamsLab2

t = np.linspace(0, stop=50, num=1000)



def trans_func():

    w = initPamsLab2.calc_w()

    print(w)
    y1, t1 = step(w, t)
    plt.plot(t, y1, "r")
    plt.title('Step Response')
    plt.ylabel('Amplitude  h(t)')
    plt.xlabel('Time(sec)')
    plt.grid(True)
    plt.show()

    return


def bode_func():

    w = initPamsLab2.calc_w()

    print(w)
    mag, phase, omega = bode(w, dB=False)
    plt.title("Frequency Response", y=2.2)
    plt.plot()
    plt.show()

    return


def nyquist_diagram():

    w = initPamsLab2.calc_w()

    real, imag, freq = nyquist(w, labelFreq=10, color='g')
    plt.title('Nyquist Diagram')
    plt.plot()
    plt.show()
    #
    return

def poles_analaze():

    from control import pole

    w = initPamsLab2.calc_w()
    poles = pole(w)
    print(poles)
    pole, zeros = pzmap(w)
    plt.title('Graph of poles')
    plt.plot()
    plt.show()


def gurwitz_crit():

    w = initPamsLab2.calc_w()
    matrix = formating_matrix(w)

    for i in range(len(matrix), 0, -1):
        opr = det(matrix[:i, :i])
        print("det of", i, "matrix: ", opr)
        if opr < 0:
            print("ne ust")
            break



    inits = initPamsLab2.init_pams()

    for i in arange(1.3936,1.3937,0.00001):
        inits[1] = i
        w = initPamsLab2.finish_chain(inits)
        matrix = formating_matrix(w)
        opr = det(matrix[:len(matrix) - 1, :len(matrix) - 1])
        print("det", opr, "Koc:", i) if - 2 <= opr <= 2 else "no"





# def critical_number(init):
#
#     w = initPamsLab2.finish_chain(init)
#
#     num, denum = tfdata(w)
#     # num = num[0][0][:]
#     denum = denum[0][0][:]


def formating_matrix(w):

    num, denum = tfdata(w)
    # num = num[0][0][:]
    denum = denum[0][0][:]

    matrix = np.zeros((len(denum) - 1, len(denum) - 1))
    a1 = 0

    for i in range(len(denum) - 1):
        if i % 2 == 0:
            a = int((i + 1) // 2)

            a1 = a

        else:
            a = a1

        for j in range(len(denum)):

            if (j % 2) != (i % 2):
                matrix[i, a] = denum[j]
                # print(a)
                # print(matrix)
                a += 1

    # print(matrix)

    return matrix


