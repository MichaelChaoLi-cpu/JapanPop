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
gdf_landCover = pd.read_pickle(otherDataFolder+"00_2015_LandCover_CLASSandDIST.pkl")
gdf_landCover = gdf_landCover.drop(columns = ['x', 'y', 'geometry'])
gdf_landCover = gdf_landCover.astype('float')
gdf_landCover.id = gdf_landCover.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_landCover, on = "id", how = 'left')
del gdf_landCover

### NPP
gdf_other = pd.read_pickle(otherDataFolder+"01_2015_NPP.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### NTL
gdf_other = pd.read_pickle(otherDataFolder+"02_2015_NTL.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### temperature
gdf_other = pd.read_pickle(otherDataFolder+"03_2015_Temp.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### precipitation
gdf_other = pd.read_pickle(otherDataFolder+"04_precipitation.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### road Density
gdf_other = pd.read_pickle(otherDataFolder+"05_roadDensity.pkl")
gdf_other.columns
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### coastline distance
gdf_other = pd.read_pickle(otherDataFolder+"06_CoastLine.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### high population density
gdf_other = pd.read_pickle(otherDataFolder+"07_PopulationDensityClass.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_other = gdf_other.rename(columns = \
                             {"within" : "highPop_within", \
                              "dist" : "highPop_dist"})
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### railway distance
gdf_other = pd.read_pickle(otherDataFolder+"08_RailwayDist.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

### poi distance
gdf_other = pd.read_pickle(otherDataFolder+"09_PoiDist.pkl")
gdf_other.columns
gdf_other = gdf_other.drop(columns = ['x', 'y', 'geometry'])
gdf_other = gdf_other[['id', 'school_dist', 'hospital_dist', \
                       'park_dist', 'welfare_dist', \
                           'firestation_dist', 'postOffice_dist']]
gdf_other = gdf_other.astype('float')
gdf_other.id = gdf_other.id.astype('int')
gdf_mesh = pd.merge(gdf_mesh, gdf_other, on = "id", how = 'left')
del gdf_other

gdf_mesh.to_pickle(otherDataFolder+"99_mergedDataset2015.pkl")
