'''
Filename: c:\cygwin64\home\Shinki\datasets\k-medias.py
Path: c:\cygwin64\home\Shinki\datasets
Created Date: Wednesday, January 16th 2019, 10:20:47 pm
Author: Henrique Kodama, Carlos Tadeu, Vinicius Salinas, Bruno Peres

Copyright (c) 2019 Your Company
'''

import numpy as np
import matplotlib.pyplot as plot
import random
import math
import csv
from sklearn.metrics.cluster import adjusted_rand_score

# Detclaracao do tamanho do grafico, tipo de grafico
plot.rcParams['figure.figsize'] = (16, 9)
plot.style.use('ggplot')
# Declaracao de vetores para auxiliar na coloracao dos pontos
colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
centroid_color = ['b*', 'g*', 'r*', 'c*', 'm*', 'y*', 'k*', 'w*']


# Funcao para inicializar o vetor closest_centroid
def initialize(dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid):
    closest_centroid_index = 0

    # Para todos os pontos, calcula o centroide mais proximo e guarda no vetor closest_centroid
    for i in range(len(dots_X)):
        # aux = infinito (maximo valor de float)
        aux = float("inf")
        distance = 0.0

        # Para todo centroide calcula a distancia euclidiana entre o ponto e os centroides
        for j in range(len(centroids_X)):
            distance = math.sqrt((dots_X[i] - centroids_X[j]) ** 2 + (dots_Y[i] - centroids_Y[j]) ** 2)
            if (distance < aux):
                aux = distance
                closest_centroid_index = j

        closest_centroid.append(closest_centroid_index)


# Funcao para iterar e modificar os centroides conforme forem mudando, implementacao identica ao initialize()
def group(dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid):
    closest_centroid_index = 0
    centroid_changed = 0

    for i in range(len(dots_X)):
        aux = float("inf")
        distance = 0.0

        for j in range(len(centroids_X)):
            distance = math.sqrt((dots_X[i] - centroids_X[j]) ** 2 + (dots_Y[i] - centroids_Y[j]) ** 2)
            if (distance < aux):
                aux = distance
                closest_centroid_index = j

        if (closest_centroid[i] != closest_centroid_index):
            centroid_changed = 1
        closest_centroid[i] = closest_centroid_index

    return centroid_changed


def main():
    # dots_X contem as coordenadas X dos pontos
    # dots_Y contem as coordenadas Y dos pontos
    # centroids_X contem as coordenadas X dos centroides declarados randomicamente
    # centroids_Y contem as coordenadas Y dos centroides declarados randomicamente
    # closest_centroid contem o numero do centroide mais proximo do ponto em dada iteracao (0, 1, .... , N)
    # compare_values eh utilizado para o indice rand ajustado para comparar a similaridade entre clusters
    # i e utilizado como auxiliar
    dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid, compare_values, ARI = ([] for i in range(7))
    i = 0
    run = 1
    k_min = 0 
    k_max = 0

    # Pergunta o arquivo desejado e espera a quantidade de clusters desejados
    print(""" 
    1. c2ds1-2sp.txt (2 - 5 clusters)
    2. c2ds3-2g.txt (2 - 5 clusters)
    3. monkey.txt (5 - 12 clusters)
    """)

    option = int(input("Enter the option: "))
    N_iterations = int(input("Enter the amount of iterations: "))

    if (option == 1):
        file_name = "../../datasets/c2ds1-2sp.txt"
        Realfile_name = "../../datasets/c2ds1-2spReal.clu"
        resultimage_name = "resultado1.png"
        realimage_name = "real1.png"
        k_min = 2
        k_max = 5
    elif (option == 2):
        file_name = "../../datasets/c2ds3-2g.txt"
        Realfile_name = "../../datasets/c2ds3-2gReal.clu"
        resultimage_name = "resultado2.png"
        realimage_name = "real2.png"
        k_min = 2
        k_max = 5
    elif (option == 3):
        file_name = "../../datasets/monkey.txt"
        Realfile_name = "../../datasets/monkeyReal1.clu"
        resultimage_name = "resultado3.png"
        realimage_name = "real3.png"
        k_min = 5
        k_max = 12

    # Leitura dos dados. Vale notar que os dados estao com '.' em vez de ',' portanto e necessario modificar
    # Abertura do arquivo como leitura
    read = open(file_name, 'r')

    for line in read:
        newline = line.rstrip("\n").split("\t")
        newline[1].replace(".", ",")
        newline[2].replace(".", ",")
        if (i != 0):
            dots_X.append(float(newline[1]))
            dots_Y.append(float(newline[2]))
        i = i + 1
    read.close()

    # Abertura do arquivo Real
    read = open(Realfile_name, 'r')

    # Separacao da segunda coluna do arquivo
    for line in read:
        newline = line.rstrip("\n").split("\t")
        compare_values.append(int(newline[1]))

    for j in range(k_min, k_max + 1):
        resultimage_name = "resultado" + str(option) + "_" + str(j) + ".png"
        resultfile_name = "../../Resultados/k-medias_results" + str(option) + ".csv"
        centroids_X = []
        centroids_Y = []
        closest_centroid = []

        # Determinacao das coordenadas dos clusters aleatoriamente
        for i in range(j):
            centroids_X.append(round(random.uniform(min(dots_X), max(dots_X)), 4))
            centroids_Y.append(round(random.uniform(min(dots_Y), max(dots_Y)), 4))

        initialize(dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid)

        # Loop principal do algoritmo
        i = 1
        while (run and i < N_iterations):
            run = group(dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid)
            i = i + 1
            
        ARI.append(adjusted_rand_score(compare_values, closest_centroid))
        # Determina o limite de X e Y do grafico
        plot.xlim(min(dots_X) - 1, max(dots_X) + 1)
        plot.ylim(min(dots_Y) - 1, max(dots_Y) + 1)

        # Plota os pontos e atribui a cor ao centroide correspondente na FIGURA1
        plot.figure(1)
        plot.clf()
        for i in range(len(dots_X)):
            plot.plot(dots_X[i], dots_Y[i], colors[closest_centroid[i] % 8], markersize=1)

        # Plota os centroides como estrelas
        for i in range(len(centroids_X)):
            plot.plot(centroids_X[i], centroids_Y[i], centroid_color[i % 8], markersize=10)
        plot.savefig(resultimage_name, bbox_inches = 'tight')   

        # Plota os pontos para verificacao na FIGURA2
        # plot.figure(2)
        # for i in range(len(dots_X)):
        #     plot.plot(dots_X[i], dots_Y[i], colors[compare_values[i] % 8], markersize=1)
        # plot.savefig(realimage_name, bbox_inches = 'tight')

    with open(resultfile_name, 'w') as csvfile:
        fieldnames = ['N. clusters', 'ARI']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        i = 0
        for i in range (len(ARI)):
            writer.writerow({'N. clusters': i + k_min, 'ARI': ARI[i]})

if __name__ == "__main__":
    main()
