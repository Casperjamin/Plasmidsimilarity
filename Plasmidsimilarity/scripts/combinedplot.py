import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

from Plasmidsimilarity.scripts.heatmap import minsize

matplotlib.use('Agg')


def generateplot(abricate, distancematrix, output):
    geno = pd.read_csv(abricate, sep = '\t', index_col = 0)
    dist = pd.read_csv(distancematrix, sep = '\t', index_col = 0)

    height = minsize(len(geno) * 0.6, 6)
    width = minsize(len(geno.columns) * 0.4, 10) * 2
    plot, axes = plt.subplots(1,2, figsize = [width, height])

    linked = linkage(squareform(dist))
    den = dendrogram(linked, ax = axes[1], orientation = 'right', labels = dist.index)

    ori = sns.heatmap(
            geno.iloc[den['leaves'][::-1],:],
            ax = axes[0],
            cbar = False,
            cmap = 'Blues',
            linewidth = 0.01,
            linecolor = 'black')
    axes[0].set_ylabel("")
    axes[1].get_yaxis().set_visible(False)
    plt.subplots_adjust(wspace = 0)
    plt.savefig(output, bbox_inches = 'tight')
