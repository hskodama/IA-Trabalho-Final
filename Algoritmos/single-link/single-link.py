
import numpy as np # linear algebra
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import adjusted_rand_score
import scipy.cluster.hierarchy as shc

def main():
    compare_values = []
    i = 0

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

    if (option == 1):
        file_name = "datasets/c2ds1-2sp.txt"
        realfile_name = "datasets/c2ds1-2spReal.clu"
    elif (option == 2):
        file_name = "datasets/c2ds3-2g.txt"
        realfile_name = "datasets/c2ds3-2gReal.clu"
    elif (option == 3):
        file_name = "datasets/monkey.txt"
        realfile_name = "datasets/monkeyReal1.clu"

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

    cluster = AgglomerativeClustering(n_clusters=8, affinity='euclidean', linkage='average')
    cluster.fit_predict(X)
    #print(cluster.labels_)
    plt.scatter(X[:, 0], X[:, 1], c=cluster.labels_, cmap='rainbow', s=2)

    plt.figure(figsize=(10, 7))
    plt.title("Customer Dendograms")
    dend = shc.dendrogram(shc.linkage(X, method='average'))

    # Abertura do arquivo Real
    read = open(realfile_name, 'r')

    # Separacao da segunda coluna do arquivo
    for line in read:
        newline = line.rstrip("\n").split("\t")
        compare_values.append(int(newline[1]))

    print("\nAdjusted Rand Score: " + str(adjusted_rand_score(compare_values, cluster.labels_)))

    plt.show()

if __name__== "__main__":
    main()
