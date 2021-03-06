# Plasmidsimilarity
set of scripts to analyse similarity among plasmid sequences

## Work in process, feel free to post issues or contribute 


the concept of comparing and/or clustering of plasmid sequences is by comparing all subsequences of length K (=Kmers) and computing jaccard dissimilarity.  
From here one can generate a dendrogram indicating the dissimilarity among al plasmids.  



## Basic usage

For now, easiest way to compare multiple plasmid sequences is to use the "plasmidsimilarity.py snakemake" wrapper. for this you need to supply the script with a list of plasmid sequences in fasta format

actual cloning and usage:   
```
git clone https://github.com/casperjamin/plasmidsimilarity.git
cd plasmidsimilarity
python ./plasmidsimilarity.py snakemake \
-i plasmidseq1.fasta plasmidseq2.fasta plasmidseq2.fasta otherplasmidseq*fasta \
--cores 1 \
-o myoutdir
```

results will be shown in 'myoutdir' 

## Extracting plasmid-like sequences from asssembly graphs (in gfa format)

Plasmidsimilarity has as built-in method to extract small elements from an assembly graph.  
usage:
```
python ./plasmidsimilarity.py extract -i yourassemblygraph.gfa -o outdir/outputname
```
this will dump each plasmidlike element in a single fasta file with name format 'outputname_plasmid_#.fasta'   
warning: this does however also extract all contamination, or mis-assemblies. it works best with proper circularized assemblies, from unicycler for instance.




## To do:   
* write complete manual
* version numbering




## Requirements:  
* python 3.6 or higher  
* Abricate  for AMR and plasmid information  
If you use the "plasmidsimilarity.py snakemake"  wrapper, you also need Snakemake to be installed.  

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
