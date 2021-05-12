import pandas as pd
import Bio.SeqIO as SeqIO


def nucl_count(sequence):
    """determine counts of each letter in a sequence,
    return dictionary with counts"""
    nucl = {'A': 0, 'G': 0, 'C':  0, 'G': 0, 'N': 0}

    for letter in sequence:
        if letter not in nucl:
            nucl[letter] = 0
        nucl[letter] += 1

    return nucl


class PlasmidDescribe:
    """read sequence and collect various metadata regarding the sequence itself
    such as gc-content, number of contigs, length"""
    def __init__(self, plasmidloc):
        self.plasmidloc = plasmidloc
        self.description = self.read_seq()

    def read_seq(self):
        numcontigs = 0
        numBP = 0
        nucleotides = {}

        for contig in SeqIO.parse(self.plasmidloc, 'fasta'):
            numcontigs += 1
            numBP += len(contig.seq)
            nucleotides.update(nucl_count(contig.seq.upper()))

        results = {
            "contigs": numcontigs,
            "basepairs": numBP,
            'GC%': (nucleotides['C'] + nucleotides['G']) / numBP * 100,
            "A nucl": nucleotides['A'],
            "C nucl": nucleotides['C'],
            "G nucl": nucleotides['G'],
            "T nucl": nucleotides['T'],
            "N nucl": nucleotides['N'],
            "other nucleotides": numBP - sum(
                [nucleotides[x] for x in ['A', 'C', 'G', 'T']])
            }
        return results


class DescriptionPlasmids:
    def __init__(self, inputlist, output):
        self.inputlist = inputlist
        self.output = output
        self.data = self.describeplasmids()

    def describeplasmids(self):
        dataplasmids = []
        for i in self.inputlist:
            x = PlasmidDescribe(i)
            dataplasmids.append(pd.Series((x.description), name=i))

        dataplasmids = pd.DataFrame(dataplasmids)
        dataplasmids.to_csv(self.output, sep='\t')
