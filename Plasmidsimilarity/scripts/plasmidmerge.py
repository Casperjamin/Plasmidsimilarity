import pandas as pd


def merger(input, output):
    print("Merging kmercount files, this may take a while \n")
    samples = [pd.read_hdf(x, index_col=0) for x in input]
    df = pd.concat(samples, sort=False).fillna(0)
    print("Dumping merged kmers profiles in HDF format \n")
    df.to_hdf(f"{output}.hdf", key='df', format='fixed')
