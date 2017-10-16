from tkinter import *
from tkinter import ttk
from cliente import Cliente

class TkCliente(object):

    def __init__(self, instancia):

        instancia.title('Redes de Computadores - CLIENTE')
        instancia.geometry("600x500+380+120")
        self.font = ("Arial", 12)
        self.font2 = ("Arial", 11)

        ''' Frame de instruções '''
        self.frame1 = LabelFrame(instancia, pady = 15, text = "Instruções", font = self.font)
        self.frame1.pack(side = LEFT, expand = "yes", pady = 5, fill = Y)

        try:
            self.bt_inicar = ttk.Button(self.frame1, text = "INICIAR", command = self.iniciar)
            self.bt_inicar.pack(pady = 10)

            self.instrucoes = Label(self.frame1, font = self.font2, text=
                                                                       'Go-Back-N ARQ é uma instância \n '
                                                                       'específica do pedido automático \n '
                                                                       'de repetição (ARQ), o qual \n'
                                                                       'envia processos contínuos com \n '
                                                                       'um número de frames específico \n'
                                                                       'pelo tamanho da janela sem \n'
                                                                       'receber um pacote de confirmação \n'
                                                                       '(ACK) do receptor. É um caso \n'
                                                                       'especial do protocolo de \n'
                                                                       'janela deslizante que transmite \n'
                                                                       'uma janela de tamanho N e recebe \n'
                                                                       'uma janela de tamanho 1.')
        except:
            self.instrucoes = Label(self.frame1, font=self.font2, text= 'ERRO AO INICIAR \n\n'
                                                                       'Go-Back-N ARQ é uma instância \n '
                                                                       'específica do pedido automático \n '
                                                                       'de repetição (ARQ), o qual \n'
                                                                       'envia processos contínuos com \n '
                                                                       'um número de frames específico \n'
                                                                       'pelo tamanho da janela sem \n'
                                                                       'receber um pacote de confirmação \n'
                                                                       '(ACK) do receptor. É um caso \n'
                                                                       'especial do protocolo de \n'
                                                                       'janela deslizante que transmite \n'
                                                                       'uma janela de tamanho N e recebe \n'
                                                                       'uma janela de tamanho 1.')
        self.instrucoes.pack()

        ''' Frama Resultados '''
        self.frame2 = LabelFrame(instancia, text="Resultados", font = self.font)
        self.frame2.pack(side = LEFT, expand = 1, pady = 5, fill = 'both')

        self.scrollbar = ttk.Scrollbar(self.frame2)
        self.scrollbar.pack(side = RIGHT, fill = 'both')

        self.lista = Listbox(self.frame2, yscrollcommand = self.scrollbar.set, font = self.font)
        self.scrollbar.config(command = self.lista.yview)

    def iniciar(self):
        cliente = Cliente()
        for linha in open('lista_cliente.txt', 'r'):
            self.lista.insert(END, linha.strip())
        self.lista.pack(side = LEFT, fill = 'both', expand = 1)

''' Instancia '''
instancia = Tk()
TkCliente(instancia)
instancia.mainloop()



