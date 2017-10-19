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

    def popula_dados(self, i):
        arquivo = open("grafico.txt", "r").read()
        lista = arquivo.split('\n')
        xLista = []
        yLista = []
        for linha in lista:
            if len(linha) > 1:
                x, y = linha.split(',')
                xLista.append(int(x))
                yLista.append(float(y))

        self.a.clear()
        self.a.plot(xLista, yLista, color='black')
        self.a.set_title("Tempo de Transferência vs. Pacote", fontsize="12")
        self.a.set_xlabel('Pacote')
        self.a.set_ylabel('Tempo de Transferência (segundos)')

