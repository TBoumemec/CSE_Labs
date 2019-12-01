from control import *

initos = [20, 14, 5, 7, 1, 5]


class Initialazer:

    def __init__(self, inits = initos, regs=1):
        self.init = inits
        self.reg = regs

    def get_initial_parameters(self):
        """
        just getter of initial pams
        :return: initial pams list
        """
        return self.init

    def get_regulator_function(self):
        """
        getter of actual inputted regulator gear function
        :return: regulator gear function
        """
        return self.reg

    def get_scheme_solving(self):
        """
        same as finish_chain but for unlocked CSU
        :param init: gives a freedom in changing of pams
        :return: w6 is a finished chain
        """
        w0 = tf(1,1)

        compW1 = [[self.init[1], 1], [self.init[5], 1]]
        w1 = tf(compW1[0], compW1[1])

        compW2 = [[1], [self.init[2], 1]]
        w2 = tf(compW2[0], compW2[1])

        compW3 = [[0.05 * self.init[4], 1], [0.05 * self.init[2], 1]]
        w3 = tf(compW3[0], compW3[1])

        compW4 = [self.init[0], [self.init[3], 1]]
        w4 = tf(compW4[0], compW4[1])

        w5 = series(w2, w3, w4, w1, self.reg)

        w6 = feedback(w5, w0, -1)

        return w6
