from control import *

init = [20, 14, 5, 7, 1, 5]

# w0 = tf(1, 1)

compW1 = [[init[1], 1], [init[5], 1]]
w1 = tf(compW1[0], compW1[1])

compW2 = [[1], [init[2], 1]]
w2 = tf(compW2[0], compW2[1])

compW3 = [[0.05 * init[4], 1], [0.05 * init[2], 1]]
w3 = tf(compW3[0], compW3[1])

compW4 = [init[0], [init[3], 1]]

w4 = tf(compW3[0], compW3[1])
w5 = series(w2, w3)
w6 = series(w5, w4)
w7 = feedback(w6, w1, -1)


def finish_chain():
    return w7
