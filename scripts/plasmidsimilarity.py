#!/usr/bin/env python3
from argparse import ArgumentParser
from Bio import SeqIO
from plasmidread import plasmid
import pickle

def parse_cl_args():
    parser = ArgumentParser()

    # dest (destination) is de naam van de variable waar het argument weggeschreven wordt
    parser.add_argument("-i", "--input-file", required=True, dest="input_file")


    parser.add_argument("-o", "--output-file", required=True, dest="output_file")


    parser.add_argument(
    "-k",
     "--kmersize",
      required=False,
      dest="kmersize",
      type = int
    )

    args = parser.parse_args()

    return args.input_file, args.output_file, args.kmersize


def main():
    input_file, output_file, kmersize = parse_cl_args()

    if kmersize is None:
        kmersize = 31


    for i in SeqIO.parse(input_file, 'fasta'):
        p = plasmid(str(i.seq), i.id)
        count = p.kmercount(kmersize)
        print(count)




if __name__ == "__main__":
    main()
