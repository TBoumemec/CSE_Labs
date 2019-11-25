" function with main active motion"

from src.Lab1 import functions


def graf():
    a = int(input("There is a list of chains:\n0 - inertialess chain\n" +
                  "1 - aperiodic chain\n2 - integral chain\n3 - perfect differentiator chain\n" +
                  "4 - real differentiator chain\n"  
                  "Input number of link: "))

    b = int(input("Input your desired graph?\n 1 - transition function. \n 2 - impulse function \n"
                  " 3 - Bode function \n 4 - all of them \n" " : "))

    dictionary_of_choice = {
        1: functions.trans_func,
        2: functions.imp_func,
        3: functions.bode_func,
        4: functions.all_func,
    }

    try:
        f = dictionary_of_choice[b](a)
    except KeyError as e:
        raise ValueError('Undefined unit: {}'.format(e.args[0]))

    return
