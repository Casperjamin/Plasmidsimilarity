from scripts import abricate_summary, heatmap
import time
import os
configfile: "config/config.yaml"
SAMPLES = config['SAMPLES']


onstart:
    print("This is PlasmidSimilarity:")
    os.system("cat logo.txt")
    time.sleep(1)
    print('Checking number of input files...\n')
    if len(SAMPLES) < 2:
        raise Exception(f'Not enough input files given. \n')
    print("Will generate plasmid (dis)similarities for the following files:")
    for i in SAMPLES.items():
        print(i[0], '\t', i[1])

    time.sleep(5)



rule all:
    input:
        "results/all/merged.hdf",
        "results/all/abricate_results.tsv",
        "results/all/report/heatmap_AMR_ori.png"

#################################
# kmer counting and merging and cluster
#################################

rule merge:
    input:
        expand("results/samples/{sample}/{sample}_31.hdf", sample = SAMPLES)
    output:
        "results/all/merged.hdf"
    log:
        "logs/merge/merge.txt"
    params:
        name = "results/all/merged"
    shell:
        "python ./plasmidsimilarity.py merge -i {input} -o {params.name}"

rule count:
    input:
         lambda wildcards: SAMPLES[wildcards.sample]
    output:
          "results/samples/{sample}/{sample}_31.hdf"
    params:
        name = "results/samples/{sample}/{sample}",
        kmersize = 31
    log:
        "logs/count/{sample}_log.txt"
    shell:
         "python ./plasmidsimilarity.py count -i {input} -o {params.name} -k {params.kmersize} -c 2> {log}"

rule cluster:
    input:
        "results/all/merged.hdf"
    output:
        "results/all/report/tree.png",
        "results/all/report/leaforder.txt"
    params:
        "results/all/report"
    shell:
        "python ./plasmidsimilarity.py cluster -i {input} -o {params}"


#################################
# AMR and plasmid ORI abricate
#################################
rule abricate:
    input:
        lambda wildcards: SAMPLES[wildcards.sample]
    output:
        "results/samples/{sample}/{sample}_resistance.tsv"
    log:
       "logs/abricate/{sample}_resistance.txt"
    shell:
        "abricate {input} > {output}"

rule plasmid_abricate:
    input:
         lambda wildcards: SAMPLES[wildcards.sample]
    output:
        "results/samples/{sample}/{sample}_plasmids.tsv"
    log:
       "logs/abricate/{sample}_plasmids.txt"
    shell:
        "abricate --db plasmidfinder {input} > {output}"

rule summarize_abricate:
    params:
        covcutoff = 60,
        idcutoff = 90
    input:
        resistance = expand("results/samples/{sample}/{sample}_resistance.tsv", sample = SAMPLES),
        plasmids = expand("results/samples/{sample}/{sample}_plasmids.tsv", sample = SAMPLES)
    output:
        "results/all/abricate_results.tsv"
    run:
        data = [abricate_summary.AbricateSample(x).clean for x in input]
        df = abricate_summary.AbricateSummary(data).dataframe(covcutoff= params.covcutoff, idcutoff = params.idcutoff)
        df.to_csv(f"{output}", sep = "\t")

rule heatmap_abricate:
    input:
        heatmap = "results/all/abricate_results.tsv",
        leaforder = "results/all/report/leaforder.txt"
    output:
        "results/all/report/heatmap_AMR_ori.png"
    run:
        heatmap.generate_heatmap(str(input.heatmap), str(input.leaforder), str(output))
