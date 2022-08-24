# -*- coding: utf-8 -*-
"""
From this script the code will be from 01 again.

This folder might become a new project

We take Tokyo as an example.

#### Note: now we do not have enough calculation power.

Created on Fri Aug 19 09:44:57 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import geopandas as gpd
import pandas as pd

def getPointWithinTokyo():
    """
    This function gets a dataframe with G04c_001 and inTokyo
    """
    coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")
    prefecture = gpd.read_file(r"C:\Users\li.chao.987@s.kyushu-u.ac.jp\OneDrive - Kyushu University\17_Article\03_RStudio\09_DataAdvanceProject\01_JapanPerfectureBoundaryOCHA\jpn_admbnda_adm1_2019.shp")
    
    Tokyo = prefecture.query("ADM1_PCODE == 'JP13'")
    Tokyo = Tokyo[['ADM1_PCODE', 'geometry']]
    prefecture = None
    
    pointWithinTokyo = coords_extration.set_crs(epsg = 4326).sjoin(Tokyo.to_crs(epsg = 4326))
    coords_extration = None
    pointWithinTokyo = pointWithinTokyo[['G04c_001']]
    pointWithinTokyo['inTokyo'] = 1
    pointWithinTokyo[['G04c_001']] = pointWithinTokyo[['G04c_001']].astype("int32")
    return pointWithinTokyo

def getBigXTokyo(pointWithinTokyo):
    """
    This function is get tokyo bigX

    Parameters
    ----------
    pointWithinTokyo : dataframe
        from getPointWithinTokyo()

    Returns
    -------
    bigX_Tokyo : dataframe
        bigX data in tokyo.

    """
    single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
    bigX = pd.read_csv(single_dataset_location + "99_mergedDataset.csv")
    bigX.G04c_001 = bigX.G04c_001.astype("int32")
    bigX.year = bigX.year.astype("int32")
    bigX_Tokyo = bigX.merge(pointWithinTokyo, how = 'inner', on = "G04c_001")
    
    pointLonLatAll = pd.read_csv(single_dataset_location + "98_pointLonLatALL.csv")
    pointLonLatAll.G04c_001 = pointLonLatAll.G04c_001.astype("int32")
    pointLonLatAll.year = pointLonLatAll.year.astype("int32")
    bigX_Tokyo = bigX_Tokyo.merge(pointLonLatAll, how = 'inner', 
                                  on = ["G04c_001", "year"])
    return bigX_Tokyo

def getBigyTokyo(pointWithinTokyo, aimGroup):
    """
    This is to extract tokyo y value of one group (total, male, female)

    Parameters
    ----------
    pointWithinTokyo : dataframe
        from getPointWithinTokyo()
    aimGroup : str
        total, male, female

    Returns
    -------
    bigy_pred_Tokyo : dataframe
        bigy data in tokyo.

    """
    result_location = "F:/17_Article/04_Result/"
    bigy_pred = pd.read_csv(result_location + "SKlearn_1000tree_" + aimGroup + "_pop_log.csv")
    bigy_pred.G04c_001 = bigy_pred.G04c_001.astype("int32")
    bigy_pred.year = bigy_pred.year.astype("int32")
    bigy_pred_Tokyo = bigy_pred.merge(pointWithinTokyo, how = 'inner', on = "G04c_001")
    return  bigy_pred_Tokyo

def standardXandy(bigX_Tokyo, bigy_Tokyo):
    bigX_Tokyo = bigX_Tokyo.set_index(['G04c_001', 'year'])
    bigy_Tokyo = bigy_Tokyo.set_index(['G04c_001', 'year'])
    bigX_Tokyo = bigX_Tokyo.drop(columns='inTokyo')
    bigy_Tokyo = bigy_Tokyo.drop(columns='inTokyo')
    merged_df = pd.concat([bigy_Tokyo, bigX_Tokyo], axis=1)
    y = merged_df.iloc[:, 0:1]
    X = merged_df.iloc[:, 1:merged_df.shape[1]]
    return X, y

pointWithinTokyo = getPointWithinTokyo()
bigX_Tokyo = getBigXTokyo(pointWithinTokyo)
bigy_Tokyo = getBigyTokyo(pointWithinTokyo, 'total')
X, y = standardXandy(bigX_Tokyo, bigy_Tokyo)

data_location = "F:/17_Article/09_DataAdvanceProject/02_TokyoData/"
X.to_csv(data_location + "01_Xtokyo.csv")
y.to_csv(data_location + "02_ytokyo.csv")