#!/usr/bin/env python3
from argparse import ArgumentParser
from scripts.plasmidread import plasmid, kmercount


def main(command_line = None):
    #add main parser object
    parser = ArgumentParser()
    parser.add_argument("-v","--version", required = False, dest = "version")

    #add sub parser object
    subparsers = parser.add_subparsers(dest = "mode")

    #add suberparser that handles kmercounting
    count = subparsers.add_parser("count", help = "placeholder for count parser")
    count.add_argument("-i", "--input-file", required=True, dest="input_file")
    count.add_argument("-o", "--output-file",required=True, dest="output_file")
    count.add_argument("-k", "--kmersize", required=False, dest="kmersize", type = int, default = 31,)

    #add subparser to merges the kmer counts
    merge = subparsers.add_parser("merge", help = "placeholder for merge")
    merge.add_argument("-i", "--input-files", required=True, dest="input_files", nargs = "+")
    merge.add_argument("-o", "--output-file", required=True, dest="output_file")



    args = parser.parse_args(command_line)
    if args.mode == "count":
        kmercount(args.input_file, args.output_file, args.kmersize)





if __name__ == "__main__":
    main()
