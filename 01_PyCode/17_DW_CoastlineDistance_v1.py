# -*- coding: utf-8 -*-
"""
Source: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-C23.html

Created on Mon Apr 25 10:36:30 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

coastlineShapeFile = gpd.read_file("F:/17_Article/01_Data/13_CoastLine/MergedCoastline.shp")

coastlineShapeFileDissolved = coastlineShapeFile.dissolve()
coastlineShapeFileDissolved = coastlineShapeFileDissolved.set_crs(epsg = 4326)

coords_extration_dist = gpd.sjoin_nearest(coords_extration, coastlineShapeFileDissolved, distance_col="distances")
    
coords_extration["coast_dist"] = valueArray