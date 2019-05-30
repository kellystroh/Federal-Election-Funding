%matplotlib inline

import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')

results_data_76to2018 = pd.read_csv('/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/results-from-Dataverse/house1976-2018.csv', sep=',', header=0)
results_data_80to18 = results_data_76to2018[results_data_76to2018['year']>1979]
senate_data = pd.read_csv('/Users/Kelly/galvanize/week4/Federal-Election-Funding/data/results-from-Dataverse/Senate/1976-2018-senate2.csv', sep=',', header=0)
senate_data_80to18 = senate_data[senate_data['year']>1979]

results_raw = pd.concat([senate_data_80to18, results_data_80to18], axis=0)

#filter out primaries
results_gen_elec1 = results_raw[results_raw['stage']=='gen']
#filter out write ins
results_gen_elec2 = results_gen_elec1[results_gen_elec1['writein']==False]
#filter out special
results_gen_elec3 = results_gen_elec2[results_gen_elec2['special']==False]
#add column for district string
results_gen_elec3['district_str'] = results_gen_elec3['district'].apply(lambda x: str(x) if len(str(x))>1 else '0' + str(x))
#add column for vote percentage
results_gen_elec3['vote%'] = 100 * results_gen_elec3['candidatevotes']/results_gen_elec3['totalvotes']
#add column for elec_id
results_gen_elec3['elec_id'] = results_gen_elec3['year'].astype(str) +'-'+results_gen_elec3['state_po']+'-'+results_gen_elec3['district_str']


#extract last name from candidate column (potential for error) & make new column
surname_series2 = results_gen_elec3['candidate'].apply(lambda x: x.split(' ')[-1].upper() if x.split(' ')[-1] not in nix_name else x.split(' ')[-2].upper())
#strip trailing commas 
results_gen_elec3['last_name'] = surname_series2.str.strip(',')
#look for faulty entries, particularly among frequently occurring names  
nix_name = ['Sr', 'Sr.', 'Jr', 'Jr.', 'III', 'II']
surname_series = results_gen_elec3['candidate'].apply(lambda x: x.split(' ')[-1] if x.split(' ')[-1] not in nix_name else x.split(' ')[-2])
# make list of all names that occur and remove bad entries ['Other', 'Vote/Scattering', 'scatter', 'Vote', ' ']
# *** ' ' = likely due to flaw in code
surname_lst = list(surname_series.value_counts().index)
last_name_list = [x.upper() for x in (surname_lst[3:7]+surname_lst[8:139] + surname_lst[140:])]
last_name_list
results_gen_elec3[results_gen_elec3['last_name'].isin(last_name_list)]
# make ELEC-CAND column (first edit elec_id to match formatting of finance_df)
results_gen_elec3['elec_id'] = results_gen_elec3['elec_id'].str.replace('statewide', '00')
results_gen_elec3['elec-cand'] = results_gen_elec3['elec_id'] + '-' + results_gen_elec3['last_name']
# remove duplicates from ELEC-CAND
repeats = results_gen_elec3['elec-cand'].value_counts()
repeats_df = pd.DataFrame()
repeats_df['filtered'] = repeats[repeats > 1]
mystery_repeats = results_gen_elec3[results_gen_elec3['elec-cand'].isin(repeats_df.reset_index()['index'])]
results_GE = results_gen_elec3[~results_gen_elec3['elec-cand'].isin(repeats_df.reset_index()['index'])]
# ready for merge? 
results_GE



