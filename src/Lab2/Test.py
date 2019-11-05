from src.Lab2 import dictionary
from src.Lab2 import toolBox
from src.Lab2 import newToolBox
from src.Lab2 import gurwitzSpaghetti
from src.Lab2 import NyquistBode
from src.Lab2 import initPamsLab2


# key
b = 5

# b = int(input("Input your desired analyze tool?\n 1 - transition function \n 2 - bode function \n"
#                   " 3 - Nyquist diagram \n 4 - analyzing by all higher tools \n 5 - Gurwitz criterion \n" " :
#                   \n 6 - godoghraph Mihailova"))



dictionary_of_choice = {
        1: newToolBox.newToolBox().get_trans_func,
        2: NyquistBode.Nyquist().get_bode_func,
        3: NyquistBode.Nyquist().get_nyquist_diagram,
        4: newToolBox.newToolBox().all_of_them,
        5: gurwitzSpaghetti.gurwitz_crit,
        6: newToolBox.newToolBox().get_godoghraph,
    }

try:
    dictionary_of_choice[b]()
except KeyError as e:
    raise ValueError('Undefined unit: {}'.format(e.args[0]))
