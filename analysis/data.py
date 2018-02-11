"""Utils for loading data.
"""
import pandas as pd

def load(name):
    path = '../data/' + name
    df = pd.read_csv(path, index_col='id')
    return df
