#!/usr/bin/env python3
from argparse import ArgumentParser
from scripts.plasmidplots import plot




def parse_cl_args():
    parser = ArgumentParser()

    parser.add_argument(
    "-i",
     "--input-files",
      required=True,
       dest="input_files",
       )
    parser.add_argument(
    "-o",
     "--output-file",
      required=True,
       dest="output_file"
       )

    args = parser.parse_args()

    return args.input_files,\
    args.output_file,\



input_files, output_file = parse_cl_args()


def main():
    plot(input_files, output_file)


if __name__ == "__main__":
    main()
