from control import *

init = [20, 14, 5, 7, 1, 5]



def init_pams():
    """
    just getter of initial pams
    :return:
    """
    return init


def finish_chain(inits):
    """
    :param inits: gives a freedom in changing of init pams
    :return: w6 is a finished chain
    """
    # для задачи на защите
    # w0 = tf(1, 1)
    # ww = tf([2, 0.1], [1, 0])
    # # print(ww)
    # ww2 = tf([0, 3, 0], [4, -2, 1])
    # # print(ww2)
    # w33 = series(ww, ww2)
    # # print(w33)
    # w44 = feedback(w33, w0, -1)
    # # print(w44)

    compW1 = [[inits[1], 1], [inits[5], 1]]
    w1 = tf(compW1[0], compW1[1])

    compW2 = [[1], [inits[2], 1]]
    w2 = tf(compW2[0], compW2[1])

    compW3 = [[0.05 * inits[4], 1], [0.05 * inits[2], 1]]
    w3 = tf(compW3[0], compW3[1])

    compW4 = [inits[0], [inits[3], 1]]
    w4 = tf(compW4[0], compW4[1])

    w5 = series(w2, w3, w4)
    w6 = feedback(w5, w1, -1)

    return w6

def finish_for_nyquist(inits):
    """
    same as finish_chain but for unlocked CSU
    :param inits: gives a freedom in changing of pams
    :return: w6 is a finished chain
    """

    compW1 = [[inits[1], 1], [inits[5], 1]]
    w1 = tf(compW1[0], compW1[1])

    compW2 = [[1], [inits[2], 1]]
    w2 = tf(compW2[0], compW2[1])

    compW3 = [[0.05 * inits[4], 1], [0.05 * inits[2], 1]]
    w3 = tf(compW3[0], compW3[1])

    compW4 = [inits[0], [inits[3], 1]]
    w4 = tf(compW4[0], compW4[1])

    w5 = series(w2, w3, w4, w1)

    return w5


def calc_w():
    """
    fast calculation of finished chain with initial pams
    :return:
    """
    inits = init_pams()
    w = finish_chain(inits)

    return w

def calc_nyquist():
    inits = init_pams()
    w = finish_for_nyquist(inits)

    return w
