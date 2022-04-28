# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 15:48:06 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import glob
import pandas as pd
import math
import numpy as np

### mesh
mesh_location = "F:\\17_Article\\01_Data\\00_mesh\\mesh_center_point.shp"
gdf_mesh = gpd.read_file(mesh_location)
gdf_mesh = gdf_mesh[['x', 'y','id']]
gdf_mesh.id = gdf_mesh.id.astype('int')

### gdf_popMesh
aimFolder = "F:\\17_Article\\01_Data\\09_populationMesh\\2015Mesh"

fileList = glob.glob(aimFolder + "\\*.shp")

gdf_popMesh = gpd.read_file(fileList[0])
gdf_popMesh = gdf_popMesh[['MESH_ID', 'PTN_2015']]
gdf_popMesh = gdf_popMesh.rename(columns = {'MESH_ID':'id'})

gdf_mesh = pd.merge(gdf_mesh, gdf_popMesh, on = "id", how = 'left')
gdf_mesh.PTN_2015 = gdf_mesh.PTN_2015.fillna(0)
gdf_mesh['PTN_2015_log'] = np.log(gdf_mesh.PTN_2015 + 1) 

### Other data folder
otherDataFolder = "F:\\17_Article\\01_Data\\99_MiddleFileStation\\"
### land cover
gdf_landCover = pd.read_pickle(otherDataFolder+"05_roadDensity.pkl")
