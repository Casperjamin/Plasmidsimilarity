from scripts import abricate_summary


configfile: "config/config.yaml"
SAMPLES = config['SAMPLES']


rule all:
    input:
        "results/all/merged.hdf",
        "results/all/abricate_results.tsv"

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
        name = "results/samples/l {sample}/{sample}",
        kmersize = 31
    log:
        "logs/count/{sample}_log.txt"
    shell:
         "python ./plasmidsimilarity.py count -i {input} -o {params.name} -k {params.kmersize} 2> {log}"


rule cluster:
    input:
        "results/all/merged.hdf"
    output:

    shell:
        "python ./plasmidsimilarity.py cluster -i {input} -o {output}"


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


