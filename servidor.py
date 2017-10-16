import socket
import _thread
import time
import sys
import pacote
from tempo import Tempo
import os
import random

class Servidor():

    def __init__(self, nome_arquivo, tamanho_janela, tempo_espera, tempo_limite, rtt):

        self.HOST = '127.0.0.1'
        self.PORTA = 8291
        self.TAM_PACOTE = 300
        self.TAM_JANELA = tamanho_janela
        self.TEMPO_ESPERA = tempo_espera
        self.TEMPO_LIMITE = tempo_limite
        self.RTT = rtt
        self.lista_tempo = []
        self.nome_arquivo = nome_arquivo

        self.base = 0
        self.mutex = _thread.allocate_lock()
        self.tempo_remetente = Tempo(self.TEMPO_LIMITE)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', 0))

        self.dados = open('lista_servidor.txt', 'w', encoding="utf8")
        self.dados.write("Tamanho Arquivo: " + str(os.path.getsize(self.nome_arquivo)) + " bytes\n")
        self.grafico = open('grafico.txt', 'w', encoding="utf8")

        self.inicio = 0
        self.fim = 0
        self.tempo_atual = 0

    def resposta(self, s):

        while True:
            pct, _ = s.recvfrom(1024)
            ack, _ = pacote.extrair(pct)

            self.dados.write('ACK recebido ' + str(ack) + '\n')
            self.calcular_atraso(ack)
            if ack >= self.base:
                self.mutex.acquire()
                self.base = int(ack) + 1
                self.dados.write('Base atualizada ' + str(self.base) + '\n')
                self.tempo_remetente.stop()
                self.mutex.release()

    def enviar(self):
        self.inicio = time.time()
        try:
            self.arquivo = open(self.nome_arquivo, 'rb')
            self.s.sendto(self.nome_arquivo.encode('ascii'), (self.HOST, self.PORTA))
            self.s.sendto(str(self.RTT).encode('ascii'), (self.HOST, self.PORTA))
        except IOError:
            self.dados.write('Arquivo não encontrado  ' + self.nome_arquivo + '\n')
            sys.exit()

        pacotes = []
        num_sequencia = 0
        while True:
            data = self.arquivo.read(self.TAM_PACOTE)
            if not data:
                break
            pacotes.append(pacote.criar(num_sequencia, data))
            num_sequencia += 1

        num_pacotes = len(pacotes)
        self.dados.write('Recebidos ' + str(num_pacotes) + '\n')
        tam_janela = min(self.TAM_JANELA, num_pacotes - self.base)  # Ajusta a janela
        prox_enviar = 0
        self.base = 0

        _thread.start_new_thread(self.resposta, (self.s,))

        while self.base < num_pacotes:
            self.mutex.acquire()

            # Envia todos os pacotes pela janela
            while prox_enviar < self.base + tam_janela:
                self.s.sendto(pacotes[prox_enviar], (self.HOST, self.PORTA))
                self.fim = time.time()
                self.dados.write('Enviando pacote ' + str(prox_enviar) + '\n')
                self.tempo_atual = self.fim - self.inicio
                self.grafico.write(str(prox_enviar) + ',' + '%f \n' %(self.tempo_atual))
                prox_enviar += 1

            if not self.tempo_remetente.running():
                self.dados.write('Iniciando temporizador\n')
                self.tempo_remetente.start()

            while self.tempo_remetente.running() and not self.tempo_remetente.timeout():
                self.mutex.release()
                self.dados.write('Dormindo\n')
                time.sleep(self.TEMPO_ESPERA)
                self.mutex.acquire()

            if self.tempo_remetente.timeout():
                self.dados.write('Tempo esgotado\n')
                self.tempo_remetente.stop()
                prox_enviar = self.base
            else:
                self.dados.write('Movendo janela\n')
                tam_janela = min(self.TAM_JANELA, num_pacotes - self.base)  # Ajusta a janela
            self.mutex.release()

        self.s.sendto(''.encode('ascii'), (self.HOST, self.PORTA))

        self.arquivo.close()
        self.dados.close()
        self.grafico.close()
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