#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
import yaml
import os

from Plasmidsimilarity.scripts import plasmidplots
from Plasmidsimilarity.scripts import graphextract
from Plasmidsimilarity.scripts.plasmidmerge import merger
from Plasmidsimilarity.scripts.plasmidread import kmercount
from Plasmidsimilarity.scripts.unique import unique as uniq


locationrepo = os.path.dirname(os.path.abspath(__file__))


def get_absolute_path(path):
    return os.path.abspath(path)


def file_name_generator(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def snakemake_in(samples, kmersize, outdir, minid, mincov):
    samplesdic = {}
    samplesdic['parameters'] = {}
    samplesdic['parameters']["KMERSIZE"] = kmersize
    samplesdic['parameters']["outdir"] = get_absolute_path(outdir)
    samplesdic['parameters']['minid'] = minid
    samplesdic['parameters']['mincov'] = mincov
    samplesdic["SAMPLES"] = {}

    # generate the samples dictionary as input for snakemake
    for i in samples:
        samplename = file_name_generator(i)
        samplesdic["SAMPLES"][samplename] = get_absolute_path(i)
    data = yaml.dump(samplesdic, default_flow_style=False)

    # make and write config file location
    os.system(f"mkdir -p {locationrepo}/config")
    with open(f"{locationrepo}/config/config.yaml", 'w') as f:
        f.write(data)


def main(command_line=None):
    """Console script for Plasmidsimilarity."""
    # add main parser object
    print(locationrepo)
    parser = ArgumentParser(description="Plasmidsimilarity toolkit...")

    # add sub parser object
    subparsers = parser.add_subparsers(dest="mode")

    # add module to determine uniqueness of each k-mer
    unique = subparsers.add_parser(
            "unique",
            help="""determine the fraction of unique k-mers over
            a range of k-mers, output is sent to stdout""")
    unique.add_argument("-i",
                        required=True,
                        dest='input_file'
                        )
    unique.add_argument("-u",
                        required=False,
                        dest='upper_limit',
                        type=int,
                        default=51,
                        help='upper limit of the size of k-mers to analyse'
                        )
    unique.add_argument("-l",
                        required=False,
                        dest='lower_limit',
                        type=int, default=7,
                        help='lower limit of the size of k-mers to analyse'
                        )
    unique.add_argument("--cores",
                        dest='cores', required=False,
                        type=int,
                        default=1,
                        help='Number of CPU cores to use'
                        )

    # add snakemake pipeline to completely run fasta to clustered output
    snakemake = subparsers.add_parser("snakemake",
                                      help='''run full pipeline from fasta to
                                      clustering and determining AMR,
                                      virulence and ORIs''')
    snakemake.add_argument(
                "-i",
                required=True,
                dest="input_files",
                nargs="+"
                )
    snakemake.add_argument(
                            "--cores",
                            dest='cores',
                            required=True,
                            type=int,
                            help='Number of CPU cores to use'
                            )

    snakemake.add_argument("-k", required=False,
                           dest="kmersize", type=int, default=31)
    snakemake.add_argument("--mincov", required=False,
                           dest="mincov", type=float, default=60)
    snakemake.add_argument("--minid", required=False,
                           dest="minid", type=float, default=90)
    snakemake.add_argument("-o", required=True, dest="outdir")

    # add subparser for extracting plasmidlike elements from assembly graph
    extract = subparsers.add_parser("extract",
                                    help='''Takes a GFA file and output
                                    different fasta files containing binned
                                    plasmid contigs. This is based on the
                                    connectivity in the assembly graph'''
                                    )
    extract.add_argument("-i", required=True, dest="input_file")
    extract.add_argument("-o", required=True, dest="output_file")
    extract.add_argument("-u", required=False, dest="upper_limit",
                         default=1000000, type=int)
    extract.add_argument("-l", required=False, dest="lower_limit",
                         default=1000, type=int)

    # add subparser that handles kmercounting
    count = subparsers.add_parser(
                                  "count",
                                  help='''Takes a fasta file and counts the
                                  occurences of kmers of specified length,
                                  it returns a hdf file containing a pandas
                                  dataframe where each fasta entry is a new
                                  row in the dataframe'''
                                  )
    count.add_argument("-i", required=True, dest="input_file")
    count.add_argument("-o", required=True, dest="output_file")
    count.add_argument("-k", required=False,
                       dest="kmersize", type=int, default=31)
    count.add_argument(
                "-c",
                required=False,
                dest="circular",
                action='store_true',
                default=True,
                help='''if marked, sequences are considered circular
                and therefore the part of the sequence going
                from the end to the beginning
                of the contig will be used for kmer counting'''
                )

    # add subparser to merges the kmer counts
    merge = subparsers.add_parser(
                                "merge",
                                help='''Takes multiple kmer count
                                files and merge them
                                into one file, required to do clustering on'''
                                )
    merge.add_argument("-i", required=True, dest="input_files", nargs="+")
    merge.add_argument("-o", required=True, dest="output_file")

    # add subparser that handles the clustering and plotting
    cluster = subparsers.add_parser("cluster",
                                    help="""Takes a merged kmercount file and
                                    cluster the sequences based on Jaccard
                                    dissimilarity, it generates a dendrogram
                                    showing the relationship among sequences"""
                                    )
    cluster.add_argument("-i", required=True, dest="input_file")
    cluster.add_argument("-o", required=True, dest="output_file")

    # add subparser to convert a gfa to fasta
    convert = subparsers.add_parser("convert",
                                    help="convert a GFA to a fasta file")
    convert.add_argument("-i", required=True, dest="input_file")
    convert.add_argument("-o", required=True, dest="output_file")

####################
# parsing part
####################

    args = parser.parse_args(command_line)
    if args.mode == "count":
        kmercount(
                input_file=args.input_file,
                output_file=args.output_file,
                kmersize=args.kmersize,
                circular=args.circular
        )

    elif args.mode == "unique":
        uniq(
            input_file=args.input_file,
            lower=args.lower_limit,
            upper=args.upper_limit,
            numcores=args.cores
            )

    elif args.mode == "merge":
        merger(
                args.input_files,
                args.output_file
                )

    elif args.mode == "cluster":
        plasmidplots.cluster(
                args.input_file,
                args.output_file
                )

    elif args.mode == "convert":
        print("Converting GFA file to FASTA")
        mygraph = graphextract.assemblygraph(args.input_file)
        mygraph.graph_to_fasta(args.output_file)

    elif args.mode == "extract":
        print("extracting plasmid contigs and output them in separate bins")
        mygraph = graphextract.assemblygraph(args.input_file)
        mygraph.graph_to_plasmids(
                args.output_file,
                args.lower_limit,
                args.upper_limit
                )

    elif args.mode == "snakemake":
        snakemake_in(
                samples=args.input_files,
                kmersize=args.kmersize,
                outdir=args.outdir,
                minid=args.minid,
                mincov=args.mincov
                )

        os.chdir(f"{locationrepo}")
        os.system(f"snakemake --cores {args.cores}")

    else:
        parser.print_usage()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
