import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.style.use('ggplot')


import build_financial_df as fin
import build_results_df as res
import merge_df as mer
import rematch_df as rem

import statsmodels.api as sm


# LINEAR REGRESSION for full DF
df = rem.rematch_df[['delta_vote', 'delta_spend']]
X = df['delta_spend']
y = df['delta_vote']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# DEFINE BEST FIT LINE for full DF
def all_f(z):
    return  model.params[1]*x + model.params[0]

# PLOT SCATTER for full DF
plot_all = rematch_df[['delta_vote', 'delta_spend']]
x = plot_all['delta_vote']
y = plot_all['delta_spend']
fig, ax = plt.subplots(1, figsize=(20,12))
z = np.linspace(-6000000, 6000000, num=1200)
ax.plot(z, all_f(z), '-')
ax.scatter(y, x, alpha=1, s=15)
ax.set_xlim(-6000000, 6000000)
ax.set_ylim(-80, 80)
ax.set_title('Comparing Spending and Vote Percentages across Rematch Elections', fontsize=30)
ax.set_xlabel('Change in Money Spent', fontsize=18)
ax.set_ylabel('Change in Vote Point', fontsize=18)

# SUBSETS of DF by party
rematch_GOP = rematch_df[rematch_df['party']=='republican']
rematch_Dem = rematch_df[rematch_df['party']=='democrat']
rematch_Ind = rematch_df[(rematch_df['party']!='democrat') & (rematch_df['party']!='republican')]

# DEFINE BEST FIT LINE for GOP subset
def GOP_f(x):
    return  model_GOP.params[1]*x + model_GOP.params[0]

# LINEAR REGRESSION for republican subset
df_GOP = rematch_GOP[['delta_vote', 'delta_spend']]
X = df_GOP['delta_spend']
y = df_GOP['delta_vote']
X = sm.add_constant(X)
model_GOP = sm.OLS(y, X).fit()
predictions = model_GOP.predict(X)

# DEFINE BEST FIT LINE for democrat subset
def Dem_f(x):
    return  model_Dem.params[1]*x + model_Dem.params[0]

# LINEAR REGRESSION for democrat subset
df_Dem = rematch_Dem[['delta_vote', 'delta_spend']]
X = df_Dem['delta_spend']
y = df_Dem['delta_vote']
X = sm.add_constant(X)
model_Dem = sm.OLS(y, X).fit()
predictions = model_Dem.predict(X)

# DEFINE BEST FIT LINE for independent subset
def Ind_f(x):
    return  model_Ind.params[1]*x + model_Ind.params[0]

# LINEAR REGRESSION for independent subset
df_Ind = rematch_Ind[['delta_vote', 'delta_spend']]
X = df_Ind['delta_spend']
y = df_Ind['delta_vote']
X = sm.add_constant(X)
model_Ind = sm.OLS(y, X).fit()
predictions = model_Ind.predict(X)

# PLOT SCATTER for GOP, Dem, Ind subsets
x1 = rematch_GOP['delta_vote']
y1 = rematch_GOP['delta_spend']
x2 = rematch_Dem['delta_vote']
y2 = rematch_Dem['delta_spend']
x3 = rematch_Ind['delta_vote']
y3 = rematch_Ind['delta_spend']

x = np.linspace(-6000000, 6000000, num=1200)

fig, ax = plt.subplots(1, figsize=(20,12))
ax.scatter(y1, x1, alpha=1, s=15)
ax.scatter(y2, x2, alpha=1, s=15)
ax.scatter(y3, x3, color='yellow', alpha=1, s=15)

# plot Ind line
ax.plot(x, Ind_f(x), '-', color='yellow')
# plot Dem line
ax.plot(x, Dem_f(x), '-', color='blue')
# plot GOP line
ax.plot(x, GOP_f(x), '-', color='red')


ax.set_xlim(-6000000, 6000000)
ax.set_ylim(-80, 80)
ax.set_title('Comparing Spending and Vote Percentages \n across US Congressional Rematch Elections (1980 - 2018)', fontsize=30)
ax.set_xlabel('Change in Money Spent', fontsize=24)
ax.set_ylabel('Change in Vote Point', fontsize=24)
ax.xaxis.labelpad = 20 #move position of x-axis label, but not x ticks
ax.yaxis.labelpad = 20 #move position of x-axis label (but not y ticks)

