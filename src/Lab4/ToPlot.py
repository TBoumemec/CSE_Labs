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

    if toPlotTrans:
        plt.plot(t, y1, "r")
        plt.title('Step Response')
        plt.ylabel('Amplitude  h(t)')
        plt.xlabel('Time(sec)')
        plt.grid(True)
        plt.show()

    if toFindT:
        y2 = list(y1)
        t2 = list(t)
        max1 = t2[y2.index(max(y2))]

        #******************
        del t2[0:y2.index(max(y2))]
        del y2[0:y2.index(max(y2))]
        del t2[0:5]
        del y2[0:5]
        # ******************

        max2 = t2[y2.index(max(y2))]
        return max2 - max1


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
