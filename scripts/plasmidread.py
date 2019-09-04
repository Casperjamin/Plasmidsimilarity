


def reversecomp(inputseq):
    #function to generate reverse complementary of DNA seq
    revcomp = {
    "A":"T",
    "C":"G",
    "G":"C",
    "T":"A",
    "N":"N"
    }
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



    def kmercount(self, k = 31):
        #generate kmercount of plasmid DNA sequence

        d = {}
        seq = self.sequence

        length = len(seq) - k + 1

        for i in range(length):
            kmer = seq[i:i+k]

            kmer = sorted([kmer, reversecomp(kmer)])[0]

            if kmer not in d:
                d[kmer] = 0
            d[kmer] += 1

        return d
