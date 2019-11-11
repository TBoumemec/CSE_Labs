from control import stability_margins

from src.Lab2 import newToolBox
from src.Lab2 import gurwitzSpaghetti
from src.Lab2 import NyquistBode,initPamsLab2

"""
main file with user choice keys
"""

# key
b = 6
# b = int(input("Input your desired analyze tool?\n 1 - transition function \n 2 - bode function \n"
#                   " 3 - Nyquist diagram \n 4 - analyzing by all higher tools \n 5 - Gurwitz criterion \n"
#                   " 6 - godoghraph Mihailova \n 7 - poles analyzing \n :"))


dictionary_of_choice = {
        1: newToolBox.newToolBox().get_trans_func,
        2: NyquistBode.NyquistBode().get_bode_func,
        3: NyquistBode.NyquistBode().get_nyquist_diagram,
        4: newToolBox.newToolBox().all_of_them,
        5: gurwitzSpaghetti.gurwitz_crit,
        6: newToolBox.newToolBox().get_godoghraph,
        7: newToolBox.newToolBox().get_poles_analyze,
    }

try:
    dictionary_of_choice[b]()
except KeyError as e:
    raise ValueError('Undefined unit: {}'.format(e.args[0]))
