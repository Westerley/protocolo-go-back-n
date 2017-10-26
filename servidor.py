import socket
import _thread
import time
import sys
import os
import random
import math

class Servidor():

    TEMPO_PARADA = -1

    def __init__(self, nome_arquivo, tamanho_janela, probabilidade, tempo_limite, rtt, media):

        self.HOST = '127.0.0.1'
        self.PORTA = 8291
        self.TAM_PACOTE = 300
        self.TAM_JANELA = tamanho_janela
        self.TEMPO_LIMITE = tempo_limite
        self.RTT = rtt
        self.media = media
        self.probabilidade = probabilidade
        self.lista_tempo = []
        self.nome_arquivo = nome_arquivo
        self.iniciar_tempo = self.TEMPO_PARADA

        self.base = 0
        self.thread = _thread.allocate_lock()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', 0))

        self.dados = open('lista_servidor.txt', 'w', encoding="utf8")
        self.dados.write("Tamanho Arquivo: " + str(os.path.getsize(self.nome_arquivo)) + " bytes\n")
        self.grafico = open('grafico.txt', 'w', encoding="utf8")

        self.tempo_inicio = 0
        self.tempo_fim = 0
        self.tempo_atual = 0

    def enviar(self):
        self.tempo_inicio = time.time()
        try:
            self.arquivo = open(self.nome_arquivo, 'rb')
            self.s.sendto(self.nome_arquivo.encode('ascii'), (self.HOST, self.PORTA))
            self.s.sendto(str(self.RTT).encode('ascii'), (self.HOST, self.PORTA))
            self.s.sendto(str(self.media).encode('ascii'), (self.HOST, self.PORTA))
        except IOError:
            self.dados.write('Arquivo não encontrado  ' + self.nome_arquivo + '\n')
            sys.exit()

        pacotes = []
        num_sequencia = 0
        while True:
            data = self.arquivo.read(self.TAM_PACOTE)
            if not data:
                break
            pacotes.append(num_sequencia.to_bytes(4, byteorder = 'little', signed = True) + data)
            num_sequencia += 1

        num_pacotes = len(pacotes)
        self.dados.write('Recebidos ' + str(num_pacotes) + '\n')
        tam_janela = min(self.TAM_JANELA, num_pacotes - self.base)
        prox_enviar = 0
        self.base = 0

        _thread.start_new_thread(self.resposta, (self.s,))

        while self.base < num_pacotes:
            self.thread.acquire()

            while prox_enviar < self.base + tam_janela:
                if not self.probabilidade_perda():
                    try:
                        self.s.sendto(pacotes[prox_enviar], (self.HOST, self.PORTA))
                        self.dados.write('Enviando pacote ' + str(prox_enviar) + '\n')
                        self.tempo_fim = time.time()
                        self.tempo_atual = self.tempo_fim - self.tempo_inicio
                        self.grafico.write(str(prox_enviar) + ',' + '%f \n' %(self.tempo_atual))
                    except IOError:
                        sys.exit()
                prox_enviar += 1

            if not self.verifica_execucao():
                self.dados.write('Iniciando temporizador\n')
                self.iniciar_tempo = time.time()

            while self.verifica_execucao() and not self.verifica_timeout():
                self.thread.release()
                self.dados.write('Aguardando ...\n')
                time.sleep(0.05)
                self.thread.acquire()

            if self.verifica_timeout():
                self.dados.write('Tempo esgotado\n')
                self.iniciar_tempo = self.TEMPO_PARADA
                prox_enviar = self.base
            else:
                self.dados.write('Movendo janela\n')
                tam_janela = min(self.TAM_JANELA, num_pacotes - self.base)

            self.thread.release()

        self.s.sendto(''.encode('ascii'), (self.HOST, self.PORTA))

        self.arquivo.close()
        self.dados.close()
        self.grafico.close()
        self.s.close()

    def resposta(self, s):
        while True:
            pct, _ = s.recvfrom(1024)
            ack = int.from_bytes(pct[0:4], byteorder = 'little', signed = True)

            self.dados.write('ACK recebido ' + str(ack) + '\n')
            self.calcular_atraso(ack)
            if ack >= self.base:
                self.thread.acquire()
                self.base = int(ack) + 1
                self.dados.write('Base atualizada ' + str(self.base) + '\n')
                self.iniciar_tempo = self.TEMPO_PARADA
                self.thread.release()

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

    def probabilidade_perda(self):
        valor = random.random()
        if valor <= self.probabilidade:
            return True
        return False

    def verifica_execucao(self):
        return self.iniciar_tempo != self.TEMPO_PARADA

    def verifica_timeout(self):
        if not self.verifica_execucao():
            return False
        else:
            return time.time() - self.iniciar_tempo >= self.TEMPO_LIMITE
