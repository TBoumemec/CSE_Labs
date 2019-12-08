from control import tf, parallel


class RegulatorBody:

    def __init__(self, k=1, Td=1, Tu=1):
        """
        :param k: proportional coefficient
        :param Td: differential coefficient
        :param Tu: integral coefficient
        """
        self.k = k
        self.Td = Td
        self.Tu = Tu

    def get_regulator_coefficients(self):

        return self.k, self.Td, self.Tu

    def set_regulator_coefficients(self, k=1, Td=1, Tu=1):

        self.k = k
        self.Td = Td
        self.Tu = Tu

    def show_regulator_coefficients(self):
        print("Пропорциональный коэффициент: ", str(self.k))
        print("Дифференциальный коэффициент: ", str(self.Td))
        print("Интегральный коэффициент: ", str(self.Tu))


class ProportionalRegulator(RegulatorBody):
    def get_TrFunc_proportional_regulator(self):
        """
        definition for calculating transmission function of propotrional
        regulator type
        :return: transmission function
        """

        w = tf([0, self.k], [0, 1])
        return w


class PIDRegulator(RegulatorBody):
    def get_TrFunc_pid_regulator(self):
        """
        definition for calculating transmission function of complex PID regulator type
        :return: transmission function
        """

        w1 = tf([0, self.k], [0, 1])
        w2 = tf([self.Td, 0], [0, 1])
        w3 = tf([0, 1], [self.Tu, 0])
        w = parallel(w1, w2, w3)

        return w
