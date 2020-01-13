#!/usr/bin/env python
import os
from argparse import ArgumentParser

import yaml

from scripts import plasmidplots
from scripts import graphextract
from scripts.plasmidmerge import merger
from scripts.plasmidread import kmercount


def obtain_repoloc():
    return os.path.dirname(os.path.abspath(__file__))

def get_absolute_path(path):
    return os.path.abspath(path)

locationrepo = obtain_repoloc()


def snakemake_in(samples):
    samplesdic = {"SAMPLES":{}}
    for i in samples:
        samplename = i.split("/")[-2]
        samplesdic["SAMPLES"][samplename] = get_absolute_path(i)
    data = yaml.dump(samplesdic, default_flow_style=False)
    with open(f"{locationrepo}/config/config.yaml", 'w') as f:
        f.write(data)

####################
# Command line Parsers initialization
####################

def main(command_line = None):
    #add main parser object
    parser = ArgumentParser(description = "Plasmidsimilarity toolkit...")

    #add sub parser object
    subparsers = parser.add_subparsers(dest = "mode")


    #add snakemake pipeline to completely run fasta to clustered output
    snakemake = subparsers.add_parser("snakemake", help = "run fill pipeline from fasta to merged and clustering")
    snakemake.add_argument("-i", required = True, dest = "input_files", nargs = "+")


    #add subparser for extracting plasmidlike elements from assembly graph
    extract = subparsers.add_parser("extract", help = "take a GFA file and output different fasta files containing binned plasmid contigs. This is based on the connectivity in the assembly graph")
    extract.add_argument("-i", required = True, dest = "input_file")
    extract.add_argument("-o", required = True, dest = "output_file")
    extract.add_argument("-u", required = False, dest = "upper_limit", default = 1000000, type = int)
    extract.add_argument("-l", required = False, dest = "lower_limit", default = 1000, type = int)


    #add subparser that handles kmercounting
    count = subparsers.add_parser("count", help = "Takes a fasta file and counts the occurences of kmers of specified length, it returns a pickled file containing a pandas dataframe where each fasta entry is a new row in the dataframe")
    count.add_argument("-i", required = True, dest ="input_file")
    count.add_argument("-o", required = True, dest = "output_file")
    count.add_argument("-k", required = False, dest = "kmersize", type = int, default = 31,)


    #add subparser to merges the kmer counts
    merge = subparsers.add_parser("merge", help = "Takes multiple kmer count files and merge them into one file, required to do clustering on")
    merge.add_argument("-i", required = True, dest = "input_files", nargs = "+")
    merge.add_argument("-o", required = True, dest = "output_file")


    #add subparser that handles the clustering and plotting
    cluster = subparsers.add_parser("cluster", help = "Takes a merged kmercount file and cluster the sequences based on Jaccard dissimilarity, it generates a dendrogram showing the relationship among sequences")
    cluster.add_argument("-i", required = True, dest = "input_file")
    cluster.add_argument("-o", required = True, dest = "output_file")

    #add subparser to convert a gfa to fasta
    convert = subparsers.add_parser("convert", help = "convert a GFA to a fasta file")
    convert.add_argument("-i", required = True, dest = "input_file")
    convert.add_argument("-o", required = True, dest = "output_file")



####################
# parsing part
####################

    args = parser.parse_args(command_line)
    if args.mode == "count":
        kmercount(args.input_file, args.output_file, args.kmersize)

    elif args.mode == "merge":
        merger(args.input_files, args.output_file)

    elif args.mode == "cluster":
        plasmidplots.cluster(args.input_file, args.output_file)

    elif args.mode == "convert":
        print("Converting GFA file to FASTA")
        mygraph = graphextract.assemblygraph(args.input_file)
        mygraph.graph_to_fasta(args.output_file)

    elif args.mode == "extract":
        print("extracting plasmid contigs and output them in separate bins")
        mygraph = graphextract.assemblygraph(args.input_file)
        mygraph.graph_to_plasmids(args.output_file, args.lower_limit, args.upper_limit)

    elif args.mode == "snakemake":
        snakemake_in(args.input_files)
        os.chdir(f"{locationrepo}")
        os.system(f"Snakemake --cores 4")


    else:
        parser.print_usage()




if __name__ == "__main__":
    main()
