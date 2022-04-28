# -*- coding: utf-8 -*-
"""
Point of interest

Created on Wed Apr 27 16:40:00 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import pandas as pd
import zipfile
import glob

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

### school
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\school"

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder)
     
fileName = glob.glob(aimFolder + "\\*\\*.shp")
schoolShapeFile = gpd.read_file(fileName[0])
schoolShapeFile = schoolShapeFile[['geometry']]
schoolShapeFile.crs
schoolShapeFile = schoolShapeFile.to_crs(epsg = 4326)
schoolShapeFile = schoolShapeFile.dissolve()

coords_extration = coords_extration.sjoin_nearest(schoolShapeFile, distance_col = "school_dist")

### hospital
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\hospital"

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder)
        
fileName = glob.glob(aimFolder + "\\*\\*.shp")
hospitalShapeFile = gpd.read_file(fileName[0])
hospitalShapeFile = hospitalShapeFile[['geometry']]
hospitalShapeFile.crs
hospitalShapeFile = hospitalShapeFile.set_crs(epsg = 6668)
hospitalShapeFile = hospitalShapeFile.to_crs(epsg = 4326)
hospitalShapeFile = hospitalShapeFile.dissolve()

coords_extration = coords_extration.drop(columns = ['index_right'])
coords_extration = coords_extration.sjoin_nearest(hospitalShapeFile, distance_col = "hospital_dist")
