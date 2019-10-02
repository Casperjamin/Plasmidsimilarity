from Bio import SeqIO
import pandas as pd

def kmercount(input_file, output_file, kmersize):
    """reads fasta file and return a pickle file containing a pandas DataFrame
    with the kmer-counts per fasta entry
    """

    kmerdic = {}
    for i in SeqIO.parse(input_file, 'fasta'):
        p = plasmid(str(i.seq), i.id)
        count = p.sequencekmercount(kmersize)
        kmerdic[i.id] = count
        print(f"done counting kmers of {input_file}\t ")
    df = pd.DataFrame(kmerdic).T
    df.to_pickle(f"{output_file}_{kmersize}.pkl")
    print(f"pickled the kmercounts of all sequences from the file {input_file}\n ")




revcomp = {
    "A":"T",
    "C":"G",
    "G":"C",
    "T":"A",
    "N":"N"
    }


def reversecomp(inputseq):
    #function to generate reverse complementary of DNA seq

    seq = inputseq[::-1]
    revcomstring = ""
    for i in seq:
        revcomstring += revcomp[i]

    return revcomstring


class plasmid:
    def __init__(self, sequence, name):

        self.sequence = sequence.upper()
        self.name = name

    def seq(self):
        return self.sequence



    def sequencekmercount(self, k = 31):
        #generate kmercount of plasmid DNA sequence

        d = {}
        seq = self.sequence

        length = len(seq) - k + 1

        for i in range(length):
            kmer = seq[i:i+k]

            #selects lexographically first kmer between a kmer and its reverse complement
            kmer = sorted([kmer, reversecomp(kmer)])[0]

            if kmer not in d:
                d[kmer] = 0
            d[kmer] += 1

        return d
