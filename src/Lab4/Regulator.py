from random import random

from control import tf, parallel
from src.Lab3.Regulator import RegulatorBody


class GeneticPIDRegulatorBody(RegulatorBody):

    def set_random_regs(self, n1=0.01, n2=5):
        """
        setter of random coefficients
        :param n1: from...
        :param n2: to...
        """

        self.k = random.uniform(n1, n2)
        self.Td = random.uniform(n1, n2)
        self.Tu = random.uniform(n1, n2)
