import numpy as np
from control import *
from numpy.linalg import det

from src.Lab2 import toolBox
from src.Lab2 import initPamsLab2


# w = initPamsLab2.finish_chain()
# print(w)

# key
b = 4


# b = int(input("Input your desired analyze tool?\n 1 - transition function \n 2 - bode function \n"
#                   " 3 - Nyquist diagram \n 4 - Gurwitz criterion \n" " : "))

dictionary_of_choice = {
    1: toolBox.trans_func,
    2: toolBox.bode_func,
    3: toolBox.nyquist_diagram,
    4: toolBox.gurwitz_crit,
}

try:
    f = dictionary_of_choice[b]()
except KeyError as e:
    raise ValueError('Undefined unit: {}'.format(e.args[0]))







