# Protocolo-go-back-n

## Trabalho realizado para a disciplina de redes de computadores

O trabalho proposto tem como objetivo implementar um protocolo
confiável tipo Go-Back-N para transferência de arquivos, utilizando
o protocolo da camada de transporte UDP para estabelecer uma
conexão entre processos. Para simular perdas de pacotes foi
requisitado uma função para simular atrasos na rede para o
recebimento de ack e  mensagens. Também deve-se implementar
uma função  que escolhe se o pacote será entregue ou não.
Isto é, um pacote é perdido com probabilidade p.

<img src="imagens/imagem.png" width="850" height="400">

## Módulos

* Python >= 3.5
* tkinter, matplotlib, socket, time, sys, os, random, math, _thread, numpy, pandas

## Execução

* [Recomendável] Executar o arquivo tkinterCliente.py
* [Recomendável] Executar o arquivo tkinterServidor.py

OU

* Criar o arquivo executável com pyInstaller. Ex.: pyinstaller tkinterCliente; pyinstaller tkinterServidor

## Ambiente

* Linux - Ubuntu 16.04


