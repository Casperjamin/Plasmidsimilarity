#!/usr/bin/env python3
from argparse import ArgumentParser
from scripts.plasmidread import plasmid, kmercount
from scripts.plasmidmerge import merger


def main(command_line = None):
    #add main parser object
    parser = ArgumentParser(description = "Plasmidsimilarity toolkit...")

    #add sub parser object
    subparsers = parser.add_subparsers(dest = "mode")

    #add suberparser that handles kmercounting
    count = subparsers.add_parser("count", help = "placeholder for kmercounting")
    count.add_argument("-i", required=True, dest="input_file")
    count.add_argument("-o", required=True, dest="output_file")
    count.add_argument("-k", required=False, dest="kmersize", type = int, default = 31,)

    #add subparser to merges the kmer counts
    merge = subparsers.add_parser("merge", help = "placeholder for merge")
    merge.add_argument("-i", required=True, dest="inputfiles", nargs = "+")
    merge.add_argument("-o", required=True, dest="outputfile")



    args = parser.parse_args(command_line)
    if args.mode == "count":
        kmercount(args.input_file, args.output_file, args.kmersize)
    elif args.mode == "merge":
        merger(args.inputfiles, args.outputfile)
    else:
        parser.print_usage()




if __name__ == "__main__":
    main()
