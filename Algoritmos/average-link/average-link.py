
import numpy as np # linear algebra
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt
from scipy.spatial import distance
from sklearn.cluster import AgglomerativeClustering


import scipy.cluster.hierarchy as shc


import math

def main():
    # dots_X contem as coordenadas X dos pontos
    # dots_Y contem as coordenadas Y dos pontos
    dots_X, dots_Y, centroids_X, centroids_Y, closest_centroid = ([] for i in range(5))
    i = 0
    run = 1

    # Pergunta o arquivo desejado
    print(""" 
    1. c2ds1-2sp.txt
    2. c2ds3-2g.txt
    3. monkey.txt
    """)

    option = int(input("Enter the option: "))

    # Intervalo de valores para k (numero de clusters):
    #kMin = int(input("Kmin: "))
    #kMax = int(input("Kmax: "))

    if(option == 1):
        file_name = "datasets/c2ds1-2sp.txt"
    elif(option == 2):
        file_name = "datasets/c2ds3-2g.txt"
    elif(option == 3):
        file_name = "datasets/monkey.txt"

    # Abertura do arquivo como leitura
    read = open(file_name, 'r')

    # Leitura dos dados. Vale notar que os dados estao com '.' em vez de ',' portanto eh necessario modificar:
    X = []
    for line in read:
        aux = []
        newline = line.rstrip("\n").split("\t")
        newline[1].replace(".", ",")
        newline[2].replace(".", ",")
        if(i != 0):
            aux.append(float(newline[1]))
            aux.append(float(newline[2]))
            X.append(aux)
            #np.insert(X, aux)
        i = i + 1
    read.close()
    X = np.array(X)

    cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='average')
    cluster.fit_predict(X)
    #print(cluster.labels_)
    plt.scatter(X[:, 0], X[:, 1], c=cluster.labels_, cmap='rainbow')

    plt.figure(figsize=(10, 7))
    plt.title("Customer Dendograms")
    dend = shc.dendrogram(shc.linkage(X, method='average'))

    plt.show()

if __name__== "__main__":
    main()
