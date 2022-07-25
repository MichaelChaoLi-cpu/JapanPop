# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:45:22 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import matplotlib.pyplot as plt
import matplotlib.colors
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
##### y
realPopDf_Y = pd.read_pickle(single_dataset_location + "03_population.pkl")

result_location = "F:\\17_Article\\04_Result\\"
figure_location = "C:\\Users\\li.chao.987@s.kyushu-u.ac.jp\\OneDrive - Kyushu University\\17_Article\\03_RStudio\\05_Figure\\"

total_pop_result = pd.read_csv(result_location + "SKlearn_1000tree_total_pop_log.csv")
total_pop_result.G04c_001 = total_pop_result.G04c_001.astype('int32')
total_pop_result.year = total_pop_result.year.astype('int32')
total_pop_result = total_pop_result.set_index(['G04c_001', 'year'])

##### cv test
fittingModelResultDf = pd.concat([realPopDf_Y, total_pop_result], axis = 1, join='inner')
fittingModelResultDf['TotalPop_log'] = np.log(fittingModelResultDf['TotalPop'] + 1)
fittingModelResultDf = fittingModelResultDf.rename(columns={'bigy_pred':'TotalPop_log_pred'})
fittingModelResultDf['TotalPop_pred'] = np.exp(fittingModelResultDf['TotalPop_log_pred']) - 1

# figure total fitting model
xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop_log, 
                                      fittingModelResultDf.TotalPop_log_pred, 
                                      (xedges, yedges))

xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log_pred, yedges), 0, hist.shape[1] - 1)
c = hist[xidx, yidx]

reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop_log), fittingModelResultDf.TotalPop_log_pred)
reg.coef_
reg.intercept_
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 10), dpi=1000)
ax1.scatter(fittingModelResultDf.TotalPop_log, fittingModelResultDf.TotalPop_log_pred, 
            c=c, cmap='jet')
ax1.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax1.axline((0, reg.intercept_), (10, (reg.intercept_ + 10 * reg.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
ax1.grid(True)
ax1.legend()
ax1.text(9, 9.7, "a", fontsize=20)
ax1.set_xlabel("Logarithm of the Observed Total Population", fontsize=15)
ax1.set_ylabel("Logarithm of the Predicted Total Population", fontsize=15)
ax1.set_xlim([0, 10])
ax1.set_ylim([0, 10])

xedges, yedges = np.linspace(0, 16000, 41), np.linspace(0, 16000, 41)
hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop, 
                                      fittingModelResultDf.TotalPop_pred, 
                                      (xedges, yedges))

xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_pred, yedges), 0, hist.shape[1] - 1)
c = hist[xidx, yidx]

reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop), fittingModelResultDf.TotalPop_pred)
reg.coef_
reg.intercept_

ax2.scatter(fittingModelResultDf.TotalPop, fittingModelResultDf.TotalPop_pred, 
            c=c, cmap='jet')
ax2.axline((0, 0), (16000, 16000), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax2.axline((0, reg.intercept_), (16000, (reg.intercept_ + 16000 * reg.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
ax2.grid(True)
ax2.legend()
ax2.text(15000, 15500, "b", fontsize=20)
ax2.set_xlabel("the Observed Total Population", fontsize=15)
ax2.set_ylabel("the Predicted Total Population", fontsize=15)
ax2.set_xlim([0, 16000])
ax2.set_ylim([0, 16000])

plt.show();

fig.savefig(figure_location + "fittingModel_total.jpg")