#must add: import matplotlib.ticker as ticker
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

### next three lines make y labels into percentages
vals = ax.get_yticks()
percents = [x/100 for x in vals] #if already in decimal format, skip this
ax.set_yticklabels(['{:,.0%}'.format(x) for x in percents])

plt.xticks(rotation=45) #rotate x labels

# SUBSETS of DF by decade
rematch_80s = rematch_df[rematch_df['year']<1990]
rematch_90s = rematch_df[(rematch_df['year']<2000) & (rematch_df['year']>1989)]
rematch_00s = rematch_df[(rematch_df['year']<2010) & (rematch_df['year']>1999)]
rematch_10s = rematch_df[rematch_df['year']>2009]

# LINEAR REGRESSION for Decade subsets
df_80s = rematch_80s[['delta_vote', 'delta_spend']]
X = df_80s['delta_spend']
y = df_80s['delta_vote']
X = sm.add_constant(X)
model_80s = sm.OLS(y, X).fit()
predictions = model_80s.predict(X)

df_90s = rematch_90s[['delta_vote', 'delta_spend']]
X = df_90s['delta_spend']
y = df_90s['delta_vote']
X = sm.add_constant(X)
model_90s = sm.OLS(y, X).fit()
predictions = model_90s.predict(X)

df_00s = rematch_00s[['delta_vote', 'delta_spend']]
X = df_00s['delta_spend']
y = df_00s['delta_vote']
X = sm.add_constant(X)
model_00s = sm.OLS(y, X).fit()
predictions = model_00s.predict(X)

df_10s = rematch_10s[['delta_vote', 'delta_spend']]
X = df_10s['delta_spend']
y = df_10s['delta_vote']
X = sm.add_constant(X)
model_10s = sm.OLS(y, X).fit()
predictions = model_10s.predict(X)

# DEFINE BEST FIT LINE for Decade subsets
def Y80_f(x):
    return  model_80s.params[1]*x + model_80s.params[0]
def Y90_f(x):
    return  model_90s.params[1]*x + model_90s.params[0]
def Y00_f(x):
    return  model_00s.params[1]*x + model_00s.params[0]
def Y10_f(x):
    return  model_10s.params[1]*x + model_10s.params[0]

# PLOT 
fig, ax = plt.subplots(1, figsize=(20,12))
ax.scatter(rematch_80s['delta_spend'], rematch_80s['delta_vote'], alpha=1, s=15, color='#02ab2e', label='1980-1988')
ax.scatter(rematch_90s['delta_spend'], rematch_90s['delta_vote'], alpha=.7, s=15, color='#9a0eea', label='1990-1998')
ax.scatter(rematch_00s['delta_spend'], rematch_00s['delta_vote'], alpha=.7, s=15, color='#fe46a5', label='2000-2008')
ax.scatter(rematch_10s['delta_spend'], rematch_10s['delta_vote'], alpha=.7, s=15, color='#0485d1', label='2010-2018')

# plot 80s line
ax.plot(x, Y80_f(x), '-', color='#02ab2e')
# plot 90s line
ax.plot(x, Y90_f(x), '-', color='#9a0eea')
# plot 00s line
ax.plot(x, Y00_f(x), '-', color='#fe46a5')
# plot 10s line
ax.plot(x, Y10_f(x), '-', color='#0485d1')

ax.legend(loc='lower right', frameon=False, fontsize='x-large')


ax.set_xlim(-6000000, 6000000)
ax.set_ylim(-80, 80)
ax.set_title('Comparing Spending and Vote Percentages \n across US Congressional Rematch Elections (1980 - 2018)', fontsize=30)
ax.set_xlabel('Change in Money Spent', fontsize=24)
ax.set_ylabel('Change in Vote Percent', fontsize=24)
ax.xaxis.labelpad = 20 #move position of x-axis label, but not x ticks
ax.yaxis.labelpad = 20 #move position of x-axis label (but not y ticks)



#must add: import matplotlib.ticker as ticker
#
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

### next three lines make y labels into percentages
vals = ax.get_yticks()
percents = [x/100 for x in vals] #if already in decimal format, skip this
ax.set_yticklabels(['{:,.0%}'.format(x) for x in percents])

plt.xticks(rotation=45) #rotate x labels

