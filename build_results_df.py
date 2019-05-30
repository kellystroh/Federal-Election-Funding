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

