import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pacote = [4619, 4619, 4619, 4619, 4619]
tempo = [104.794350, 112.279248, 112.039556, 106.722737, 114.455940]

xLista = [0.20, 0.40, 0.60, 0.80, 1]
yLista = []
for i in range(len(tempo)):
    yLista.append(pacote[i] / tempo[i])

plt.plot(xLista, yLista, linestyle='--', color='blue', marker = 's')

plt.title("Throughput vs. RTT")
plt.xlabel('RTT')
plt.ylabel('Throughput (Pacotes por Segundo)')
plt.show()

