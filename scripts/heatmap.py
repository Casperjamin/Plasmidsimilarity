import pandas as pd
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import sys
import matplotlib.pyplot as plt

def generate_heatmap(abricateAMR, leaforder, output):
    df = pd.read_csv(abricateAMR, sep = "\t", index_col = 0)
    order = read_leaf_order(leaforder)
    order = order[::-1] #reverse to match with dendrogram leaves
    df = df.reindex(order)
    make_heatmap(df, output)


def read_leaf_order(leaforder):
    order = []
    with open(leaforder, 'r') as f:
        for i in f:
            order.append(i.strip('\n'))
    return order

def make_heatmap(df, output):
    width = len(df.T) * 0.6
    height = len(df) * 0.4
    plt.figure(figsize = [width,height])
    plt.title('Heatmap of AMR genes and plasmid ORIs')
    sns.heatmap(df, cmap = "YlGnBu", linewidth = 0.5, linecolor = 'black')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(output)
