from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as mensagem
from functools import partial
import matplotlib.animation as animation
from tkinterGrafico import Grafico
from servidor import Servidor

class TkServidor(object):

    def __init__(self, instancia):
        instancia.title('Redes de Computadores - SERVIDOR')
        instancia.geometry("600x500+380+120")
        self.font = ("Arial", 12)
        self.font2 = ("Arial", 11)

        ''' Menu '''
        menu = Menu(instancia, font = self.font)
        instancia.config(menu = menu)
        arquivo = Menu(menu)
        arquivo.add_command(label = 'Mostrar Gráfico', command = self.abrir_grafico, font = self.font)
        arquivo.add_command(label = 'Exit', command = lambda: exit(), font = self.font)
        menu.add_cascade(label = 'Arquivo', menu = arquivo)

        ''' Frame de Configurações '''
        self.frame2 = LabelFrame(instancia, pady = 5, text="Configurações", font = self.font)
        self.frame2.pack(side = LEFT, expand="yes", pady = 5, padx = 5, fill = 'both')

        self.texto_janela = ttk.Label(self.frame2, text = 'Janela', font = self.font)
        self.texto_janela.pack()
        self.janela = Spinbox(self.frame2, from_ = 1, to = 100, font = self.font)
        self.janela.pack(pady = 10, padx = 30)

        self.texto_probabilidade = ttk.Label(self.frame2, text = 'Probabilidade (p)', font = self.font)
        self.texto_probabilidade.pack()
        self.probabilidade = Spinbox(self.frame2, from_ = 0, to = 100, increment = 0.05, font = self.font)
        self.probabilidade.pack(pady = 10)

        self.texto_tempo_limite = ttk.Label(self.frame2, text = 'Timeout', font = self.font)
        self.texto_tempo_limite.pack()
        self.tempo_limite = Spinbox(self.frame2, from_ = 0, to = 100, increment = 0.05, font = self.font)
        self.tempo_limite.pack(pady = 10)

        self.texto_rtt = ttk.Label(self.frame2, text = 'RTT', font = self.font)
        self.texto_rtt.pack()
        self.rtt = Spinbox(self.frame2, from_ = 0, to = 100, increment = 0.05, font = self.font)
        self.rtt.pack(pady = 10)

        self.texto_media = ttk.Label(self.frame2, text = 'Média E[X]', font = self.font)
        self.texto_media.pack()
        self.media = Spinbox(self.frame2, from_ = 0, to = 100, increment = 0.05, font = self.font)
        self.media.pack(pady = 10)

        self.lb_arquivo = ttk.Label(self.frame2)
        self.lb_arquivo.pack()
        self.bt_arquivo = ttk.Button(self.frame2, text = 'ABRIR ARQUIVO')
        self.bt_arquivo['command'] = partial(self.abrir_arquivo, self.lb_arquivo)
        self.bt_arquivo.pack(pady = 10)

        self.bt_enviar = ttk.Button(self.frame2, text="ENVIAR", command = self.obter_dados)
        self.bt_enviar.pack(pady = 10)

        ''' Frama Resultados '''
        self.frame3 = LabelFrame(instancia, text="Resultados", font = self.font)
        self.frame3.pack(expand = 1, pady = 5, padx = 5, fill = 'both')

        self.scrollbar = ttk.Scrollbar(self.frame3)
        self.scrollbar.pack(side = RIGHT, fill = 'both')

        self.lista = Listbox(self.frame3, yscrollcommand = self.scrollbar.set, font = self.font2)
        self.scrollbar.config(command = self.lista.yview)

        ''' Frame de instruções '''
        self.frame1 = LabelFrame(instancia, pady = 15, text = "Instruções", font = self.font)
        self.frame1.pack(side = LEFT, pady = 5, padx = 5, fill = 'both')

        self.instrucoes = Label(self.frame1, font = self.font2, text=
                                                '* Antes de enviar o arquivo, inicie \n '
                                                'o serviço do cliente.\n\n'
                                                '* Definir os parâmetros de entrada \n'
                                                'antes de enviar o arquivo.\n\n'
                                                '* Extensões testadas: .txt .pdf .jpg.')
        self.instrucoes.pack(expand = 1)

    def abrir_grafico(self):
        grafico = Grafico()
        an = animation.FuncAnimation(grafico.f, grafico.popula_dados, interval = 1000)
        grafico.mainloop()

    def abrir_arquivo(self, lb_arquivo):
        try:
            nome = askopenfilename(initialdir="C:/",
                                   filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                                   title="Escolher arquivo"
                                   )

            self.lb_arquivo['text'] = nome
        except:
            lb_arquivo['text'] = "Erro ao abrir arquivo"

    def obter_dados(self):
        servidor = Servidor(self.lb_arquivo['text'], int(self.janela.get()), float(self.probabilidade.get()), float(self.tempo_limite.get()), float(self.rtt.get()), float(self.media.get()))
        servidor.enviar()

        for linha in open('lista_servidor.txt', 'r'):
            self.lista.insert(END, linha.strip())
        self.lista.pack(side = LEFT, fill = 'both', expand = 1)

        mensagem.showinfo("Aviso", "Processo concluido")

''' Instancia '''
instancia = Tk()
TkServidor(instancia)
instancia.mainloop()




