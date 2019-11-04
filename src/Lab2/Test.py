import numpy as np
from control import *
import matplotlib.pyplot as plt
from control.matlab import step
from numpy.linalg import det

w0 = tf(1, 1)

compW1 = [[48, 1], [1, 0]]
w1 = tf(compW1[0], compW1[1])

compW2 = [[1], [0.1, 1]]
w2 = tf(compW2[0], compW2[1])

compW3 = [[1], [5, 1]]
w3 = tf(compW3[0], compW3[1])

w4 = series(w1, w2)
w5 = feedback(w4, 1 / w1, -1)
w6 = parallel(1 / w4, 1 / w3)
w7 = series(w6, w5)
w8 = parallel(w7, -w0)
w9 = feedback(w3, w8, -1)
w10 = series(w9, w7)

print(w10)
y, x = step(w10)
plt.plot(x, y, "r")
plt.title('Step Resonance')
plt.ylabel('Amplitude  h(t)')
plt.xlabel('t(с)')
plt.grid(True)
plt.show()

real, imag, freq = nyquist(w10, labelFreq=10)
plt.title('Nyquist Diagram')
plt.plot()
plt.show()

poles = pole(w10)
print(poles)
pole, zeros = pzmap(w10)
plt.title('Graph of poles')
plt.plot()
plt.show()


num, denum = tfdata(w10)
num = num[0][0][:]
denum = denum[0][0][:]

matrix = np.zeros((len(denum) - 1, len(denum) - 1))
a1 = 0

for i in range(len(denum) - 1):
    if (i + 1) % 2 != 0:
        a = int((i + 1) // 2)
        a1 = a

    else:
        a = a1

    for j in range(len(denum) - 1):
        if (j % 2) == (i % 2):
            matrix[i][a] = denum[j]
            a += 1


for i in range((len(matrix)), -1, -1):
    opr = det(matrix[:i, :i])
    print(opr)
    # if opr < 0:
    #     print("ne ust")
    #     break