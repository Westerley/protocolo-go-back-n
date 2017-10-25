import socket
import sys
import random
import time
import math

class Cliente():

    def __init__(self):

        self.HOST = '127.0.0.1'
        self.PORTA = 8291

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST, self.PORTA))
        self.dados = open('lista_cliente.txt', 'w', encoding="utf8")
        self.lista_tempo = []
        self.RTT = 0
        self.media = 0

        self.inicio = 0
        self.fim = 0
        self.tempo_atual = 0

        try:
            msg = self.s.recvfrom(1024)
            msg_rtt = self.s.recvfrom(1024)
            msg_media = self.s.recvfrom(1024)
            self.RTT = float(msg_rtt[0].decode('ascii'))
            self.media = float(msg_media[0].decode('ascii'))
            self.inicio = time.time()
            nome_arquivo = str(msg[0].decode('ascii')).split('/')
            nome_arquivo = nome_arquivo[len(nome_arquivo) - 1]
            nome_arquivo = 'copy_' + nome_arquivo
            arquivo = open(nome_arquivo, 'wb')
        except IOError:
            self.dados.write('Arquivo não encontrado\n')
            sys.exit()

        num_esperado = 0
        while True:
            pct, endereco = self.s.recvfrom(1024)
            if not pct:
                break
            num_sequencia = int.from_bytes(pct[0:4], byteorder = 'little', signed = True)
            data = pct[4:]
            self.dados.write('Pacote recebido ' + str(num_sequencia) + '\n')
            self.fim = time.time()
            self.tempo_atual = self.fim - self.inicio

            if num_sequencia == num_esperado:
                self.dados.write('Pacote recebido é igual ao pacote esperado\n')
                self.dados.write('Enviando ACK de confirmação ' + str(num_esperado) + '\n')
                pct = num_esperado.to_bytes(4, byteorder = 'little', signed = True)
                self.calcular_atraso(num_sequencia)
                self.s.sendto(pct, endereco)
                num_esperado += 1
                arquivo.write(data)
            else:
                self.dados.write('Enviando ACK esperado ' + str(num_esperado - 1) + '\n')
                pct = (num_esperado - 1).to_bytes(4, byteorder = 'little', signed = True)
                self.s.sendto(pct, endereco)

        arquivo.close()
        self.s.close()

    def calcular_atraso(self, segmento):
        X = -(self.media) * math.log(random.random(), math.e)
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