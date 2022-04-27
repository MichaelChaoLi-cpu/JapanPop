# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:24:56 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import pandas as pd

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

highDensityShapeFile = gpd.read_file("F:/17_Article/01_Data/06_HighDensityPopulation/A16-15_GML/A16-15_00_DID.shp")
highDensityShapeFile = highDensityShapeFile.set_crs(epsg = 4326)
highDensityShapeFile = highDensityShapeFile[['geometry']]
highDensityShapeFileRepair = highDensityShapeFile.buffer(0)
highDensityShapeFile = gpd.GeoDataFrame(geometry = highDensityShapeFileRepair, crs="EPSG:4326")
highDensityShapeFileDissolved = highDensityShapeFile.dissolve()
highDensityShapeFileDissolved['within'] = 1

joinShape = coords_extration.sjoin(highDensityShapeFileDissolved)
joinDistance = coords_extraction.sjoin_nearest(highDensityShapeFileDissolved, distance_col = "dist")
joinDistance = joinDistance.drop(columns = ["within"]) 

joinShape = joinShape[["id", "within"]]

result = pd.merge(joinDistance, joinShape, on='id', how='left')
result['within'] = result['within'].fillna(0)
result = result.drop(columns = ["index_right"]) 

result.loc[result['within'] == 1, 'dist'] = 0
result.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/07_PopulationDensityClass.pkl")
