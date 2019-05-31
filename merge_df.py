import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')



import build_financial_df as fin
import build_results_df as res
merge_df_start = res.results_GE.merge(fin.finance_df, how="inner", left_on="elec-cand", right_on="ELEC-CAND")
merge_df_start.head(5)

#identify Senate (not success)
sen_bool = merge_df_start['office']=="US Senate"
merge_df_start['new_elec_id'] = merge_df_start['elec_id'].str.replace('-00','-SE')

# 8783 races that survived the data cull
num_cand = merge_df_start['new_elec_id'].value_counts()

# 6547 races with 2+ candidates that survived the data cull
num_cand_df = pd.DataFrame()
num_cand_df = num_cand[num_cand>1]
merge_df_cut = merge_df_start[merge_df_start['new_elec_id'].isin(num_cand_df.reset_index()['index'])]

# get top 2 candidates
top2_cand = merge_df_cut.groupby('new_elec_id')['vote%'].nlargest(2)

# make dictionary with values equal to set of names of top 2 candidates 
cand_pair_dct = {}
for pair in top2_cand.index:
    l_name = merge_df_cut.loc[pair[1], 'last_name']
    if pair[0] not in cand_pair_dct:
        cand_pair_dct[pair[0]] = set()
    cand_pair_dct[pair[0]].add(l_name)

# list of sets of rematch races
from itertools import chain
rev_dict = {}
for key, value in cand_pair_dct.items():
    rev_dict.setdefault(str(value), set()).add(key)
rematch_list = [values for key, values in rev_dict.items() if len(values) > 1]

#write function to get rematch table for each item in rematch_list
def get_rematch_table(idx):
    cand_rematch = merge_df_cut[merge_df_cut.loc[:, 'new_elec_id'].isin(rematch_list[idx])]
    return cand_rematch[['new_elec_id','candidate', 'candidatevotes', 'office', 'party', 'state', 'district','INC_STATUS','totalvotes', 'TTL_RECEIPTS', 'TTL_DISB']]

'''
# eventually want to filter these weirdos because total vote % > 100%
sum_vote_percent = merge_df_cut.groupby('new_elec_id')['vote%'].nlargest(2).sum(level=0)
# below attempt didn't work
sum_percent_df = pd.DataFrame()
sum_percent_df = sum_vote_percent[sum_vote_percent<=100]
merge_df_cut2 = merge_df_cut[merge_df_cut['new_elec_id'].isin(sum_percent_df.reset_index()['index'])]
merge_df_cut2
'''
