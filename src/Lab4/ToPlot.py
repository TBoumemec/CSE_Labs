from control.matlab import step
from control import *
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go

def plot_trans_func(w, toFindT=False, toPlotTrans=False):
    """
    функция находит и возвращает период переходной характеристики
    """
    t = np.linspace(0, stop=100, num=2000)

    y1, t1 = step(w, t)

    t=list(t)

    if toPlotTrans:
        plt.plot(t, y1, "r")
        plt.title('Step Response')
        plt.ylabel('Amplitude  h(t)')
        plt.xlabel('Time(sec)')
        plt.grid(True)
        plt.show()

    if toFindT:
        two_maxes = []

        for num in range(len(y1[1:-1])):
            if y1[num - 1] < y1[num] > y1[num + 1]:
                two_maxes.append(num)
            if len(two_maxes) == 2: break

        return t[two_maxes[1]] - t[two_maxes[0]]


def plot_3d(Kp, Kd, Ku):
    """
    Функция построения 3д диаграмм рассеивания. Взята с:
    https://github.com/ostwalprasad/PythonMultiDimensionalPlots/tree/master/src
    :param Kp: пропорциональный коэффициент
    :param Kd: дифференциальный коэффициент
    :param Ku: интегральный коэффициент
    """

    fig1 = go.Scatter3d(x=Kp, y=Kd, z=Ku,
                        marker=dict(
                            opacity=0.9, reversescale=True, colorscale='Blues', size=5),
                        line=dict(width=0.02), mode='markers')

    mylayout = go.Layout(scene=dict(xaxis=dict(title="Кп"),
                                    yaxis=dict(title="Kd"),
                                    zaxis=dict(title="Ku")), )

    plotly.offline.plot({"data": [fig1], "layout": mylayout},
                        auto_open=True, filename=("3DPlot.html"))
