from control import tf, parallel


class Regulator_body:

    def __init__(self, k=1, Td=1, Tu=1):
        """
        constructor
        :param k: proportional coefficient
        :param Td: differential coefficient
        :param Tu: integral coefficient
        """
        self.k = k
        self.Td = Td
        self.Tu = Tu

    def Prop_reg(self):
        """
        definition for calculating transmission function of propotrional
        regulator
        :return: transmission function
        """
        w = tf([0, self.k], [0, 1])
        print(w)
        return w

    def PUD_reg(self):
        """
        definition for calculating transmission function of complex regulator
        :return: transmission function
        """
        w1 = tf([0, self.k], [0, 1])
        w2 = tf([self.Td, 0], [0, 1])
        w3 = tf([0, 1], [self.Tu, 0])
        w = parallel(w1, w2, w3)
        print(w)

        return w
