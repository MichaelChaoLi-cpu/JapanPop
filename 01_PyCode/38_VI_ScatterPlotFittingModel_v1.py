# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:45:22 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import matplotlib.pyplot as plt
import matplotlib.colors
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib as mpl

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green","yellow","red"])

single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
##### y
realPopDf_Y = pd.read_pickle(single_dataset_location + "03_population.pkl")

result_location = "F:\\17_Article\\04_Result\\"
figure_location = "C:\\Users\\li.chao.987@s.kyushu-u.ac.jp\\OneDrive - Kyushu University\\17_Article\\03_RStudio\\05_Figure\\"

def drawTotalPop(result_location, figure_location, realPopDf_Y):
    #### total pop 
    total_pop_result = pd.read_csv(result_location + "SKlearn_1000tree_total_pop_log.csv")
    total_pop_result.G04c_001 = total_pop_result.G04c_001.astype('int32')
    total_pop_result.year = total_pop_result.year.astype('int32')
    total_pop_result = total_pop_result.set_index(['G04c_001', 'year'])
    total_pop_result = total_pop_result.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    realPopDf_Y = realPopDf_Y.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    
    ##### log back
    fittingModelResultDf = pd.concat([realPopDf_Y, total_pop_result], axis = 1, join='outer')
    fittingModelResultDf = fittingModelResultDf.dropna(subset = 'bigy_pred')
    fittingModelResultDf = fittingModelResultDf.fillna(0)
    fittingModelResultDf['TotalPop_log'] = np.log(fittingModelResultDf['TotalPop'] + 1)
    fittingModelResultDf = fittingModelResultDf.rename(columns={'bigy_pred':'TotalPop_log_pred'})
    fittingModelResultDf['TotalPop_pred'] = np.exp(fittingModelResultDf['TotalPop_log_pred']) - 1
    
    # figure total fitting model
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(20, 21), dpi=1000,
                            gridspec_kw={'height_ratios': [10, 10, 1]})
    
    xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop_log, 
                                          fittingModelResultDf.TotalPop_log_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 30000] = 30000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop_log), fittingModelResultDf.TotalPop_log_pred)
    reg.coef_
    reg.intercept_
    
    axs[0,0].scatter(fittingModelResultDf.TotalPop_log, fittingModelResultDf.TotalPop_log_pred, 
                     c=c, cmap=cmap)
    axs[0,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[0,0].axline((0, reg.intercept_), (10, (reg.intercept_ + 10 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[0,0].grid(True)
    axs[0,0].legend()
    axs[0,0].text(9, 9.7, "a", fontsize=20)
    axs[0,0].set_xlabel("Logarithm of the Observed Total Population", fontsize=15)
    axs[0,0].set_ylabel("Logarithm of the Predicted Total Population", fontsize=15)
    axs[0,0].set_xlim([0, 10])
    axs[0,0].set_ylim([0, 10])
    
    xedges, yedges = np.linspace(0, 11000, 41), np.linspace(0, 11000, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop, 
                                          fittingModelResultDf.TotalPop_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 30000] = 30000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop), fittingModelResultDf.TotalPop_pred)
    reg.coef_
    reg.intercept_
    
    axs[0,1].scatter(fittingModelResultDf.TotalPop, fittingModelResultDf.TotalPop_pred, 
                     c=c, cmap=cmap)
    axs[0,1].axline((0, 0), (11000, 11000), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[0,1].axline((0, reg.intercept_), (11000, (reg.intercept_ + 11000 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[0,1].grid(True)
    axs[0,1].legend()
    axs[0,1].text(10000, 10500, "b", fontsize=20)
    axs[0,1].set_xlabel("the Observed Total Population", fontsize=15)
    axs[0,1].set_ylabel("the Predicted Total Population", fontsize=15)
    axs[0,1].set_xlim([0, 11000])
    axs[0,1].set_ylim([0, 11000])
    
    #### total pop 
    total_pop_result_cv = pd.read_csv(result_location + "SKlearn_1000tree_TotalPopLog_DF_cv_3_7.csv")
    total_pop_result_cv.G04c_001 = total_pop_result_cv.G04c_001.astype('int32')
    total_pop_result_cv.year = total_pop_result_cv.year.astype('int32')
    total_pop_result_cv = total_pop_result_cv.set_index(['G04c_001', 'year'])
    
    ##### log back
    fittingModelResultDf = total_pop_result_cv.copy()
    fittingModelResultDf['TotalPop_count'] = np.exp(fittingModelResultDf['TotalPopLog']) - 1
    fittingModelResultDf['TotalPop_countpred'] = np.exp(fittingModelResultDf['y_pred']) - 1
    
    xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPopLog, 
                                          fittingModelResultDf.y_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPopLog, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.y_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 5000] = 5000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPopLog), fittingModelResultDf.y_pred)
    reg.coef_
    reg.intercept_
    
    axs[1,0].scatter(fittingModelResultDf.TotalPopLog, fittingModelResultDf.y_pred, 
                     c=c, cmap=cmap)
    axs[1,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[1,0].axline((0, reg.intercept_), (10, (reg.intercept_ + 10 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[1,0].grid(True)
    axs[1,0].legend()
    axs[1,0].text(9, 9.7, "c", fontsize=20)
    axs[1,0].set_xlabel("Logarithm of the Observed Total Population", fontsize=15)
    axs[1,0].set_ylabel("Logarithm of the Predicted Total Population", fontsize=15)
    axs[1,0].set_xlim([0, 10])
    axs[1,0].set_ylim([0, 10])
    
    xedges, yedges = np.linspace(0, 11000, 41), np.linspace(0, 11000, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop_count, 
                                          fittingModelResultDf.TotalPop_countpred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_count, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_countpred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 5000] = 5000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop_count), fittingModelResultDf.TotalPop_countpred)
    reg.coef_
    reg.intercept_
    
    axs[1,1].scatter(fittingModelResultDf.TotalPop_count, fittingModelResultDf.TotalPop_countpred, 
                     c=c, cmap=cmap)
    axs[1,1].axline((0, 0), (11000, 11000), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[1,1].axline((0, reg.intercept_), (11000, (reg.intercept_ + 11000 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[1,1].grid(True)
    axs[1,1].legend()
    axs[1,1].text(10000, 10500, "d", fontsize=20)
    axs[1,1].set_xlabel("the Observed Total Population", fontsize=15)
    axs[1,1].set_ylabel("the Predicted Total Population", fontsize=15)
    axs[1,1].set_xlim([0, 11000])
    axs[1,1].set_ylim([0, 11000])
    
    norm = mpl.colors.Normalize(vmin=0, vmax=30000)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        cax=axs[2,0], orientation='horizontal')
    cbar.set_label('Density',size=24)
    cbar.ax.tick_params(labelsize=18) 
    
    norm = mpl.colors.Normalize(vmin=0, vmax=5000)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        cax=axs[2,1], orientation='horizontal')
    cbar.set_label('Density',size=24)
    cbar.ax.tick_params(labelsize=18) 
    #plt.show();
    
    fig.savefig(figure_location + "fittingModel_total.jpg")

def drawMalePop(result_location, figure_location, realPopDf_Y):
    total_pop_result = pd.read_csv(result_location + "SKlearn_1000tree_male_pop_log.csv")
    total_pop_result.G04c_001 = total_pop_result.G04c_001.astype('int32')
    total_pop_result.year = total_pop_result.year.astype('int32')
    total_pop_result = total_pop_result.set_index(['G04c_001', 'year'])
    total_pop_result = total_pop_result.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    realPopDf_Y = realPopDf_Y.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    
    ##### log back
    fittingModelResultDf = pd.concat([realPopDf_Y, total_pop_result], axis = 1, join='outer')
    fittingModelResultDf = fittingModelResultDf.dropna(subset = 'bigy_pred')
    fittingModelResultDf = fittingModelResultDf.fillna(0)
    fittingModelResultDf['TotalPop_log'] = np.log(fittingModelResultDf['MalePop'] + 1)
    ################################################ Revise here is enough ^^^^
    fittingModelResultDf = fittingModelResultDf.rename(columns={'bigy_pred':'TotalPop_log_pred'})
    fittingModelResultDf['TotalPop_pred'] = np.exp(fittingModelResultDf['TotalPop_log_pred']) - 1
    fittingModelResultDf = fittingModelResultDf[['MalePop', 'TotalPop_log_pred',
                                                 'TotalPop_log', 'TotalPop_pred']]
    fittingModelResultDf = fittingModelResultDf.rename(columns={'MalePop':'TotalPop'})
    
    # figure total fitting model
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(20, 21), dpi=1000,
                            gridspec_kw={'height_ratios': [10, 10, 1]})
    
    xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop_log, 
                                          fittingModelResultDf.TotalPop_log_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 30000] = 30000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop_log), fittingModelResultDf.TotalPop_log_pred)
    reg.coef_
    reg.intercept_
    
    axs[0,0].scatter(fittingModelResultDf.TotalPop_log, fittingModelResultDf.TotalPop_log_pred, 
                     c=c, cmap=cmap)
    axs[0,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[0,0].axline((0, reg.intercept_), (10, (reg.intercept_ + 10 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[0,0].grid(True)
    axs[0,0].legend()
    axs[0,0].text(9, 9.7, "a", fontsize=20)
    axs[0,0].set_xlabel("Logarithm of the Observed Male Population", fontsize=15)
    axs[0,0].set_ylabel("Logarithm of the Predicted Male Population", fontsize=15)
    axs[0,0].set_xlim([0, 10])
    axs[0,0].set_ylim([0, 10])
    
    xedges, yedges = np.linspace(0, 5000, 41), np.linspace(0, 5000, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop, 
                                          fittingModelResultDf.TotalPop_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 30000] = 30000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop), fittingModelResultDf.TotalPop_pred)
    reg.coef_
    reg.intercept_
    
    axs[0,1].scatter(fittingModelResultDf.TotalPop, fittingModelResultDf.TotalPop_pred, 
                     c=c, cmap=cmap)
    axs[0,1].axline((0, 0), (5000, 5000), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[0,1].axline((0, reg.intercept_), (5000, (reg.intercept_ + 5000 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[0,1].grid(True)
    axs[0,1].legend()
    axs[0,1].text(4500, 4800, "b", fontsize=20)
    axs[0,1].set_xlabel("the Observed Male Population", fontsize=15)
    axs[0,1].set_ylabel("the Predicted Male Population", fontsize=15)
    axs[0,1].set_xlim([0, 5000])
    axs[0,1].set_ylim([0, 5000])
    
    #### total pop 
    total_pop_result_cv = pd.read_csv(result_location + "SKlearn_1000tree_MalePopLog_DF_cv_3_7.csv")
    total_pop_result_cv.G04c_001 = total_pop_result_cv.G04c_001.astype('int32')
    total_pop_result_cv.year = total_pop_result_cv.year.astype('int32')
    total_pop_result_cv = total_pop_result_cv.set_index(['G04c_001', 'year'])
    
    ##### log back
    fittingModelResultDf = total_pop_result_cv.copy()
    fittingModelResultDf = fittingModelResultDf.rename(columns={'MalePopLog':'TotalPopLog'})
    fittingModelResultDf['TotalPop_count'] = np.exp(fittingModelResultDf['TotalPopLog']) - 1
    fittingModelResultDf['TotalPop_countpred'] = np.exp(fittingModelResultDf['y_pred']) - 1
    
    xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPopLog, 
                                          fittingModelResultDf.y_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPopLog, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.y_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 5000] = 5000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPopLog), fittingModelResultDf.y_pred)
    reg.coef_
    reg.intercept_
    
    axs[1,0].scatter(fittingModelResultDf.TotalPopLog, fittingModelResultDf.y_pred, 
                     c=c, cmap=cmap)
    axs[1,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[1,0].axline((0, reg.intercept_), (10, (reg.intercept_ + 10 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[1,0].grid(True)
    axs[1,0].legend()
    axs[1,0].text(9, 9.7, "c", fontsize=20)
    axs[1,0].set_xlabel("Logarithm of the Observed Male Population", fontsize=15)
    axs[1,0].set_ylabel("Logarithm of the Predicted Male Population", fontsize=15)
    axs[1,0].set_xlim([0, 10])
    axs[1,0].set_ylim([0, 10])
    
    xedges, yedges = np.linspace(0, 11000, 41), np.linspace(0, 11000, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop_count, 
                                          fittingModelResultDf.TotalPop_countpred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_count, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_countpred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 5000] = 5000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop_count), fittingModelResultDf.TotalPop_countpred)
    reg.coef_
    reg.intercept_
    
    axs[1,1].scatter(fittingModelResultDf.TotalPop_count, fittingModelResultDf.TotalPop_countpred, 
                     c=c, cmap=cmap)
    axs[1,1].axline((0, 0), (5000, 5000), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[1,1].axline((0, reg.intercept_), (5000, (reg.intercept_ + 5000 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[1,1].grid(True)
    axs[1,1].legend()
    axs[1,1].text(4500, 4800, "d", fontsize=20)
    axs[1,1].set_xlabel("the Observed Male Population", fontsize=15)
    axs[1,1].set_ylabel("the Predicted Male Population", fontsize=15)
    axs[1,1].set_xlim([0, 5000])
    axs[1,1].set_ylim([0, 5000])
    
    norm = mpl.colors.Normalize(vmin=0, vmax=30000)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        cax=axs[2,0], orientation='horizontal')
    cbar.set_label('Density',size=24)
    cbar.ax.tick_params(labelsize=18) 
    
    norm = mpl.colors.Normalize(vmin=0, vmax=5000)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        cax=axs[2,1], orientation='horizontal')
    cbar.set_label('Density',size=24)
    cbar.ax.tick_params(labelsize=18) 
    #plt.show();
    
    fig.savefig(figure_location + "fittingModel_male.jpg")

def drawFemalePop(result_location, figure_location, realPopDf_Y):
    total_pop_result = pd.read_csv(result_location + "SKlearn_1000tree_female_pop_log.csv")
    total_pop_result.G04c_001 = total_pop_result.G04c_001.astype('int32')
    total_pop_result.year = total_pop_result.year.astype('int32')
    total_pop_result = total_pop_result.set_index(['G04c_001', 'year'])
    total_pop_result = total_pop_result.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    realPopDf_Y = realPopDf_Y.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    
    ##### log back
    fittingModelResultDf = pd.concat([realPopDf_Y, total_pop_result], axis = 1, join='outer')
    fittingModelResultDf = fittingModelResultDf.dropna(subset = 'bigy_pred')
    fittingModelResultDf = fittingModelResultDf.fillna(0)
    fittingModelResultDf['TotalPop_log'] = np.log(fittingModelResultDf['FemalePop'] + 1)
    ################################################ Revise here is enough ^^^^
    fittingModelResultDf = fittingModelResultDf.rename(columns={'bigy_pred':'TotalPop_log_pred'})
    fittingModelResultDf['TotalPop_pred'] = np.exp(fittingModelResultDf['TotalPop_log_pred']) - 1
    fittingModelResultDf = fittingModelResultDf[['FemalePop', 'TotalPop_log_pred',
                                                 'TotalPop_log', 'TotalPop_pred']]
    fittingModelResultDf = fittingModelResultDf.rename(columns={'FemalePop':'TotalPop'})
    
    # figure total fitting model
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(20, 21), dpi=1000,
                            gridspec_kw={'height_ratios': [10, 10, 1]})
    
    xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop_log, 
                                          fittingModelResultDf.TotalPop_log_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_log_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 30000] = 30000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop_log), fittingModelResultDf.TotalPop_log_pred)
    reg.coef_
    reg.intercept_
    
    axs[0,0].scatter(fittingModelResultDf.TotalPop_log, fittingModelResultDf.TotalPop_log_pred, 
                     c=c, cmap=cmap)
    axs[0,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[0,0].axline((0, reg.intercept_), (10, (reg.intercept_ + 10 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[0,0].grid(True)
    axs[0,0].legend()
    axs[0,0].text(9, 9.7, "a", fontsize=20)
    axs[0,0].set_xlabel("Logarithm of the Observed Female Population", fontsize=15)
    axs[0,0].set_ylabel("Logarithm of the Predicted Female Population", fontsize=15)
    axs[0,0].set_xlim([0, 10])
    axs[0,0].set_ylim([0, 10])
    
    xedges, yedges = np.linspace(0, 5000, 41), np.linspace(0, 5000, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop, 
                                          fittingModelResultDf.TotalPop_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 30000] = 30000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop), fittingModelResultDf.TotalPop_pred)
    reg.coef_
    reg.intercept_
    
    axs[0,1].scatter(fittingModelResultDf.TotalPop, fittingModelResultDf.TotalPop_pred, 
                     c=c, cmap=cmap)
    axs[0,1].axline((0, 0), (5000, 5000), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[0,1].axline((0, reg.intercept_), (5000, (reg.intercept_ + 5000 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[0,1].grid(True)
    axs[0,1].legend()
    axs[0,1].text(4500, 4800, "b", fontsize=20)
    axs[0,1].set_xlabel("the Observed Female Population", fontsize=15)
    axs[0,1].set_ylabel("the Predicted Female Population", fontsize=15)
    axs[0,1].set_xlim([0, 5000])
    axs[0,1].set_ylim([0, 5000])
    
    #### total pop 
    total_pop_result_cv = pd.read_csv(result_location + "SKlearn_1000tree_FemalePopLog_DF_cv_3_7.csv")
    total_pop_result_cv.G04c_001 = total_pop_result_cv.G04c_001.astype('int32')
    total_pop_result_cv.year = total_pop_result_cv.year.astype('int32')
    total_pop_result_cv = total_pop_result_cv.set_index(['G04c_001', 'year'])
    
    ##### log back
    fittingModelResultDf = total_pop_result_cv.copy()
    fittingModelResultDf = fittingModelResultDf.rename(columns={'FemalePopLog':'TotalPopLog'})
    fittingModelResultDf['TotalPop_count'] = np.exp(fittingModelResultDf['TotalPopLog']) - 1
    fittingModelResultDf['TotalPop_countpred'] = np.exp(fittingModelResultDf['y_pred']) - 1
    
    xedges, yedges = np.linspace(0, 10, 41), np.linspace(0, 10, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPopLog, 
                                          fittingModelResultDf.y_pred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPopLog, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.y_pred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 5000] = 5000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPopLog), fittingModelResultDf.y_pred)
    reg.coef_
    reg.intercept_
    
    axs[1,0].scatter(fittingModelResultDf.TotalPopLog, fittingModelResultDf.y_pred, 
                     c=c, cmap=cmap)
    axs[1,0].axline((0, 0), (10, 10), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[1,0].axline((0, reg.intercept_), (10, (reg.intercept_ + 10 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[1,0].grid(True)
    axs[1,0].legend()
    axs[1,0].text(9, 9.7, "c", fontsize=20)
    axs[1,0].set_xlabel("Logarithm of the Observed Female Population", fontsize=15)
    axs[1,0].set_ylabel("Logarithm of the Predicted Female Population", fontsize=15)
    axs[1,0].set_xlim([0, 10])
    axs[1,0].set_ylim([0, 10])
    
    xedges, yedges = np.linspace(0, 11000, 41), np.linspace(0, 11000, 41)
    hist, xedges, yedges = np.histogram2d(fittingModelResultDf.TotalPop_count, 
                                          fittingModelResultDf.TotalPop_countpred, 
                                          (xedges, yedges))
    
    xidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_count, xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(fittingModelResultDf.TotalPop_countpred, yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    c[c > 5000] = 5000
    
    reg = LinearRegression().fit(pd.DataFrame(fittingModelResultDf.TotalPop_count), fittingModelResultDf.TotalPop_countpred)
    reg.coef_
    reg.intercept_
    
    axs[1,1].scatter(fittingModelResultDf.TotalPop_count, fittingModelResultDf.TotalPop_countpred, 
                     c=c, cmap=cmap)
    axs[1,1].axline((0, 0), (5000, 5000), linewidth=6, color='r', alpha=0.4, linestyle='--',
                    label='y = x')
    axs[1,1].axline((0, reg.intercept_), (5000, (reg.intercept_ + 5000 * reg.coef_[0])), 
                    linewidth=6, color='blue', alpha=0.4, linestyle='--',
                    label='y = ' + str(round(reg.coef_[0], 2))+"x + " + str(round(reg.intercept_, 2)))
    axs[1,1].grid(True)
    axs[1,1].legend()
    axs[1,1].text(4500, 4800, "d", fontsize=20)
    axs[1,1].set_xlabel("the Observed Female Population", fontsize=15)
    axs[1,1].set_ylabel("the Predicted Female Population", fontsize=15)
    axs[1,1].set_xlim([0, 5000])
    axs[1,1].set_ylim([0, 5000])
    
    norm = mpl.colors.Normalize(vmin=0, vmax=30000)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        cax=axs[2,0], orientation='horizontal')
    cbar.set_label('Density',size=24)
    cbar.ax.tick_params(labelsize=18) 
    
    norm = mpl.colors.Normalize(vmin=0, vmax=5000)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        cax=axs[2,1], orientation='horizontal')
    cbar.set_label('Density',size=24)
    cbar.ax.tick_params(labelsize=18) 
    #plt.show();
    
    fig.savefig(figure_location + "fittingModel_female.jpg")


### run
drawTotalPop(result_location, figure_location, realPopDf_Y)
drawMalePop(result_location, figure_location, realPopDf_Y)
drawFemalePop(result_location, figure_location, realPopDf_Y)
