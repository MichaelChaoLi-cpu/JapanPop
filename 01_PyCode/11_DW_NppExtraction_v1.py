# -*- coding: utf-8 -*-
"""
get NPP from MOD17AHGF

year: 2015

Point: Japanese 3rd time Mesh 1 Km centroid

Created on Sun Apr 17 15:27:21 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import pandas as pd
import geopandas as gpd
import numpy as np
from osgeo import gdal
import os
import glob
import rasterio

year = 2015
aimFolder = "F:/17_Article/01_Data/02_NetPrimaryProductivity"
os.mkdir(aimFolder + "\\temp")
rasterFile = glob.glob("F:/17_Article/01_Data/02_NetPrimaryProductivity/Net_PP_Yearly_500m_v6/Npp/*"+str(year) +"_001.tif")

tifflayer_0 = gdal.Open(rasterFile[0], gdal.GA_ReadOnly)
tifflayer_1 = gdal.Open(rasterFile[1], gdal.GA_ReadOnly)

nband = 1
geotransform = tifflayer_0.GetGeoTransform()
spatialreference = tifflayer_0.GetProjection()

tifflayer_0_array = tifflayer_0.ReadAsArray()
tifflayer_0_array = np.array(tifflayer_0_array)
tifflayer_0_array = tifflayer_0_array.astype(float)
tifflayer_0_array[tifflayer_0_array == 65535] = np.nan
tifflayer_0_array[tifflayer_0_array > 32760] = 0

tifflayer_1_array = tifflayer_1.ReadAsArray()
tifflayer_1_array = np.array(tifflayer_1_array)
tifflayer_1_array = tifflayer_1_array.astype(float)
tifflayer_1_array[tifflayer_1_array == 65535] = np.nan
tifflayer_1_array[tifflayer_1_array > 32760] = 0

tifflayer_double_array = np.array([tifflayer_0_array, tifflayer_1_array])
tifflayer_mean_array = np.nanmean(tifflayer_double_array, axis = 0)

ncol = tifflayer_mean_array.shape[1]
nrow = tifflayer_mean_array.shape[0]

temp_file = aimFolder + "/temp/temp_file.tif"

driver = gdal.GetDriverByName("GTiff")
dst_dataset = driver.Create(temp_file, ncol, nrow, nband, gdal.GDT_Float32)
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)
dst_dataset.GetRasterBand(1).WriteArray(tifflayer_mean_array)
dst_dataset = None

original_temp_raster = gdal.Open(temp_file, gdal.GA_ReadOnly)
raster_rprj = gdal.Warp(aimFolder + "/temp/temp_file_0008.tif", original_temp_raster, dstSRS = "EPSG:4326", 
                        xRes = 0.008, yRes = 0.008, resampleAlg = "average")
original_temp_raster = None
raster_rprj = None

coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

rasterFile = rasterio.open(aimFolder + "/temp/temp_file_0008.tif")
aimPoint = coords_extration
rasterArray = rasterFile.read(1)

valueArray = []
for point in aimPoint['geometry']:
    x = point.xy[0][0]
    y = point.xy[1][0]
    row, col = rasterFile.index(x, y)
    valueArray.append(rasterArray[row, col])
    
valueArray = np.array(valueArray)
coords_extration['NPP_'+str(year)] = valueArray

coords_extration.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/01_2015_NPP.pkl")

rasterFile = None

os.remove(temp_file)
os.remove(aimFolder + "/temp/temp_file_0008.tif")

os.rmdir(aimFolder + "\\temp")
