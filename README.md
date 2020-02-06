# Plasmidsimilarity
set of scripts to analyse and visualise plasmid sequences

## Work in process, feel free to post issues or contribute 


the concept of comparing and/or clustering of plasmid sequences is by comparing all subsequences of length K (=Kmers) and computing jaccard dissimilarity.  
From here one can generate a dendrogram indicating the dissimilarity among al plasmids.  



## usage

For now, easiest way to compare multiple plasmid sequences is to use the "plasmidsimilarity.py snakemake" wrapper. for this you need to supply 1 directoy with subdirectories each containing 1 fasta file with a plasmid sequence.  
The name of these subdirecties will be use for naming the samples  
actual usage:   
```
git clone https://hithub.com/casperjamin/plasmidsimilarity.git
cd plasmidsimilarity
python ./plasmidsimilarity.py snakemake -i YOUR/INPUT/DIRECTORY
```

results will be shown in the results folder within this repo/directory


To do:  
* write complete manual
* version numbering
* come up with a suitable way to handle output directory with Snakemake
* specify number of cores in snakemake mode



Requirements:  
* python 3.6 or higher  
* Abricate  for AMR and plasmid information
if you use the "plasmidsimilarity.py snakemake"  wrapper, you also need Snakemake to be installed.  

python packages  
* pandas
* pytables  
* networkx      
* matplotlib
* seaborn 
* scipy  
* Biopython    




## Acknowledgments

This work was supported by the Dutch workgroup Molecular typing for infectious diseases, the WMDI
