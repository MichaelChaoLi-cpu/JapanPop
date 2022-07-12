# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:10:50 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import pandas as pd
import numpy as np
import geopandas as gpd

result_folder = "F:\\17_Article\\04_Result\\"
total_pop_predict = pd.read_csv(result_folder + "SKlearn_1000tree_total_pop_log.csv")
total_pop_predict.head()
total_pop_predict['total_pop'] = np.exp(total_pop_predict['bigy_pred']) - 1

total_pop_predict_wider = total_pop_predict.drop(columns="bigy_pred").copy()
total_pop_predict_wider = total_pop_predict_wider.pivot(index='G04c_001', 
                                                        columns='year',
                                                        values='total_pop')


meshGDF = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPolyMesh500m.shp")
meshGDF.G04c_001.dtype
meshGDF.G04c_001 = meshGDF.G04c_001.astype('int64')
meshGDF = meshGDF.set_index("G04c_001")

meshGDF = pd.concat([meshGDF, total_pop_predict_wider], axis=1)
meshGDF = meshGDF.set_crs(epsg = 4326)
meshGDF.columns = ['geometry',"X2001","X2002",'X2003',
                   'X2004','X2005', 'X2006','X2007', 'X2008',
                   'X2009','X2010','X2011', 'X2012', 'X2013',
                   'X2014','X2015','X2016','X2017', 
                   'X2018','X2019','X2020']

japan_perfecture = gpd.read_file("F:/17_Article/01_Data/00_mesh/gadm40_JPN_1.shp")
figure_location = "C:\\Users\\li.chao.987@s.kyushu-u.ac.jp\\OneDrive - Kyushu University\\17_Article\\03_RStudio\\05_Figure\\"

import matplotlib.pyplot as plt
import matplotlib.colors

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green","yellow","red"])
def plotPop(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(11, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    meshGDF.plot(column='X' + year, ax=ax, legend=True, cmap=cmap)
    plt.title("Japan Population Distribution in 2001", loc = "left")
    plt.grid(True)
    plt.xlim(125, 150)
    plt.ylim(25,48)
    plt.show();

    fig.savefig(figure_location + "y"+ year +".jpg")
    
from joblib import Parallel, delayed

Parallel(n_jobs=5)(delayed(plotPop)(year, japan_perfecture, meshGDF, cmap) for year in np.linspace(2001, 2020, 20))
