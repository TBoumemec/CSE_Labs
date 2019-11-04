from control import *

init = [20, 14, 5, 7, 1, 5]

def init_pams():
    return init

def finish_chain(inits):
    # w0 = tf(1, 1)

    compW1 = [[inits[1], 1], [inits[5], 1]]
    w1 = tf(compW1[0], compW1[1])

    compW2 = [[1], [inits[2], 1]]
    w2 = tf(compW2[0], compW2[1])

    compW3 = [[0.05 * inits[4], 1], [0.05 * inits[2], 1]]
    w3 = tf(compW3[0], compW3[1])

    compW4 = [inits[0], [inits[3], 1]]
    w4 = tf(compW4[0], compW4[1])

    w5 = series(w2, w3)
    w6 = series(w5, w4)
    w7 = feedback(w6, w1, -1)


    return w7

def calc_w():

    inits = init_pams()
    w = finish_chain(inits)

    return w