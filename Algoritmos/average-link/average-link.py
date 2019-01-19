
import numpy as np 
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt
from scipy.spatial import distance
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import adjusted_rand_score
import csv
import scipy.cluster.hierarchy as shc


import math

def main():
    # dots_X contem as coordenadas X dos pontos
    # dots_Y contem as coordenadas Y dos pontos
    real_value = []
    i = 0

    # Pergunta o arquivo desejado
    print(""" 
    1. c2ds1-2sp.txt
    2. c2ds3-2g.txt
    3. monkey.txt
    """)

    option = int(input("Enter the option: "))
    clusters = 2

    # Intervalo de valores para k (numero de clusters):
    #kMin = int(input("Kmin: "))
    #kMax = int(input("Kmax: "))

    if (option == 1):
        file_name = "../../datasets/c2ds1-2sp.txt"
        Realfile_name = "../../datasets/c2ds1-2spReal.clu"
        resultfile_name = "../../Resultados/average-link_results1.csv"
        dendoimage_name = "resultado1.png"
        realimage_name = "dendrogram1.png"
    elif (option == 2):
        file_name = "../../datasets/c2ds3-2g.txt"
        Realfile_name = "../../datasets/c2ds3-2gReal.clu"
        resultfile_name = "../../Resultados/average-link_results2.csv"
        dendoimage_name = "resultado2.png"
        realimage_name = "dendrogram2.png"
    elif (option == 3):
        file_name = "../../datasets/monkey.txt"
        Realfile_name = "../../datasets/monkeyReal1.clu"
        resultfile_name = "../../Resultados/average-link_results3.csv"
        dendoimage_name = "resultado3.png"
        realimage_name = "dendrogram3.png"
        clusters = 8

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

    read = open(Realfile_name, 'r')

    # Separacao da segunda coluna do arquivo
    for line in read:
        newline = line.rstrip("\n").split("\t")
        real_value.append(int(newline[1]))

    X = np.array(X)


    cluster = AgglomerativeClustering(n_clusters=clusters, affinity='euclidean', linkage='average')
    cluster.fit_predict(X)
    
    plt.figure(figsize=(16, 9))
    plt.scatter(X[:, 0], X[:, 1], c=cluster.labels_, cmap='rainbow', s=1)
    plt.savefig(dendoimage_name, bbox_inches = 'tight')

    plt.figure(figsize=(16, 9))
    shc.dendrogram(shc.linkage(X, method='average'))
    plt.savefig(realimage_name, bbox_inches = 'tight')

    ARI = adjusted_rand_score(real_value, cluster.labels_)

    # Exporta para CSV
    with open(resultfile_name, 'w') as csvfile:
        fieldnames = ['Real', 'Calculado', 'ARI']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        i = 0
        for i in range (len(real_value)):
            if(i == 0):
                writer.writerow({'Real': real_value[i], 'Calculado': cluster.labels_[i], 'ARI': ARI})
            else:
                writer.writerow({'Real': real_value[i], 'Calculado': cluster.labels_[i]})

if __name__== "__main__":
    main()
