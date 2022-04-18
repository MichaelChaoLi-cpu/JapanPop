# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 17:22:38 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import os
import zipfile
import glob
import rasterio
from osgeo import gdal
import geopandas as gpd
import numpy as np

aimFolder = "F:\\17_Article\\01_Data\\03_NTL_VIIRS"
os.mkdir(aimFolder + "\\temp")

year = 2015

filename = aimFolder + "\\" + str(year) + ".zip"
with zipfile.ZipFile(filename, "r") as zip_ref:
    zip_ref.extractall(aimFolder + "\\temp")
    
filename = glob.glob(aimFolder + "\\temp\\*.tif")
shapefile_input = "F:\\17_Article\\01_Data\\00_mesh\\mesh1.shp" 
raster_out = aimFolder + "\\temp\\clip.tif"

results = gdal.Warp(raster_out, filename, cutlineDSName = shapefile_input,
                    cropToCutline = True)

coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")
rasterFile = rasterio.open(raster_out)
aimPoint = coords_extration
rasterArray = rasterFile.read(1)

valueArray = []
for point in aimPoint['geometry']:
    x = point.xy[0][0]
    y = point.xy[1][0]
    row, col = rasterFile.index(x, y)
    valueArray.append(rasterArray[row, col])
    
valueArray = np.array(valueArray)
coords_extration['NTL_'+str(year)] = valueArray

coords_extration.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/02_2015_NTL.pkl")

results = None
rasterFile = None

fileList = glob.glob(aimFolder + "\\temp\\*")
for filename in fileList:
    os.remove(filename)
