from Plasmidsimilarity.scripts.plasmidread import kmercount
from joblib import Parallel, delayed


def unique(input_file, lower, upper, numcores=1):
    """
    count number of unique k-mers over a range of k-mers,
    returns fraction of unique k-mers

    INPUT:
    input_file: fasta file that will be analysed
    lower: lower limit of size k to use
    upper: upper limit of size k to use
    numcores: number of cores to use

    OUTPUT:
    sends for each size of k the fraction of unique k-mers
    """
    inputs = list(range(lower, upper + 1))
    processed = Parallel(n_jobs=numcores)(
                delayed(determine_unique)(i, input_file) for i in inputs)
    [print(x[0], '\t', x[1]) for x in processed]


def determine_unique(kmersize, input_file):
    series = kmercount(
                input_file,
                output_file=None,
                kmersize=kmersize,
                write=False)
    num_uniq = series.value_counts()[1]
    total = len(series)
    return (kmersize, num_uniq / total)
