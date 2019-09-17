import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt


def plot(input, output):
    print("Reading merged kmercounts ...\n")
    df = pd.read_hdf(input, index_col = 0)

    print("Calculating Jaccard dissimilarity among the kmerprofiles ...\n ")
    matrix = pdist(df, metric = "jaccard")

    print("Clustering distances ... \n ")
    Z = linkage(matrix)

    plt.figure(figsize = [10, 10])
    dn = dendrogram(Z, orientation = "right", labels = df.index)
    plt.tight_layout()
    plt.savefig(f"{output}.png")
