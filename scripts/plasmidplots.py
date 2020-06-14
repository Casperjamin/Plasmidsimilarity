import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import os



def write_leaves_order(list_of_leaves, outdir):
    with open(f'{outdir}/leaforder.txt',  'w+') as f:
        for i in list_of_leaves:
            f.writelines(i + '\n')


def plottree(output, cluster, labels):
    width = 10
    height = len(labels) * 0.2
    dn = plt.figure(figsize=[width, height])
    dn = dendrogram(cluster, orientation="right", labels=labels)
    list_of_leaves = labels[dn['leaves']]
    write_leaves_order(list_of_leaves = list_of_leaves, outdir = output)
    plt.xlabel("Jaccard dissimilarity")
    dn = plt.tight_layout()

    dn = plt.savefig(f"{output}/tree.png")

def generate_pairwise_distance(matrix, df, output):
    labeledmatrix = pd.DataFrame(squareform(matrix), index = df.index, columns = df.index)
    labeledmatrix = labeledmatrix.unstack().reset_index()
    labeledmatrix.columns = ['Sample 1', 'Sample 2', 'Jaccard dissimilarity']
    labeledmatrix.to_csv(f"{output}/distances.tsv", sep = "\t")


def dataframe_to_clusters(input):
    print("Reading merged kmercounts\n")
    df = pd.read_hdf(input, index_col=0)
    print("Calculating Jaccard dissimilarity among the kmerprofiles\n ")
    matrix = pdist(df, metric="jaccard")
    print("Clustering distances  \n ")
    Z = linkage(matrix)
    return Z, matrix, df

def cluster(input, output):
    os.system(f"mkdir -p {output}")
    Z, matrix, df = dataframe_to_clusters(input)
    plottree(output, Z, df.index)
    generate_pairwise_distance(matrix, df, output)

