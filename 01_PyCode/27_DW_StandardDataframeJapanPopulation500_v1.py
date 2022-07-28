# -*- coding: utf-8 -*-
"""
merge population table

Created on Fri Jul  1 14:48:56 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import glob
import pandas as pd
import numpy as np
import os
import zipfile

aimFolder = "F:\\17_Article\\01_Data\\09_populationMesh\\500m"


def mergeTableToStandardDF(year, aimFolder):
    fileList = glob.glob(aimFolder + "\\" + str(year) + "\\*.zip")
    os.mkdir(aimFolder + "\\" + str(year) + "\\temp")
    for filename in fileList:
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(aimFolder + "\\" + str(year) + "\\temp")
    
    txtFileList = glob.glob(aimFolder + "\\" + str(year) + "\\temp" + "\\*.txt")
    
    df_output = pd.DataFrame()
    for txtFile in txtFileList:
        df = pd.read_csv(txtFile, encoding="cp932", skiprows=(1))
        df.columns = ['G04c_001', 'TotalPop', 'MalePop', 'FemalePop', 'Family']
        df['year'] = int(year)
        df = df.set_index(['G04c_001', 'year'])
        df_output = pd.concat([df_output, df], axis=0)
        
    for root, dirs, files in os.walk(aimFolder + "\\" + str(year) + "\\temp", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(aimFolder + "\\" + str(year) + "\\temp")
    return df_output

df_2000 = mergeTableToStandardDF(2000, aimFolder)
df_2005 = mergeTableToStandardDF(2005, aimFolder)
df_2010 = mergeTableToStandardDF(2010, aimFolder)

def mergeTableToStandardDF2015(year, aimFolder):
    fileList = glob.glob(aimFolder + "\\" + str(year) + "\\*.zip")
    os.mkdir(aimFolder + "\\" + str(year) + "\\temp")
    for filename in fileList:
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(aimFolder + "\\" + str(year) + "\\temp")
    
    txtFileList = glob.glob(aimFolder + "\\" + str(year) + "\\temp" + "\\*.txt")
    
    df_output = pd.DataFrame()
    for txtFile in txtFileList:
        df = pd.read_csv(txtFile, encoding="cp932", skiprows=(1))
        df = df.iloc[:,[0,4,5,6,28]]
        df.columns = ['G04c_001', 'TotalPop', 'MalePop', 'FemalePop', 'Family']
        df['year'] = int(year)
        df = df.set_index(['G04c_001', 'year'])
        df_output = pd.concat([df_output, df], axis=0)
        
    for root, dirs, files in os.walk(aimFolder + "\\" + str(year) + "\\temp", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(aimFolder + "\\" + str(year) + "\\temp")
    return df_output

df_2015 = mergeTableToStandardDF2015(2015, aimFolder)

def mergeTableToStandardDF2020(year, aimFolder):
    fileList = glob.glob(aimFolder + "\\" + str(year) + "\\*.zip")
    os.mkdir(aimFolder + "\\" + str(year) + "\\temp")
    for filename in fileList:
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(aimFolder + "\\" + str(year) + "\\temp")
    
    txtFileList = glob.glob(aimFolder + "\\" + str(year) + "\\temp" + "\\*.txt")
    
    df_output = pd.DataFrame()
    for txtFile in txtFileList:
        df = pd.read_csv(txtFile, encoding="cp932", skiprows=(1))
        df = df.iloc[:,[0,4,5,6,37]]
        df.columns = ['G04c_001', 'TotalPop', 'MalePop', 'FemalePop', 'Family']
        df['year'] = int(year)
        df = df.set_index(['G04c_001', 'year'])
        df_output = pd.concat([df_output, df], axis=0)
        
    for root, dirs, files in os.walk(aimFolder + "\\" + str(year) + "\\temp", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(aimFolder + "\\" + str(year) + "\\temp")
    return df_output

df_2020 = mergeTableToStandardDF2020(2020, aimFolder)

popDf = pd.read_pickle("F:/17_Article/01_Data/98_20yearPickles/03_population.pkl")
popDf = pd.concat([popDf, df_2020], axis=0)

#popDf = pd.concat([df_2000, df_2005, df_2010, df_2015], axis=0)
popDf.to_pickle("F:/17_Article/01_Data/98_20yearPickles/03_population.pkl")

#aimFolder = "F:\\17_Article\\01_Data\\09_populationMesh\\250m"
#df_2015_250 = mergeTableToStandardDF2015(2015, aimFolder)
#### since the focus on high density region, it is not enough to estimate.