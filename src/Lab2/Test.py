from src.Lab2 import dictionary
from src.Lab2 import toolBox
from src.Lab2 import newToolBox
from src.Lab2 import gurwitzSpaghetti


# key
b = 5

# b = int(input("Input your desired analyze tool?\n 1 - transition function \n 2 - bode function \n"
#                   " 3 - Nyquist diagram \n 4 - analyzing by all higher tools \n 5 - Gurwitz criterion \n" " : "))



dictionary_of_choice = {
        1: newToolBox.newToolBox().get_trans_func,
        2: newToolBox.newToolBox().get_bode_func,
        3: newToolBox.newToolBox().get_nyquist_diagram,
        4: newToolBox.newToolBox().all_of_them,
        5: gurwitzSpaghetti.gurwitz_crit,
    }

try:
    dictionary_of_choice[b]()
except KeyError as e:
    raise ValueError('Undefined unit: {}'.format(e.args[0]))
