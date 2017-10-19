"""
Arquivo responsavel por gerar o gráfico dos resultados
Deve-se adicionar o arquivo.txt gerado ao transferir o arquivo
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df4 = pd.read_table('rtt20.txt', delimiter=',', names=('Pacote', 'Tempo'))
df8 = pd.read_table('rtt40.txt', delimiter=',', names=('Pacote', 'Tempo'))
df12 = pd.read_table('rtt60.txt', delimiter=',', names=('Pacote', 'Tempo'))
df16 = pd.read_table('rtt80.txt', delimiter=',', names=('Pacote', 'Tempo'))
df20 = pd.read_table('rtt100.txt', delimiter=',', names=('Pacote', 'Tempo'))

plt.plot(np.array(df4["Pacote"]), np.array(df4["Tempo"]), linestyle='--', color='red', label = 'RTT: 0.20')

plt.plot(np.array(df8["Pacote"]), np.array(df8["Tempo"]), linestyle=':', color='blue', label = 'RTT: 0.40')

plt.plot(np.array(df12["Pacote"]), np.array(df12["Tempo"]), linestyle='-.', color='black', label = 'RTT: 0.60')

plt.plot(np.array(df16["Pacote"]), np.array(df16["Tempo"]), linestyle='-', color='orange', label = 'RTT: 0.80')

plt.plot(np.array(df20["Pacote"]), np.array(df20["Tempo"]), linestyle='--', color='green', label = 'RTT: 1')

plt.title("Tempo de Transferência vs. Pacote")
plt.xlabel('Pacote')
plt.ylabel('Tempo de Transferência (segundos)')
plt.legend()
plt.show()

