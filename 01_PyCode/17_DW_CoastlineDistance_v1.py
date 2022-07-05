# -*- coding: utf-8 -*-
"""
Source: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-C23.html

year: 2006

Created on Mon Apr 25 10:36:30 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import pandas as pd

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")

coastlineShapeFile = gpd.read_file("F:/17_Article/01_Data/13_CoastLine/MergedCoastline.shp")

coastlineShapeFileDissolved = coastlineShapeFile.dissolve()
coastlineShapeFileDissolved = coastlineShapeFileDissolved.set_crs(epsg = 4326)

coords_extration_dist = gpd.sjoin_nearest(coords_extration, coastlineShapeFileDissolved, distance_col="dist_coast")
coords_extration_result = pd.DataFrame(coords_extration_dist[['G04c_001', 'dist_coast']])
coords_extration_result['year'] = 2010
   
coords_extration_result.to_pickle("F:/17_Article/01_Data/98_20yearPickles/06_CoastLine.pkl")
