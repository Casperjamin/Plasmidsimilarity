import pandas as pd
from .plasmidread import kmercount
from joblib import Parallel, delayed



def unique(input_file, output, lower, upper, numcores = 1):

    inputs = list(range(lower, upper + 1))
    processed = Parallel(n_jobs = numcores)(delayed(determine_unique)(i, input_file) for i in inputs)
    [print(x[0],x[1]) for x in processed]
     



def determine_unique(kmersize, input_file):
    series = kmercount(input_file, output_file = None, kmersize = kmersize, write = False)
    num_uniq = series.value_counts()[1]
    total = len(series)
    return (kmersize, num_uniq / total)
