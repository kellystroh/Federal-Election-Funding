import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')


import build_financial_df as fin
import build_results_df as res
import merge_df as mer

# get top 2 candidates from each race, leaving 13212 candidates total
# this step simplifies, but reduces info about third party candidates
top2_cand = mer.merge_df_cut.groupby('elec_id')['vote%'].nlargest(2)
# top2_cand is a pd.Series double-indexed by new_elec_id & merge_df_cut index no.


# make dictionary with values equal to set of names of top 2 candidates 
cand_pair_dct = {}
for pair in top2_cand.index:
    l_name = mer.merge_df_cut.loc[pair[1], 'last_name']
    if pair[0] not in cand_pair_dct:
        cand_pair_dct[pair[0]] = set()
    cand_pair_dct[pair[0]].add(l_name)

# list of sets of rematch races
from itertools import chain
rev_dict = {}
for key, value in cand_pair_dct.items():
    rev_dict.setdefault(str(value), set()).add(key)
rematch_list = [values for key, values in rev_dict.items() if len(values) > 1]

rematch_elec_id = []
for i in rematch_list:
    for x in i:
        rematch_elec_id.append(x)
        
# create dataframe of the 13212 'candidate entries' (bear in mind each candidate is in there at least twice)
index_list = [top2_cand.index[i][1] for i in range(len(top2_cand))]
rematch_df_start = mer.merge_df_start[mer.merge_df_start['elec_id'].isin(rematch_elec_id)]

'''

#use this to see how many races remain in dataset; this should be 
count_ttl = 0
for each in rematch_list:
    x = len(each)
    count_ttl += x
count_ttl
# first attempt, count_ttl is 1324
# second attempt, count_ttl is 1295... this makes sense because 

'''

rematch_cut = rematch_df_start[['FEC_ID','elec_id','year', 'candidate', 'candidatevotes', 'vote%', 'office', 'party', 'state', 'district','INC_STATUS','totalvotes', 'TTL_RECEIPTS', 'TTL_DISB']]

rematch3 = rematch_cut[(~rematch_cut['delta_spend'].isna()) & (~rematch_cut['delta_vote'].isna())]
rematch4 = rematch3[rematch3['delta_vote']!= 0]
rematch4
#I expected 1374; I got 1208 entries 
# missing 166

for i in range(len(rematch_list)):
    a = rematch_cut[rematch_cut['elec_id']==list(rematch_list[i])[0]].sort_values('FEC_ID').reset_index()
    b = rematch_cut[rematch_cut['elec_id']==list(rematch_list[i])[1]].sort_values('FEC_ID').reset_index()
    i1 = a['index'][0]
    i2 = a['index'][1]
    i3 = b['index'][0]
    i4 = b['index'][1]
    a.set_index('candidate')
    b.set_index('candidate')
    #print(a)
    #print(i1, i2, i3, i4)
    
    x = b['vote%']-a['vote%']
    # delta_vote for cand-idx0 in election a
    rematch_cut.loc[i1, 'delta_vote'] = 0
    # delta_vote for cand-idx1 in election a
    rematch_cut.loc[i2, 'delta_vote'] = 0
    # delta_vote for cand-idx0 in election b
    rematch_cut.loc[i3, 'delta_vote'] = x[0]
    # delta_vote for cand-idx1 in election b
    rematch_cut.loc[i4, 'delta_vote'] = x[1] 
    #print(x)
    y = b['TTL_DISB']-a['TTL_DISB']
    # delta_spend for cand-idx0 in election a
    rematch_cut.loc[i1, 'delta_spend'] = 0
    # delta_spend for cand-idx1 in election a
    rematch_cut.loc[i2, 'delta_spend'] = 0
    # delta_spend for cand-idx0 in election b
    rematch_cut.loc[i3, 'delta_spend'] = y[0]
    # delta_spend for cand-idx1 in election b
    rematch_cut.loc[i4, 'delta_spend'] = y[1] 
    #print(y)
    
rematch3 = rematch_cut[(~rematch_cut['delta_spend'].isna()) & (~rematch_cut['delta_vote'].isna())]
rematch4 = rematch3[rematch3['delta_vote']!= 0]
rematch4
#I expected 1374; I got 1208 entries 
# missing 166
