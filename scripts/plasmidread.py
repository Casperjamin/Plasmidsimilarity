from Bio import SeqIO
import pandas as pd

def reversecomp(inputseq):
    # generate reverse complementary of DNA seq
    revcomp = {
        "A":"T",
        "C":"G",
        "G":"C",
        "T":"A",
        "N":"N"}

    seq = inputseq[::-1]
    revcomstring = ""
    for i in seq:
        revcomstring += revcomp[i]
    return revcomstring


def seq_to_kmercount(seq, kmerdict, kmersize):
    """
    DNA sequence and count number of kmers in the dictionary, and return this dictionary
    """
    seq = str(seq).upper()

    length = len(seq) - kmersize + 1
    for i in range(length):
        kmer = seq[i:i+kmersize]
        # select lexographically lowest kmer between a kmer and its reverse complement
        kmer = sorted([kmer, reversecomp(kmer)])[0]
        if kmer not in kmerdict:
            kmerdict[kmer] = 0
        kmerdict[kmer] += 1
    return kmerdict


def multiplecontigs(inputfasta):
    """
    returns True if more than 1 contig is found in file; otherwise return False
    """
    count = 0
    for i in SeqIO.parse(inputfasta, 'fasta'):
        count += 1
        if count > 1:
            return True
    return False


def generate_output(kmer_dataframe, output_file, kmersize):
    """
    take kmer_dataframe of dictionaries of kmercounts, generate output files
    """
    kmer_dataframe.columns = [output_file.split("/")[-1]]
    kmer_dataframe = kmer_dataframe.T
    kmer_dataframe.to_hdf(f"{output_file}_{kmersize}.hdf", key = 'df', format = 'fixed')


def kmercount(input_file, output_file, kmersize = 31, circular = False):
    """
    reads fasta file and return a hdf file containing a pandas DataFrame
    with the kmer-counts per fasta entry
    """
    inputfilename = input_file.split('/')[-1].strip('.fasta')
    if multiplecontigs(input_file):
        # assesment of circular plasmids is considered false if more than 1 contig is present
        circular = False

    kmerdict = {}

    number_of_contigs = 0
    for i in SeqIO.parse(input_file, 'fasta'):
        sequence = i.seq
        number_of_contigs += 1
        kmerdict = seq_to_kmercount(sequence, kmerdict = kmerdict, kmersize = kmersize)

    # generate counts of kmers on the overlapping part of a contig's end and beginning
    if number_of_contigs == 1 & circular == True:
        overlapping_sequence = overlapper(sequence)
        kmerdict = seq_to_kmercount(overlapping_sequence, kmerdict = kmerdict, kmersize = kmersize)

    series = pd.Series(kmerdict, name = inputfilename)
    df = pd.DataFrame(series)
    print(df.head())
    print(input_file)
    print(f"done counting kmers of {input_file}\t ")
    generate_output(df, output_file = output_file, kmersize = kmersize)
