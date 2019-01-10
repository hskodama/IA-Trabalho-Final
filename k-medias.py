'''
Filename: c:\cygwin64\home\Shinki\datasets\k-medias.py
Path: c:\cygwin64\home\Shinki\datasets
Created Date: Sunday, January 6th 2019, 10:43:47 pm
Author: Henrique Kodama, Carlos Tadeu, Vinicius Salinas, Bruno Peres

Copyright (c) 2019 Your Company
'''

import random
import numpy as np
import matplotlib.pyplot as plot
import random
import math

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
        aux = float("inf")
        distance = 0.0

        # Para todo centroide calcula a distancia euclidiana entre o ponto e os centroides
        for j in range(len(centroids_X)):
            distance = math.sqrt((dots_X[i] - centroids_X[j])**2 + (dots_Y[i] - centroids_Y[j])**2)
            if(distance < aux):
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
            distance = math.sqrt((dots_X[i] - centroids_X[j])**2 + (dots_Y[i] - centroids_Y[j])**2)
            if(distance < aux):
                aux = distance
                closest_centroid_index = j
        
        if(closest_centroid[i] != closest_centroid_index):
            centroid_changed = 1
        closest_centroid[i] = closest_centroid_index
    
    return centroid_changed

def main():
    # dots_X contem as coordenadas X dos pontos
    # dots_Y contem as coordenadas Y dos pontos
    # centroids_X contem as coordenadas X dos centroides declarados randomicamente
    # centroids_Y contem as coordenadas Y dos centroides declarados randomicamente
    # closest_centroid contem o numero do centroide mais proximo do ponto em dada iteracao (0, 1, .... , N)
    # i e utilizado como auxiliar
    # run e usado para verificar o loop do algoritmo
    dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid = ([] for i in range(5))
    i = 0
    run = 1

    # Pergunta o arquivo desejado e espera a quantidade de clusters desejados
    print(""" 
    1. c2ds1-2sp.txt
    2. c2ds3-2g.txt
    3. monkey.txt
    """)

    option = int(raw_input("Enter the option: "))
    N_clusters = int(raw_input("Enter the number of clusters (Max. 8): "))

    if(option == 1):
        file_name = "c2ds1-2sp.txt"
    elif(option == 2):
        file_name = "c2ds3-2g.txt"
    elif(option == 3):
        file_name = "monkey.txt"

    # Abertura do arquivo como leitura
    read = open(file_name, 'r')

    # Leitura dos dados. Vale notar que os dados estao com '.' em vez de ',' portanto e necessario modificar
    for line in read:
        newline = line.rstrip("\n").split("\t")
        newline[1].replace(".", ",")
        newline[2].replace(".", ",")
        if(i != 0):
            dots_X.append(float(newline[1]))
            dots_Y.append(float(newline[2]))
        i = i + 1
    read.close()

    # Determinacao das coordenadas dos clusters aleatoriamente
    for i in range(N_clusters):
        centroids_X.append(round(random.uniform(min(dots_X), max(dots_X)), 4))
        centroids_Y.append(round(random.uniform(min(dots_Y), max(dots_Y)), 4))

    initialize(dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid)

    # Loop principal do algoritmo
    while(run):
        run = group(dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid)

    # Determina o limite de X e Y do grafico
    plot.ylim(min(dots_X) - 1, max(dots_X) + 1)
    plot.xlim(min(dots_Y) - 1, max(dots_Y) + 1)

    # Plota os pontos e atribui a cor ao centroide correspondente
    for i in range(len(dots_X)):
        plot.plot(dots_X[i], dots_Y[i], colors[closest_centroid[i]], markersize=1)

    # Plota os centroides como estrelas
    for i in range(len(centroids_X)):
        plot.plot(centroids_X[i], centroids_Y[i], centroid_color[i], markersize=10)

    # Plota o grafico
    plot.show()

if __name__== "__main__":
    main()
