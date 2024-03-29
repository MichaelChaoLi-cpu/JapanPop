# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 11:13:14 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from joblib import Parallel, delayed
from sklearn.linear_model import LinearRegression
import matplotlib as mpl

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green","yellow","red"])

result_folder = "F:\\17_Article\\04_Result\\"
figure_location = "C:\\Users\\li.chao.987@s.kyushu-u.ac.jp\\OneDrive - Kyushu University\\17_Article\\03_RStudio\\05_Figure\\"

#### total population
# 2005
total_pop_cv_2005 = pd.read_csv(result_folder + "SKlearn_1000tree_TotalPopLog_DF_cv_2005.csv")
total_pop_cv_2005 = total_pop_cv_2005.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(total_pop_cv_2005.TotalPopLog, total_pop_cv_2005.y_pred2005, (xedges, yedges))

xidx = np.clip(np.digitize(total_pop_cv_2005.TotalPopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(total_pop_cv_2005.y_pred2005, yedges), 0, hist.shape[1] - 1)
c_2005 = hist[xidx, yidx]
c_2005[c_2005 > 30000] = 30000

reg_2005 = LinearRegression().fit(pd.DataFrame(total_pop_cv_2005.TotalPopLog), total_pop_cv_2005.y_pred2005)
reg_2005.coef_
reg_2005.intercept_

# 2010
total_pop_cv_2010 = pd.read_csv(result_folder + "SKlearn_1000tree_TotalPopLog_DF_cv_2010.csv")
total_pop_cv_2010 = total_pop_cv_2010.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(total_pop_cv_2010.TotalPopLog, total_pop_cv_2010.y_pred2010, (xedges, yedges))

xidx = np.clip(np.digitize(total_pop_cv_2010.TotalPopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(total_pop_cv_2010.y_pred2010, yedges), 0, hist.shape[1] - 1)
c_2010 = hist[xidx, yidx]
c_2010[c_2010 > 30000] = 30000

reg_2010 = LinearRegression().fit(pd.DataFrame(total_pop_cv_2010.TotalPopLog), total_pop_cv_2010.y_pred2010)
reg_2010.coef_
reg_2010.intercept_

# 2015
total_pop_cv_2015 = pd.read_csv(result_folder + "SKlearn_1000tree_TotalPopLog_DF_cv_2015.csv")
total_pop_cv_2015 = total_pop_cv_2015.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(total_pop_cv_2015.TotalPopLog, total_pop_cv_2015.y_pred2015, (xedges, yedges))

xidx = np.clip(np.digitize(total_pop_cv_2015.TotalPopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(total_pop_cv_2015.y_pred2015, yedges), 0, hist.shape[1] - 1)
c_2015 = hist[xidx, yidx]
c_2015[c_2015 > 30000] = 30000

reg_2015 = LinearRegression().fit(pd.DataFrame(total_pop_cv_2015.TotalPopLog), total_pop_cv_2015.y_pred2015)
reg_2015.coef_
reg_2015.intercept_

# 2020
total_pop_cv_2020 = pd.read_csv(result_folder + "SKlearn_1000tree_TotalPopLog_DF_cv_2020.csv")
total_pop_cv_2020 = total_pop_cv_2020.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(total_pop_cv_2020.TotalPopLog, total_pop_cv_2020.y_pred2005, (xedges, yedges))

xidx = np.clip(np.digitize(total_pop_cv_2020.TotalPopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(total_pop_cv_2020.y_pred2005, yedges), 0, hist.shape[1] - 1)
c_2020 = hist[xidx, yidx]
c_2020[c_2020 > 30000] = 30000

reg_2020 = LinearRegression().fit(pd.DataFrame(total_pop_cv_2020.TotalPopLog), total_pop_cv_2020.y_pred2005)
reg_2020.coef_
reg_2020.intercept_

# figure
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(20, 21), dpi=1000,
                        gridspec_kw={'height_ratios': [10, 10, 1]})
ax_legend = fig.add_axes([0.1, 0.075, 0.8, 0.05])
axs[0,0].scatter(total_pop_cv_2005.TotalPopLog, total_pop_cv_2005.y_pred2005, 
            c=c_2005, cmap=cmap)
axs[0,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
axs[0,0].axline((0, reg_2005.intercept_), (10, (reg_2005.intercept_ + 10 * reg_2005.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2005.coef_[0], 2))+"x + " + str(round(reg_2005.intercept_, 2)))
axs[0,0].grid(True)
axs[0,0].legend()
axs[0,0].text(9, 9.7, "a", fontsize=20)
axs[0,0].set_xlabel("Logarithm of the Observed Total Population in 2005", fontsize=15)
axs[0,0].set_ylabel("Logarithm of the Predicted Total Population in 2005", fontsize=15)
axs[0,0].set_xlim([0, 10])
axs[0,0].set_ylim([0, 10])

axs[0,1].scatter(total_pop_cv_2010.TotalPopLog, total_pop_cv_2010.y_pred2010, 
            c=c_2010, cmap=cmap)
axs[0,1].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
axs[0,1].axline((0, reg_2010.intercept_), (10, (reg_2010.intercept_ + 10 * reg_2010.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2010.coef_[0], 2))+"x + " + str(round(reg_2010.intercept_, 2)))
axs[0,1].grid(True)
axs[0,1].legend()
axs[0,1].text(9, 9.7, "b", fontsize=20)
axs[0,1].set_xlabel("Logarithm of the Observed Total Population in 2010", fontsize=15)
axs[0,1].set_ylabel("Logarithm of the Predicted Total Population in 2010", fontsize=15)
axs[0,1].set_xlim([0, 10])
axs[0,1].set_ylim([0, 10])


axs[1,0].scatter(total_pop_cv_2015.TotalPopLog, total_pop_cv_2015.y_pred2015, 
            c=c_2015, cmap=cmap)
axs[1,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
axs[1,0].axline((0, reg_2015.intercept_), (10, (reg_2015.intercept_ + 10 * reg_2015.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2015.coef_[0], 2))+"x + " + str(round(reg_2015.intercept_, 2)))
axs[1,0].grid(True)
axs[1,0].legend()
axs[1,0].text(9, 9.7, "c", fontsize=20)
axs[1,0].set_xlabel("Logarithm of the Observed Total Population in 2015", fontsize=15)
axs[1,0].set_ylabel("Logarithm of the Predicted Total Population in 2015", fontsize=15)
axs[1,0].set_xlim([0, 10])
axs[1,0].set_ylim([0, 10])

axs[1,1].scatter(total_pop_cv_2020.TotalPopLog, total_pop_cv_2020.y_pred2005, 
            c=c_2020, cmap=cmap)
axs[1,1].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
axs[1,1].axline((0, reg_2020.intercept_), (10, (reg_2020.intercept_ + 10 * reg_2020.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2020.coef_[0], 2))+"x + " + str(round(reg_2020.intercept_, 2)))
axs[1,1].grid(True)
axs[1,1].legend()
axs[1,1].text(9, 9.7, "d", fontsize=20)
axs[1,1].set_xlabel("Logarithm of the Observed Total Population in 2020", fontsize=15)
axs[1,1].set_ylabel("Logarithm of the Predicted Total Population in 2020", fontsize=15)
axs[1,1].set_xlim([0, 10])
axs[1,1].set_ylim([0, 10])

axs[2, 0].axis('off')
axs[2, 1].axis('off')

norm = mpl.colors.Normalize(vmin=0, vmax=30000)
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                    cax=ax_legend, orientation='horizontal')
cbar.set_label('Density',size=24)
cbar.ax.tick_params(labelsize=18) 

plt.show();

fig.savefig(figure_location + "CV_total.jpg")

#### female population
# 2005
female_pop_cv_2005 = pd.read_csv(result_folder + "SKlearn_1000tree_FemalePopLog_DF_cv_2005.csv")
female_pop_cv_2005 = female_pop_cv_2005.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(female_pop_cv_2005.FemalePopLog, female_pop_cv_2005.y_pred2005, (xedges, yedges))

xidx = np.clip(np.digitize(female_pop_cv_2005.FemalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(female_pop_cv_2005.y_pred2005, yedges), 0, hist.shape[1] - 1)
c_2005 = hist[xidx, yidx]
c_2005[c_2005 > 30000] = 30000

reg_2005 = LinearRegression().fit(pd.DataFrame(female_pop_cv_2005.FemalePopLog), female_pop_cv_2005.y_pred2005)
reg_2005.coef_
reg_2005.intercept_

# 2010
female_pop_cv_2010 = pd.read_csv(result_folder + "SKlearn_1000tree_FemalePopLog_DF_cv_2010.csv")
female_pop_cv_2010 = female_pop_cv_2010.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(female_pop_cv_2010.FemalePopLog, female_pop_cv_2010.y_pred2010, (xedges, yedges))

xidx = np.clip(np.digitize(female_pop_cv_2010.FemalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(female_pop_cv_2010.y_pred2010, yedges), 0, hist.shape[1] - 1)
c_2010 = hist[xidx, yidx]
c_2010[c_2010 > 30000] = 30000

reg_2010 = LinearRegression().fit(pd.DataFrame(female_pop_cv_2010.FemalePopLog), female_pop_cv_2010.y_pred2010)
reg_2010.coef_
reg_2010.intercept_

# 2015
female_pop_cv_2015 = pd.read_csv(result_folder + "SKlearn_1000tree_FemalePopLog_DF_cv_2015.csv")
female_pop_cv_2015 = female_pop_cv_2015.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(female_pop_cv_2015.FemalePopLog, female_pop_cv_2015.y_pred2015, (xedges, yedges))

xidx = np.clip(np.digitize(female_pop_cv_2015.FemalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(female_pop_cv_2015.y_pred2015, yedges), 0, hist.shape[1] - 1)
c_2015 = hist[xidx, yidx]
c_2015[c_2015 > 30000] = 30000

reg_2015 = LinearRegression().fit(pd.DataFrame(female_pop_cv_2015.FemalePopLog), female_pop_cv_2015.y_pred2015)
reg_2015.coef_
reg_2015.intercept_

# 2020
female_pop_cv_2020 = pd.read_csv(result_folder + "SKlearn_1000tree_FemalePopLog_DF_cv_2020.csv")
female_pop_cv_2020 = female_pop_cv_2020.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(female_pop_cv_2020.FemalePopLog, female_pop_cv_2020.y_pred2005, (xedges, yedges))

xidx = np.clip(np.digitize(female_pop_cv_2020.FemalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(female_pop_cv_2020.y_pred2005, yedges), 0, hist.shape[1] - 1)
c_2020 = hist[xidx, yidx]
c_2020[c_2020 > 30000] = 30000

reg_2020 = LinearRegression().fit(pd.DataFrame(female_pop_cv_2020.FemalePopLog), female_pop_cv_2020.y_pred2005)
reg_2020.coef_
reg_2020.intercept_

# figure
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(20, 21), dpi=1000,
                        gridspec_kw={'height_ratios': [10, 10, 1]})
ax_legend = fig.add_axes([0.1, 0.075, 0.8, 0.05])
ax1=axs[0,0]
ax2=axs[0,1]
ax3=axs[1,0]
ax4=axs[1,1]
ax1.scatter(female_pop_cv_2005.FemalePopLog, female_pop_cv_2005.y_pred2005, 
            c=c_2005, cmap=cmap)
ax1.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax1.axline((0, reg_2005.intercept_), (10, (reg_2005.intercept_ + 10 * reg_2005.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2005.coef_[0], 2))+"x + " + str(round(reg_2005.intercept_, 2)))
ax1.grid(True)
ax1.legend()
ax1.text(9, 9.7, "a", fontsize=20)
ax1.set_xlabel("Logarithm of the Observed Female Population in 2005", fontsize=15)
ax1.set_ylabel("Logarithm of the Predicted Female Population in 2005", fontsize=15)
ax1.set_xlim([0, 10])
ax1.set_ylim([0, 10])

ax2.scatter(female_pop_cv_2010.FemalePopLog, female_pop_cv_2010.y_pred2010, 
            c=c_2010, cmap=cmap)
ax2.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax2.axline((0, reg_2010.intercept_), (10, (reg_2010.intercept_ + 10 * reg_2010.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2010.coef_[0], 2))+"x + " + str(round(reg_2010.intercept_, 2)))
ax2.grid(True)
ax2.legend()
ax2.text(9, 9.7, "b", fontsize=20)
ax2.set_xlabel("Logarithm of the Observed Female Population in 2010", fontsize=15)
ax2.set_ylabel("Logarithm of the Predicted Female Population in 2010", fontsize=15)
ax2.set_xlim([0, 10])
ax2.set_ylim([0, 10])

ax3.scatter(female_pop_cv_2015.FemalePopLog, female_pop_cv_2015.y_pred2015, 
            c=c_2015, cmap=cmap)
ax3.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax3.axline((0, reg_2015.intercept_), (10, (reg_2015.intercept_ + 10 * reg_2015.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2015.coef_[0], 2))+"x + " + str(round(reg_2015.intercept_, 2)))
ax3.grid(True)
ax3.legend()
ax3.text(9, 9.7, "c", fontsize=20)
ax3.set_xlabel("Logarithm of the Observed Female Population in 2015", fontsize=15)
ax3.set_ylabel("Logarithm of the Predicted Female Population in 2015", fontsize=15)
ax3.set_xlim([0, 10])
ax3.set_ylim([0, 10])

ax4.scatter(female_pop_cv_2020.FemalePopLog, female_pop_cv_2020.y_pred2005, 
            c=c_2020, cmap=cmap)
ax4.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax4.axline((0, reg_2020.intercept_), (10, (reg_2020.intercept_ + 10 * reg_2020.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2020.coef_[0], 2))+"x + " + str(round(reg_2020.intercept_, 2)))
ax4.grid(True)
ax4.legend()
ax4.text(9, 9.7, "c", fontsize=20)
ax4.set_xlabel("Logarithm of the Observed Female Population in 2020", fontsize=15)
ax4.set_ylabel("Logarithm of the Predicted Female Population in 2020", fontsize=15)
ax4.set_xlim([0, 10])
ax4.set_ylim([0, 10])

axs[2, 0].axis('off')
axs[2, 1].axis('off')

norm = mpl.colors.Normalize(vmin=0, vmax=30000)
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                    cax=ax_legend, orientation='horizontal')
cbar.set_label('Density',size=24)
cbar.ax.tick_params(labelsize=18) 

fig.savefig(figure_location + "CV_female.jpg")

#### male population
# 2005
male_pop_cv_2005 = pd.read_csv(result_folder + "SKlearn_1000tree_MalePopLog_DF_cv_2005.csv")
male_pop_cv_2005 = male_pop_cv_2005.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(male_pop_cv_2005.MalePopLog, male_pop_cv_2005.y_pred2005, (xedges, yedges))

xidx = np.clip(np.digitize(male_pop_cv_2005.MalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(male_pop_cv_2005.y_pred2005, yedges), 0, hist.shape[1] - 1)
c_2005 = hist[xidx, yidx]
c_2005[c_2005 > 30000] = 30000

reg_2005 = LinearRegression().fit(pd.DataFrame(male_pop_cv_2005.MalePopLog), male_pop_cv_2005.y_pred2005)
reg_2005.coef_
reg_2005.intercept_

# 2010
male_pop_cv_2010 = pd.read_csv(result_folder + "SKlearn_1000tree_MalePopLog_DF_cv_2010.csv")
male_pop_cv_2010 = male_pop_cv_2010.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(male_pop_cv_2010.MalePopLog, male_pop_cv_2010.y_pred2010, (xedges, yedges))

xidx = np.clip(np.digitize(male_pop_cv_2010.MalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(male_pop_cv_2010.y_pred2010, yedges), 0, hist.shape[1] - 1)
c_2010 = hist[xidx, yidx]
c_2010[c_2010 > 30000] = 30000

reg_2010 = LinearRegression().fit(pd.DataFrame(male_pop_cv_2010.MalePopLog), male_pop_cv_2010.y_pred2010)
reg_2010.coef_
reg_2010.intercept_

# 2015
male_pop_cv_2015 = pd.read_csv(result_folder + "SKlearn_1000tree_MalePopLog_DF_cv_2015.csv")
male_pop_cv_2015 = male_pop_cv_2015.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(male_pop_cv_2015.MalePopLog, male_pop_cv_2015.y_pred2015, (xedges, yedges))

xidx = np.clip(np.digitize(male_pop_cv_2015.MalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(male_pop_cv_2015.y_pred2015, yedges), 0, hist.shape[1] - 1)
c_2015 = hist[xidx, yidx]
c_2015[c_2015 > 30000] = 30000

reg_2015 = LinearRegression().fit(pd.DataFrame(male_pop_cv_2015.MalePopLog), male_pop_cv_2015.y_pred2015)
reg_2015.coef_
reg_2015.intercept_

# 2020
male_pop_cv_2020 = pd.read_csv(result_folder + "SKlearn_1000tree_MalePopLog_DF_cv_2020.csv")
male_pop_cv_2020 = male_pop_cv_2020.set_index(["G04c_001", "year"])

xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
hist, xedges, yedges = np.histogram2d(male_pop_cv_2020.MalePopLog, male_pop_cv_2020.y_pred2005, (xedges, yedges))

xidx = np.clip(np.digitize(male_pop_cv_2020.MalePopLog, xedges), 0, hist.shape[0] - 1)
yidx = np.clip(np.digitize(male_pop_cv_2020.y_pred2005, yedges), 0, hist.shape[1] - 1)
c_2020 = hist[xidx, yidx]
c_2020[c_2020 > 30000] = 30000

reg_2020 = LinearRegression().fit(pd.DataFrame(male_pop_cv_2020.MalePopLog), male_pop_cv_2020.y_pred2005)
reg_2020.coef_
reg_2020.intercept_

# figure
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(20, 21), dpi=1000,
                        gridspec_kw={'height_ratios': [10, 10, 1]})
ax_legend = fig.add_axes([0.1, 0.075, 0.8, 0.05])
ax1=axs[0,0]
ax2=axs[0,1]
ax3=axs[1,0]
ax4=axs[1,1]
ax1.scatter(male_pop_cv_2005.MalePopLog, male_pop_cv_2005.y_pred2005, 
            c=c_2005, cmap=cmap)
ax1.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax1.axline((0, reg_2005.intercept_), (10, (reg_2005.intercept_ + 10 * reg_2005.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2005.coef_[0], 2))+"x + " + str(round(reg_2005.intercept_, 2)))
ax1.grid(True)
ax1.legend()
ax1.text(9, 9.7, "a", fontsize=20)
ax1.set_xlabel("Logarithm of the Observed Male Population in 2005", fontsize=15)
ax1.set_ylabel("Logarithm of the Predicted Male Population in 2005", fontsize=15)
ax1.set_xlim([0, 10])
ax1.set_ylim([0, 10])

ax2.scatter(male_pop_cv_2010.MalePopLog, male_pop_cv_2010.y_pred2010, 
            c=c_2010, cmap=cmap)
ax2.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax2.axline((0, reg_2010.intercept_), (10, (reg_2010.intercept_ + 10 * reg_2010.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2010.coef_[0], 2))+"x + " + str(round(reg_2010.intercept_, 2)))
ax2.grid(True)
ax2.legend()
ax2.text(9, 9.7, "b", fontsize=20)
ax2.set_xlabel("Logarithm of the Observed Male Population in 2010", fontsize=15)
ax2.set_ylabel("Logarithm of the Predicted Male Population in 2010", fontsize=15)
ax2.set_xlim([0, 10])
ax2.set_ylim([0, 10])

ax3.scatter(male_pop_cv_2015.MalePopLog, male_pop_cv_2015.y_pred2015, 
            c=c_2015, cmap=cmap)
ax3.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax3.axline((0, reg_2015.intercept_), (10, (reg_2015.intercept_ + 10 * reg_2015.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2015.coef_[0], 2))+"x + " + str(round(reg_2015.intercept_, 2)))
ax3.grid(True)
ax3.legend()
ax3.text(9, 9.7, "c", fontsize=20)
ax3.set_xlabel("Logarithm of the Observed Male Population in 2015", fontsize=15)
ax3.set_ylabel("Logarithm of the Predicted Male Population in 2015", fontsize=15)
ax3.set_xlim([0, 10])
ax3.set_ylim([0, 10])

ax4.scatter(male_pop_cv_2020.MalePopLog, male_pop_cv_2020.y_pred2005, 
            c=c_2020, cmap=cmap)
ax4.axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
           label='y = x')
ax4.axline((0, reg_2020.intercept_), (10, (reg_2020.intercept_ + 10 * reg_2020.coef_[0])), 
           linewidth=6, color='blue', alpha=0.4, linestyle='--',
           label='y = ' + str(round(reg_2020.coef_[0], 2))+"x + " + str(round(reg_2020.intercept_, 2)))
ax4.grid(True)
ax4.legend()
ax4.text(9, 9.7, "c", fontsize=20)
ax4.set_xlabel("Logarithm of the Observed Male Population in 2020", fontsize=15)
ax4.set_ylabel("Logarithm of the Predicted Male Population in 2020", fontsize=15)
ax4.set_xlim([0, 10])
ax4.set_ylim([0, 10])

axs[2, 0].axis('off')
axs[2, 1].axis('off')

norm = mpl.colors.Normalize(vmin=0, vmax=30000)
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                    cax=ax_legend, orientation='horizontal')
cbar.set_label('Density',size=24)
cbar.ax.tick_params(labelsize=18) 

fig.savefig(figure_location + "CV_male.jpg")