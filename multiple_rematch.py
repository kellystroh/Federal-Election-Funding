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


mult_rematch_list = [each for each in rem.rematch_list if len(each)>2]
len(mult_rematch_list)

mult_dict = {}
for each in mult_rematch_list:
    if len(each) not in mult_dict:
        mult_dict[len(each)] = []
    mult_dict[len(each)].append(each)
mult_dict



