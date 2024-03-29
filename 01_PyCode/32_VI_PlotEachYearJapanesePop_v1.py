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
import matplotlib.pyplot as plt
import matplotlib.colors
from joblib import Parallel, delayed

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green","yellow","red"])


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

def plotPop(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    meshGDF.plot(column='X' + year, ax=ax, legend=True, cmap=cmap, vmax = 1000, vmin = 0)
    plt.title("Japan Population Distribution in "+ year, loc = "left")
    plt.grid(True)
    plt.xlim(125, 150)
    plt.ylim(25,48)
    plt.show();

    fig.savefig(figure_location + "y"+ year +".jpg")

Parallel(n_jobs=7)(delayed(plotPop)(year, japan_perfecture, meshGDF, cmap) for year in np.linspace(2001, 2020, 20))


total_pop_predict_log_wider = total_pop_predict.drop(columns='total_pop').copy()
total_pop_predict_log_wider = total_pop_predict_log_wider.pivot(index='G04c_001', 
                                                        columns='year',
                                                        values="bigy_pred")

#meshGDF = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPolyMesh500m.shp")
#meshGDF.G04c_001.dtype
#meshGDF.G04c_001 = meshGDF.G04c_001.astype('int64')
#meshGDF = meshGDF.set_index("G04c_001")

#meshGDF = pd.concat([meshGDF, total_pop_predict_log_wider], axis=1)
#meshGDF = meshGDF.set_crs(epsg = 4326)
total_pop_predict_log_wider.columns = ["X2001_log","X2002_log",'X2003_log',
                                       'X2004_log','X2005_log','X2006_log',
                                       'X2007_log','X2008_log','X2009_log',
                                       'X2010_log','X2011_log','X2012_log',
                                       'X2013_log','X2014_log','X2015_log',
                                       'X2016_log','X2017_log','X2018_log',
                                       'X2019_log','X2020_log']
meshGDF = pd.concat([meshGDF, total_pop_predict_log_wider], axis=1)

def plotPopLog(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    meshGDF.plot(column='X' + year + "_log", ax=ax, legend=True, cmap=cmap, vmax = 9.5, vmin = 0)
    plt.title("Japan Population Distribution (Logarithm) in "+ year, loc = "left")
    plt.grid(True)
    plt.xlim(125, 150)
    plt.ylim(25,48)
    plt.show();

    fig.savefig(figure_location + "y"+ year +"_log.jpg")


Parallel(n_jobs=7)(delayed(plotPopLog)(year, japan_perfecture, meshGDF, cmap) for year in np.linspace(2001, 2020, 20))

### male
male_pop_predict = pd.read_csv(result_folder + "SKlearn_1000tree_male_pop_log.csv")
male_pop_predict.head()
male_pop_predict["G04c_001"] = male_pop_predict["G04c_001"].astype("int64")
male_pop_predict['male_pop'] = np.exp(male_pop_predict['bigy_pred']) - 1
male_pop_predict = male_pop_predict.rename(columns={'bigy_pred':'male_bigy_pred'})

male_pop_predict_wider = male_pop_predict.drop(columns="male_bigy_pred").copy()
male_pop_predict_wider = male_pop_predict_wider.pivot(index='G04c_001', 
                                                        columns='year',
                                                        values='male_pop')
male_pop_predict_wider.columns =  ["X2001_male","X2002_male",'X2003_male',
                                       'X2004_male','X2005_male','X2006_male',
                                       'X2007_male','X2008_male','X2009_male',
                                       'X2010_male','X2011_male','X2012_male',
                                       'X2013_male','X2014_male','X2015_male',
                                       'X2016_male','X2017_male','X2018_male',
                                       'X2019_male','X2020_male']
meshGDF = pd.concat([meshGDF, male_pop_predict_wider], axis=1)

def plotPopMale(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    meshGDF.plot(column='X' + year + "_male", ax=ax, legend=True, cmap=cmap, vmax = 1000, vmin = 0)
    plt.title("Japan Male Population Distribution in "+ year, loc = "left")
    plt.grid(True)
    plt.xlim(125, 150)
    plt.ylim(25,48)
    plt.show();

    fig.savefig(figure_location + "y"+ year +"_male.jpg")
    
Parallel(n_jobs=5)(delayed(plotPopMale)(year, japan_perfecture, meshGDF, cmap) for year in np.linspace(2001, 2020, 20))

male_pop_predict_log_wider = male_pop_predict.drop(columns="male_pop").copy()
male_pop_predict_log_wider = male_pop_predict_log_wider.pivot(index='G04c_001', 
                                                              columns='year',
                                                              values='male_bigy_pred')
male_pop_predict_log_wider.columns = ["X2001_male_log","X2002_male_log",'X2003_male_log',
                                       'X2004_male_log','X2005_male_log','X2006_male_log',
                                       'X2007_male_log','X2008_male_log','X2009_male_log',
                                       'X2010_male_log','X2011_male_log','X2012_male_log',
                                       'X2013_male_log','X2014_male_log','X2015_male_log',
                                       'X2016_male_log','X2017_male_log','X2018_male_log',
                                       'X2019_male_log','X2020_male_log']
meshGDF = pd.concat([meshGDF, male_pop_predict_log_wider], axis=1)
def plotPopMaleLog(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    meshGDF.plot(column='X' + year + "_male_log", ax=ax, legend=True, cmap=cmap, vmax = 9.5, vmin = 0)
    plt.title("Japan Male Population Distribution (Logarithm) in "+ year, loc = "left")
    plt.grid(True)
    plt.xlim(125, 150)
    plt.ylim(25,48)
    plt.show();

    fig.savefig(figure_location + "y"+ year +"_male_log.jpg")
    
Parallel(n_jobs=7)(delayed(plotPopMaleLog)(year, japan_perfecture, meshGDF, cmap) for year in np.linspace(2001, 2020, 20))

### female
female_pop_predict = pd.read_csv(result_folder + "SKlearn_1000tree_female_pop_log.csv")
female_pop_predict.head()
female_pop_predict["G04c_001"] = female_pop_predict["G04c_001"].astype("int64")
female_pop_predict['female_pop'] = np.exp(female_pop_predict['bigy_pred']) - 1
female_pop_predict = female_pop_predict.rename(columns={'bigy_pred':'female_bigy_pred'})

female_pop_predict_wider = female_pop_predict.drop(columns="female_bigy_pred").copy()
female_pop_predict_wider = female_pop_predict_wider.pivot(index='G04c_001', 
                                                        columns='year',
                                                        values='female_pop')
female_pop_predict_wider.columns =  ["X2001_female","X2002_female",'X2003_female',
                                     'X2004_female','X2005_female','X2006_female',
                                     'X2007_female','X2008_female','X2009_female',
                                     'X2010_female','X2011_female','X2012_female',
                                     'X2013_female','X2014_female','X2015_female',
                                     'X2016_female','X2017_female','X2018_female',
                                     'X2019_female','X2020_female']
meshGDF = pd.concat([meshGDF, female_pop_predict_wider], axis=1)

def plotPopFemale(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    meshGDF.plot(column='X' + year + "_female", ax=ax, legend=True, cmap=cmap, vmax = 1000, vmin = 0)
    plt.title("Japan Female Population Distribution in "+ year, loc = "left")
    plt.grid(True)
    plt.xlim(125, 150)
    plt.ylim(25,48)
    plt.show();

    fig.savefig(figure_location + "y"+ year +"_female.jpg")
    
Parallel(n_jobs=5)(delayed(plotPopFemale)(year, japan_perfecture, meshGDF, cmap) for year in np.linspace(2001, 2020, 20))

female_pop_predict_log_wider = female_pop_predict.drop(columns="female_pop").copy()
female_pop_predict_log_wider = female_pop_predict_log_wider.pivot(index='G04c_001', 
                                                              columns='year',
                                                              values='female_bigy_pred')
female_pop_predict_log_wider.columns = ["X2001_female_log","X2002_female_log",'X2003_female_log',
                                       'X2004_female_log','X2005_female_log','X2006_female_log',
                                       'X2007_female_log','X2008_female_log','X2009_female_log',
                                       'X2010_female_log','X2011_female_log','X2012_female_log',
                                       'X2013_female_log','X2014_female_log','X2015_female_log',
                                       'X2016_female_log','X2017_female_log','X2018_female_log',
                                       'X2019_female_log','X2020_female_log']
meshGDF = pd.concat([meshGDF, female_pop_predict_log_wider], axis=1)
def plotPopFemaleLog(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    meshGDF.plot(column='X' + year + "_female_log", ax=ax, legend=True, cmap=cmap, vmax = 9.5, vmin = 0)
    plt.title("Japan Female Population Distribution (Logarithm) in "+ year, loc = "left")
    plt.grid(True)
    plt.xlim(125, 150)
    plt.ylim(25,48)
    plt.show();

    fig.savefig(figure_location + "y"+ year +"_female_log.jpg")
    
Parallel(n_jobs=5)(delayed(plotPopFemaleLog)(year, japan_perfecture, meshGDF, cmap) for year in np.linspace(2001, 2020, 20))

meshGDF = meshGDF.rename(columns={'G04c_001':"meshID"})
meshGDF.to_file(result_folder + "GDF_2001_2020_500mesh_total_male_female.v1.shp")


# For Prof Managi
"""
def plotPopLog(year, japan_perfecture, meshGDF, cmap):
    year = str(int(year))
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    japan_perfecture2.boundary.plot(ax=ax, edgecolor='red', alpha = 0.5, 
                                    linewidth=2, linestyle = '--')
    japan_perfecture.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.6)
    meshGDF.plot(column='X' + year + "_log", ax=ax, legend=True, cmap=cmap, vmax = 9.5, vmin = 0)
    plt.title("Japan Population Distribution (Logarithm) in "+ year, loc = "left")
    plt.grid(True)
    plt.xlim(130, 131)
    plt.ylim(33,34)
    plt.show();

    fig.savefig(figure_location + "y"+ year +"_log_ForPSM.jpg")
    
plotPopLog(2019, japan_perfecture, meshGDF, cmap)
"""