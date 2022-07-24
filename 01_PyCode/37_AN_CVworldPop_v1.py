# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 14:05:30 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")

raster2005 = "F:\\17_Article\\01_Data\\97_WorldPopCV\\01_WorldPopUNadj\\jpn_pd_2005_1km_UNadj.tif"
raster2010 = "F:\\17_Article\\01_Data\\97_WorldPopCV\\01_WorldPopUNadj\\jpn_pd_2010_1km_UNadj.tif"
raster2015 = "F:\\17_Article\\01_Data\\97_WorldPopCV\\01_WorldPopUNadj\\jpn_pd_2015_1km_UNadj.tif"

def extractValue(rasterLocation, coords_extration):
    rasterFile = rasterio.open(rasterLocation)
    rasterArray = rasterFile.read(1)
        
    valueArray = []
    for point in coords_extration['geometry']:
        x = point.xy[0][0]
        y = point.xy[1][0]
        try:
            row, col = rasterFile.index(x, y)
            valueArray.append(rasterArray[row, col])
        except:
            valueArray.append(np.nan)
            
    valueArray = np.array(valueArray)
    return valueArray

value2005 = extractValue(raster2005, coords_extration)
value2010 = extractValue(raster2010, coords_extration)
value2015 = extractValue(raster2015, coords_extration)

coords_extration['WorldPop_2005'] = value2005
coords_extration['WorldPop_2010'] = value2010
coords_extration['WorldPop_2015'] = value2015

coords_extration['WorldPop_2005'] = coords_extration['WorldPop_2005'].replace(-99999.0, np.nan)
coords_extration['WorldPop_2010'] = coords_extration['WorldPop_2010'].replace(-99999.0, np.nan)
coords_extration['WorldPop_2015'] = coords_extration['WorldPop_2015'].replace(-99999.0, np.nan)

polyMesh = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPolyMesh500m.shp")
polyMesh = polyMesh.set_crs(4326)
polyMesh = polyMesh.to_crs(3095)
polyMesh['area'] =  polyMesh.geometry.area
polyMesh['area'] = polyMesh['area']/1000000
polyArea = pd.DataFrame(polyMesh.drop(columns=['geometry'])).copy()

worldPopDataset = pd.concat(
    [pd.DataFrame(coords_extration.drop(columns=['geometry', 'G04c_001'])).copy(),
     polyArea], axis=1)

worldPopDataset['2005'] = worldPopDataset['WorldPop_2005']*worldPopDataset['area']
worldPopDataset['2010'] = worldPopDataset['WorldPop_2010']*worldPopDataset['area']
worldPopDataset['2015'] = worldPopDataset['WorldPop_2015']*worldPopDataset['area']

worldPopDataset = worldPopDataset[['G04c_001', '2005', '2010', '2015']]
worldPopDataset = pd.melt(worldPopDataset, id_vars='G04c_001',
                          value_vars=['2005', '2010', '2015'])
worldPopDataset.columns = ['G04c_001', 'year', 'WorldPopCount']
worldPopDataset.G04c_001 = worldPopDataset.G04c_001.astype('int32')
worldPopDataset.year = worldPopDataset.year.astype('int32')
worldPopDataset = worldPopDataset.set_index(['G04c_001', 'year'])
worldPopDataset.to_pickle("F:\\17_Article\\01_Data\\97_WorldPopCV\\01_worldPop.pkl")

single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
##### y
realPopDf_Y = pd.read_pickle(single_dataset_location + "03_population.pkl")

##### cv test
testDf = pd.concat([realPopDf_Y, worldPopDataset], axis = 1)
testDf = testDf.dropna()

r2 = r2_score(testDf.TotalPop, testDf.WorldPopCount)
print(r2)
mae = mean_absolute_error(testDf.TotalPop, testDf.WorldPopCount)
print(mae)
mse = mean_squared_error(testDf.TotalPop, testDf.WorldPopCount)
rmse = np.sqrt(mse)
print(rmse)
reg = LinearRegression().fit(pd.DataFrame(testDf.TotalPop), np.array(testDf.WorldPopCount))
print(reg.coef_)
print(reg.intercept_)

