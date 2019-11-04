" function with initial pams"

def init_pam():
    k = [3, 1, 0, 0, 3]
    T = [0, 4, 5, 2, 2]


    # pams for ploting ideal differentiator bode: num = [T[3], 0]; denum = [1e-20, 1]
    # pams for ploting ideal differentiator step and impulse: num = [T[3], 0]; denum = [1e-3, 1]
    #
    numer = [[0, k[0]], [0, k[1]], [k[2], 1], [T[3], 0], [k[4], 0]]
    denumer = [[T[0], 1], [T[1], 1], [T[2], 0], [1e-20, 1], [T[4], 1]]

    k = [i * 2 for i in k]
    T = [i * 2 for i in T]

    numer2 = [[0, k[0]], [0, k[1]], [k[2], 1], [T[3], 0], [k[4], 0]]
    denumer2 = [[T[0], 1], [T[1], 1], [T[2], 0], [1e-20, 1], [T[4], 1]]
    return (numer, denumer, numer2, denumer2)