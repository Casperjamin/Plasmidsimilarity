import pandas as pd

def merger(input, output):
    print("Merging kmercount files, this may take a while \n")
    df = pd.concat([pd.read_pickle(x).T for x in input], sort = False).fillna(0)
    print("Dumping merged kmers profiles in HDF format \n")
    df.to_hdf(f"{output}", key = 'df', format = 'fixed')
