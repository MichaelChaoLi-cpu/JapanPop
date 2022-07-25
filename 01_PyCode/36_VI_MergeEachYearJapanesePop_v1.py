# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 14:50:10 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors
from joblib import Parallel, delayed
import matplotlib as mpl

def drawFigure(outputVariable):
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green","yellow","red"])
    
    
    result_folder = "F:\\17_Article\\04_Result\\"
    
    meshGDF = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPolyMesh500m.shp")
    meshGDF.G04c_001.dtype
    meshGDF.G04c_001 = meshGDF.G04c_001.astype('int64')
    meshGDF = meshGDF.set_index("G04c_001")
    
    japan_perfecture = gpd.read_file("F:/17_Article/01_Data/00_mesh/gadm40_JPN_1.shp")
    figure_location = "C:\\Users\\li.chao.987@s.kyushu-u.ac.jp\\OneDrive - Kyushu University\\17_Article\\03_RStudio\\05_Figure\\"
    
    total_pop_predict = pd.read_csv(result_folder + "SKlearn_1000tree_"+outputVariable+"_pop_log.csv")
    total_pop_predict.head()
    total_pop_predict_log_wider = total_pop_predict.pivot(index='G04c_001', 
                                                          columns='year',
                                                          values="bigy_pred")
    
    total_pop_predict_log_wider.columns = ["X2001_log","X2002_log",'X2003_log',
                                           'X2004_log','X2005_log','X2006_log',
                                           'X2007_log','X2008_log','X2009_log',
                                           'X2010_log','X2011_log','X2012_log',
                                           'X2013_log','X2014_log','X2015_log',
                                           'X2016_log','X2017_log','X2018_log',
                                           'X2019_log','X2020_log']
    meshGDF = pd.concat([meshGDF, total_pop_predict_log_wider], axis=1)
    
    # figure
    fig, axs = plt.subplots(nrows=6, ncols=4, constrained_layout = True,
                            figsize=(40, 52), dpi=300, 
                            gridspec_kw={'height_ratios': [10, 10, 10, 10, 10, 2]})
    ax_legend = fig.add_axes([0.1, 0.025, 0.8, 0.005])
    ax_list = [axs[0, 0], axs[0, 1], axs[0, 2], axs[0, 3],
               axs[1, 0], axs[1, 1], axs[1, 2], axs[1, 3],
               axs[2, 0], axs[2, 1], axs[2, 2], axs[2, 3],
               axs[3, 0], axs[3, 1], axs[3, 2], axs[3, 3],
               axs[4, 0], axs[4, 1], axs[4, 2], axs[4, 3]]
    xlabel = ['125', '130', '135', '140', '145', '150']
    ylabel = ['25', '30', '35', '40', '45']
    
    i = 0
    while i < 20:
        ax = ax_list[i]
        year = str(2001 + i)
        japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
        meshGDF.plot(column='X' + year + "_log", ax=ax, legend=False, cmap=cmap, vmax = 9.5, vmin = 0)
        ax.set_title(year, loc = "left", fontsize=24)
        ax.grid(True)
        ax.set_xlim([125, 150])
        ax.set_ylim([25,48])
        ax.set_xticklabels(xlabel, fontsize=18)
        ax.set_yticklabels(ylabel, fontsize=18)
        
        i = i + 1
        
    axs[5, 0].axis('off')
    axs[5, 1].axis('off')
    axs[5, 2].axis('off')
    axs[5, 3].axis('off')
    #plt.show();
    norm = mpl.colors.Normalize(vmin=0, vmax=9.5)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        cax=ax_legend, orientation='horizontal')
    cbar.set_label('Japan '+outputVariable.capitalize()+' Population Distribution',size=36)
    cbar.ax.tick_params(labelsize=30) 
    
    fig.savefig(figure_location + "merged_"+outputVariable+"_log.jpg")
    
drawFigure('male')
drawFigure('female')