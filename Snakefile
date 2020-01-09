
configfile: "config/config.yaml"
SAMPLES = config['SAMPLES']


rule all:
    input:
          "results/all/merged.hdf"

rule merge:
    input:
        expand("results/samples/{sample}/{sample}_31.hdf", sample = SAMPLES)
    output:
        "results/all/merged.hdf"
    log:
        "logs/merge/merge.txt"
    conda:
        "envs/plasmidsimilarity.yaml"
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
        name = "results/{sample}/{sample}",
        kmersize = 31
    log:
        "logs/count/{sample}_log.txt"
    conda:
        "envs/plasmidsimilarity.yaml"
    shell:
         "python ./plasmidsimilarity.py count -i {input} -o {params.name} -k {params.kmersize} 2> {log}"
