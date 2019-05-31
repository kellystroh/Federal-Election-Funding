import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')


import build_financial_df as fin
import build_results_df as res
merge_df_start = res.results_GE.merge(fin.finance_df, how="inner", left_on="elec-cand", right_on="ELEC-CAND")

# round values in vote% to hundreth place, should've done this earlier
merge_df_start.loc[:, 'vote%'] = merge_df_start['vote%'].round(decimals=2)

#identify Senate, and fix elec_id problem
merge_df_start.loc[(merge_df_start['office']=="US Senate"), "elec_id"] = merge_df_start['elec_id'].str.replace('-00','-SE')

# num_cand = 8868 races that survived the data cull
num_cand = merge_df_start['elec_id'].value_counts()

# 14374 candidates in merge_df_cut
# 6606 races with 2+ candidates that survived the data cull
# above calc from: merge_df_cut['elec_id'].value_counts()
num_cand_df = pd.DataFrame()
num_cand_df = num_cand[num_cand>1]
merge_df_cut = merge_df_start[merge_df_start['elec_id'].isin(num_cand_df.reset_index()['index'])]

