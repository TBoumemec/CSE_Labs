from control import *
from src.Lab3.Regulator import ProportionalRegulator


class SchemeBody:

    def __init__(self, inits=[20, 14, 5, 7, 1, 5], regs_w=ProportionalRegulator().get_TrFunc_proportional_regulator()):
        """
        :param inits: matrix of initial parameters
        :param regs_w: transmittion function of regulator
        """
        self.init = inits
        # unchanging parameter
        self.regs_w = regs_w

    def get_initial_parameters(self):
        return self.init

    def get_regulator_function(self):
        return self.regs_w

    def get_scheme_solving(self):
        """
        Calculating transmission function for locked CSU;
        Should be changed dependently of research scheme.
        :param init: gives a freedom in changing of pams
        :return: w6 is a finished chain transmission func
        """
        w0 = tf(1, 1)

        compW1 = [[self.init[1], 1], [self.init[5], 1]]
        w1 = tf(compW1[0], compW1[1])

        compW2 = [[1], [self.init[2], 1]]
        w2 = tf(compW2[0], compW2[1])

        compW3 = [[0.05 * self.init[4], 1], [0.05 * self.init[2], 1]]
        w3 = tf(compW3[0], compW3[1])

        compW4 = [self.init[0], [self.init[3], 1]]
        w4 = tf(compW4[0], compW4[1])

        w5 = series(w2, w3, w4, w1, self.regs_w)

        w6 = feedback(w5, w0, -1)

        return w6
