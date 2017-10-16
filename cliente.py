import socket
import sys
import pacote
import random
import time

class Cliente():

    def __init__(self):

        self.HOST = '127.0.0.1'
        self.PORTA = 8291

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST, self.PORTA))
        self.dados = open('lista_cliente.txt', 'w', encoding="utf8")
        self.lista_tempo = []
        self.RTT = 0

        self.inicio = 0
        self.fim = 0
        self.tempo_atual = 0

        try:
            msg = self.s.recvfrom(1024)
            msg_rtt = self.s.recvfrom(1024)
            self.RTT = float(msg_rtt[0].decode('ascii'))
            self.inicio = time.time()
            nome_arquivo = str(msg[0].decode('ascii')).split('/')
            nome_arquivo = nome_arquivo[len(nome_arquivo) - 1]
            nome_arquivo = 'copy_' + nome_arquivo
            arquivo = open(nome_arquivo, 'wb')
        except IOError:
            print('Não foi possivel salvar o arquivo!')
            sys.exit()

        num_esperado = 0
        while True:
            pct, endereco = self.s.recvfrom(1024)
            if not pct:
                break
            num_sequencia, data = pacote.extrair(pct)
            self.dados.write('Pacote recebido ' + str(num_sequencia) + '\n')
            self.fim = time.time()
            self.tempo_atual = self.fim - self.inicio
            self.calcular_atraso(num_sequencia)

            if num_sequencia == num_esperado:
                self.dados.write('Sequencia/Pacote esperado = ' + str(num_sequencia) + '\n')
                self.dados.write('Enviando ACK ' + str(num_esperado) + '\n')
                pct = pacote.criar(num_esperado)
                self.s.sendto(pct, endereco)
                num_esperado += 1
                arquivo.write(data)
            else:
                self.dados.write('Enviando ACK ' + str(num_esperado - 1) + '\n')
                pct = pacote.criar(num_esperado - 1)
                self.s.sendto(pct, endereco)

        arquivo.close()
        self.s.close()

    def calcular_atraso(self, segmento):
        X = random.expovariate(10)
        atraso = (self.RTT / 2) + X
        tn = self.tempo_atual + atraso
        elemento = (tn, segmento)
        if len(self.lista_tempo) != 0:
            self.lista_tempo = sorted(self.lista_tempo)
            if elemento < self.lista_tempo[0]:
                self.lista_tempo[0] = elemento
                time.sleep(tn)
            else:
                self.lista_tempo.append((tn, segmento))
        else:
            self.lista_tempo.append((tn, segmento))