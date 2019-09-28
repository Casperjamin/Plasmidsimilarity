#!/usr/bin/env python3
from argparse import ArgumentParser
from scripts.plasmidread import plasmid, kmercount


def parse_cl_args():
    parser = ArgumentParser()

    subparsers = parser.add_subparsers()

    subparse_kmercount = subparsers.add_parsers('kmercount')

    subparse_kmercount.add_argument("-i", "--input-file", required=True, dest="input_file",)
    subparse_kmercount.add_argument("-o", "--output-file",required=True, dest="output_file",)
    subparse_kmercount.add_argument("-k", "--kmersize", required=False, dest="kmersize", type = int, default = 31,)


    parser.add_argument(
    "-m",
     "--merge",
      required=False,
      dest="merge",
    )

    args = parser.parse_args()

    return args.input_file,\
    args.output_file,\
    args.kmersize,\
    args.merge


input_file, output_file, kmersize, merge = parse_cl_args()


def main():
    kmercount(input_file, output_file, kmersize)


if __name__ == "__main__":
    main()
