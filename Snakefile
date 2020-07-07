from scripts import abricate_summary, heatmap
import time
import os
from shutil import copy2
import pathlib

configfile: "config/config.yaml"
SAMPLES = config['SAMPLES']

OUTDIR = config['parameters']['outdir'] + "/"


databases = {
		'resistance':'ncbi',
		'plasmids':'plasmidfinder',
		'virulence':'vfdb'
		}


onstart:
    print("This is PlasmidSimilarity:")
    os.system("cat logo.txt")
    time.sleep(1)

    # copy the config file to output dir
    pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)
    copy2('config/config.yaml', OUTDIR )

    print('Checking number of input files...\n')
    if len(SAMPLES) < 2:
        raise Exception(f'Not enough input files given. \n')
    print("Will generate plasmid (dis)similarities for the following files:")
    for i in SAMPLES.items():
        print(i[0], '\t', i[1])
    print(f'output directory is: {OUTDIR}')
    time.sleep(3)



rule all:
    input:
       OUTDIR + "merged.hdf",
       OUTDIR + "abricate_results.tsv",
       OUTDIR + "heatmap_AMR_ori.png"

#################################
# kmer counting and merging and cluster
#################################

rule merge:
    input:
        expand(OUTDIR + "samples/{sample}/{sample}.hdf", sample = SAMPLES)
    output:
        OUTDIR + "merged.hdf"
    log:
        OUTDIR + "logs/merge/merge.txt"
    params:
        name = OUTDIR + "merged"
    shell:
        "python ./plasmidsimilarity.py merge -i {input} -o {params.name} 2> {log}"

rule count:
    input:
         lambda wildcards: SAMPLES[wildcards.sample]
    output:
          temp(OUTDIR + "samples/{sample}/{sample}.hdf")
    params:
        name = OUTDIR + "samples/{sample}/{sample}",
        kmersize = config['parameters']['KMERSIZE']
    log:
        OUTDIR + "logs/count/{sample}_log.txt"
    shell:
         "python ./plasmidsimilarity.py count -i {input} -o {params.name} -k {params.kmersize} -c 2> {log}"

rule cluster:
    input:
        OUTDIR + "merged.hdf"
    output:
        OUTDIR + "tree.png",
        OUTDIR + "leaforder.txt"
    params:
        OUTDIR
    shell:
        "python ./plasmidsimilarity.py cluster -i {input} -o {params}"


#################################
# AMR and plasmid ORI abricate
#################################
rule abricate:
    input:
        sample = lambda wildcards: SAMPLES[wildcards.sample],
    output:
        OUTDIR + "samples/{sample}/{sample}_{database}.tsv"
    log:
       OUTDIR + "logs/abricate/{sample}_{database}.txt"
    params:
	    database = lambda wildcards: databases[wildcards.database]
    shell:
        "abricate --db {params.database} {input.sample} > {output} 2> {log}"

rule summarize_abricate:
    params:
        covcutoff = 60,
        idcutoff = 90
    input:
         expand(OUTDIR + "samples/{sample}/{sample}_{database}.tsv", sample = SAMPLES, database = databases)
    output:
        OUTDIR + "abricate_results.tsv"
    run:
        data = [abricate_summary.AbricateSample(x).clean for x in input]
        df = abricate_summary.AbricateSummary(data).dataframe(covcutoff = params.covcutoff, idcutoff = params.idcutoff)
        df.to_csv(f"{output}", sep = "\t")

rule heatmap_abricate:
    input:
        heatmap = OUTDIR + "abricate_results.tsv",
        leaforder = OUTDIR +"leaforder.txt"
    output:
        OUTDIR + "heatmap_AMR_ori.png"
    run:
        heatmap.generate_heatmap(str(input.heatmap), str(input.leaforder), str(output))
