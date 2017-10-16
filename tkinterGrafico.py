from tkinter import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
style.use("ggplot")

class Grafico(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        Tk.wm_title(self, "Redes de Computadores")

        self.f = Figure(figsize=(7, 4), dpi=85)
        self.a = self.f.add_subplot(111)

        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand=True)

    def animate(self, i):
        pullData = open("grafico.txt", "r").read()
        dataList = pullData.split('\n')
        xList = []
        yList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                xList.append(int(x))
                yList.append(float(y))

        self.a.clear()
        self.a.plot(xList, yList, color='black')
        self.a.set_title("Tempo Percorrido vs. Pacote", fontsize="12")
        self.a.set_xlabel('Pacote')
        self.a.set_ylabel('Tempo de Transferência (segundos)')

