#read file to access headers for the group of CSVs you want to use in DF

import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt
import glob

financial_headers = pd.read_csv('/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/fin_head.csv', sep=",", header=None)
financial_headers_list = list(financial_headers.iloc[:,0])

path = r'/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/all_80to18'
all_files = glob.glob(path + "/*.txt")


li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None, sep='|', names=financial_headers_list)
    li.append(df)
    
financial_df_raw = pd.concat(li, axis=0, ignore_index=0)
