from Bio import SeqIO
import pandas as pd
import warnings

def reversecomp(inputseq):
    # generate reverse complementary of DNA seq
    revcomp = {
        "A":"T",
        "C":"G",
        "G":"C",
        "T":"A",
        "M":"K",
        "K":"M",
        "B":"V",
        "V":"B",
        "H":"D",
        "Y":"R",
        "R":"Y",
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
    kmer_dataframe.to_hdf(f"{output_file}.hdf", key = 'df', format = 'fixed')

def overlapper(sequence,kmersize):
    """
    take a fasta sequence and kmersize,
    return the sequence that overlaps from the end to the beginning
    required for complete k-mer counting
    """
    end = sequence[-(kmersize -1):]
    beginning = sequence[:kmersize-1]
    return end + beginning


def kmercount(input_file, output_file, kmersize = 31, circular = True, write = True):
    """
    reads fasta file and return a hdf file containing a pandas DataFrame
    with the kmer-counts per fasta entry
    """
    inputfilename = input_file.split('/')[-1].strip('.fasta')

    kmerdict = {}

    number_of_contigs = 0
    for i in SeqIO.parse(input_file, 'fasta'):
        sequence = i.seq
        if len(sequence) < kmersize:
            continue

        number_of_contigs += 1
        kmerdict = seq_to_kmercount(seq = sequence, kmerdict = kmerdict, kmersize = kmersize)

    # generate counts of kmers on the overlapping part of a contig's end and beginning
    if number_of_contigs > 1 & circular == True:
        warnings.warn(
        f'''
        "You specified circularized plasmids,in {input_file}.
         but I encounterd multiple contigs...
         If you actually have circular plasmids, please provide fasta file with only 1 contig
         For now I will consider non-circularized plasmid sequences therefore not counting kmers from the end of the contig to the beginning.
         ''')

    if multiplecontigs(input_file):
        # assesment of circular plasmids is considered false if more than 1 contig is present
        circular = False

    if number_of_contigs == 1 & circular == True:
        overlapping_sequence = overlapper(sequence = sequence, kmersize = kmersize)
        kmerdict = seq_to_kmercount(seq = overlapping_sequence, kmerdict = kmerdict, kmersize = kmersize)

    series = pd.Series(kmerdict, name = inputfilename)
    df = pd.DataFrame(series)


    # added this if write block to reuse this code for the uniqueness module
    if write:
        print(f"done counting kmers of {input_file}\t ")
        generate_output(df, output_file = output_file, kmersize = kmersize)

    else:
        return series
