import pandas as pd

def merge(input, output):
    print("Merging kmercount files, this may take a while \n")
    df = pd.concat([pd.read_pickle(x) for x in input], sort = False).fillna(0)
    print("Dumping output in HDF \n")
    df.to_hdf(f"{output}.h5", key = 'df', format = 'fixed')
