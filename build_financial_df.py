import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt
import glob

#read file to access headers for the group of CSVs you want to use in DF
financial_headers = pd.read_csv('/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/fin_head.csv', sep=",", header=None)
financial_headers_list = list(financial_headers.iloc[:,0])

#read all 20 txt files (from 2 directories)
path1 = r'/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/all_80to18/80to98'
path2 = r'/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/all_80to18/00to18'
files1 = glob.glob(path1 + "/*.txt")
files2 = glob.glob(path2 + "/*.txt")


li = []

for filename in files1:
    df = pd.read_csv(filename, index_col=None, header=None, sep='|', names=financial_headers_list, dtype={'DISTRICT':str})
    x = filename.replace('/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/all_80to18/80to98/weball', '').replace(".txt",'')
    df['YEAR'] = int('19'+ x)
    li.append(df)
    
for filename in files2:
    df = pd.read_csv(filename, index_col=None, header=None, sep='|', names=financial_headers_list, dtype={'DISTRICT':str})
    x = filename.replace('/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/all_80to18/00to18/weball', '').replace(".txt",'')
    df['YEAR'] = int('20'+ x)
    li.append(df)
#create df by concatenating all 20 files    
financial_df_raw = pd.concat(li, axis=0, ignore_index=0)

# new column for last name
financial_df_raw['LAST_NAME'] = financial_df_raw['NAME'].str.replace(',.*', '')
# new column to identify particular races (year-state-district)
financial_df_raw["ELEC_ID"] = financial_df_raw['YEAR'].astype(str) + "-"+ financial_df_raw['STATE'].astype(str) +"-"+ financial_df_raw['DISTRICT'].astype(str)

'''
attempt to merge with candidate data files... changed mind for now
path = r'/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/financial/cn'
files = glob.glob(path + "/*.txt")
cand_cols = ['ID', "x1", "x2", 'ELEC_YEAR',"x3",'OFFICE', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15']
li = []

for filename in files:
    df = pd.read_csv(filename, index_col=None, header=None, sep='|', names=cand_cols)
    li.append(df)
    
#candidate_df_raw = pd.concat(li, axis=0, ignore_index=0)
#candidate_df = candidate_df_raw[['ID','ELEC_YEAR','OFFICE']]
#join1 = financial_df_raw.merge(candidate_df, how='inner', left_on='FEC_ID', right_on='ID')
#financial_df_plus = x123.drop('ID', axis=1)
'''
#new column for elec_id (i.e. year-state-district)
financial_df_raw["ELEC_ID"] = financial_df_raw['YEAR'].astype(str) + "-"+ financial_df_raw['STATE'].astype(str) +"-"+ financial_df_raw['DISTRICT'].astype(str)

# filter out presidential candidates
fin_cut_1 = financial_df_raw[financial_df_raw['STATE']!='00']
# create column for shared key 'ELEC-CAND'
fin_cut_1['ELEC-CAND'] = fin_cut_1["ELEC_ID"].astype(str) +"-"+ fin_cut_1["LAST_NAME"].astype(str)
# filter out repeats in ELEC-CAND... may want to add some back because of last name issue
# repeats are in mystery_df, if I have time to search them for legit entries 
#(i.e. repeats caused by two candidates in race having same last name; entries where district = '00')
count_repeats = fin_cut_1['ELEC-CAND'].value_counts()
repeat_df = pd.DataFrame()
repeat_df['filtered'] = count_repeats[count_repeats > 1]
finance_df = fin_cut_1[~fin_cut_1['ELEC-CAND'].isin(repeat_df.reset_index()['index'])]
finance_df

'''
for later consideration :
mystery_df = fin_cut_1[fin_cut_1['ELEC-CAND'].isin(new_df.reset_index()['index'])]

'''
