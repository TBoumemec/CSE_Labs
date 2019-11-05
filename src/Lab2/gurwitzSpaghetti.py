from control import tfdata, np
from numpy.linalg import det
from numpy.ma import arange

from src.Lab2 import initPamsLab2
from src.Lab2 import toolBox
from src.Lab2 import newToolBox
from src.Lab2 import NyquistBode


def gurwitz_crit():
    w = initPamsLab2.calc_w()

    matrix = formating_matrix(w)

    for i in range(len(matrix), 0, -1):
        opr = det(matrix[:i, :i])
        print("det of", i, "matrix: ", opr)
        if opr < 0:
            print("ne ust")
            break

    a = 0

    inits = initPamsLab2.init_pams()

    for i in arange(1.3936, 1.3937, 0.00001):
        inits[1] = i

        w = initPamsLab2.finish_chain(inits)
        matrix = formating_matrix(w)
        opr = det(matrix[:len(matrix) - 1, :len(matrix) - 1])

        print("det", opr, "Koc:", i) if - 2 <= opr <= 2 else "no"


    listA = [inits[1] - 5, inits[1], inits[1] + 5]
    for i in range(3):

        initis = initPamsLab2.init_pams()
        initis[1] = listA[i]
        print(initis[1])
        w = initPamsLab2.finish_chain(initis)
        newToolBox.newToolBox.all_of_them(w)
        w1 = initPamsLab2.finish_for_nyquist(initis)
        NyquistBode.Nyquist.all_of_them(w1)
        # Nyquist.Nyquist.get_nyquist_diagram(w1)


# def critical_number(init):
#
#     w = initPamsLab2.finish_chain(init)
#
#     num, denum = tfdata(w)
#     # num = num[0][0][:]
#     denum = denum[0][0][:]


def formating_matrix(w):
    num, denum = tfdata(w)
    # num = num[0][0][:]
    denum = denum[0][0][:]

    matrix = np.zeros((len(denum) - 1, len(denum) - 1))
    a1 = 0

    for i in range(len(denum) - 1):
        if i % 2 == 0:
            a = int((i + 1) // 2)

            a1 = a

        else:
            a = a1

        for j in range(len(denum)):

            if (j % 2) != (i % 2):
                matrix[i, a] = denum[j]
                # print(a)
                # print(matrix)
                a += 1

    # print(matrix)

    return matrix
