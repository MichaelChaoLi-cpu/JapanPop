# -*- coding: utf-8 -*-
"""
Source: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-W05.html

Created on Sun Apr 24 17:01:22 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import pandas as pd

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")

riverShapeFile = gpd.read_file("F:/17_Article/01_Data/12_River/MergedRiver.shp")

riverShapeFileDissolved = riverShapeFile.dissolve()

riverShapeFileDissolved = riverShapeFileDissolved.set_crs(epsg = 4326)

#dist = coords_extration.distance(riverShapeFileDissolved)

aimPoint = coords_extration.copy()
valueArray = []
for point in aimPoint['geometry']:
    x = point.xy[0][0]
    y = point.xy[1][0]
    xA = [x]
    yA = [y]
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(x = xA, y = yA))
    gdf = gdf.set_crs(epsg = 4326)
    dist = gdf.distance(riverShapeFileDissolved)
    valueArray.append(dist[0])
    
coords_extration["river_dist"] = valueArray

coords_extration = pd.DataFrame(coords_extration.drop(columns='geometry'))
coords_extration['year'] = 2010
coords_extration = coords_extration.rename(columns={'river_dist':'riverDist'})
coords_extration = coords_extration.set_index(['G04c_001', 'year'])

coords_extration.to_pickle("F:/17_Article/01_Data/98_20yearPickles/05_RiverDist.pkl")
