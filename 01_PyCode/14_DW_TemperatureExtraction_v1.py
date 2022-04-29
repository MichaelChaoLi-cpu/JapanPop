# -*- coding: utf-8 -*-
"""
Source: MOD11A2 

Warning: we do not solve the issues in gdal.Wrap(), "average" with nan.

Created on Thu Apr 21 14:42:51 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import os
import glob
from osgeo import gdal
import numpy as np
import gc
import geopandas as gpd
import rasterio
import math

aimFolder = "F:\\17_Article\\01_Data\\08_Temperature\\Surf_Temp_8Days_1Km_v6"
os.mkdir(aimFolder + "\\temp")
year = 2015

### Day time Temp
dayTimeTemperatureFileList = glob.glob(aimFolder + "\\LST_Day_1km\\M*2015*.tif")

dayTimeTemperatureRasterList = []
for dayTimeTemperatureFile in dayTimeTemperatureFileList:
    dayTimeTemperatureRasterRaw = gdal.Open(dayTimeTemperatureFile, gdal.GA_ReadOnly)
    dayTimeTemperatureRaster = dayTimeTemperatureRasterRaw.ReadAsArray()
    dayTimeTemperatureRasterRaw = None
    dayTimeTemperatureRaster = dayTimeTemperatureRaster.astype("float")
    dayTimeTemperatureRaster[dayTimeTemperatureRaster == 0] = np.nan
    dayTimeTemperatureRaster = dayTimeTemperatureRaster * 0.02 - 273.16
    dayTimeTemperatureRasterList.append(dayTimeTemperatureRaster)

meanDayTimeTemperatureRaster = np.nanmean(dayTimeTemperatureRasterList, axis = 0)
stdDayTimeTemperatureRaster = np.nanstd(dayTimeTemperatureRasterList, axis = 0)
dayTimeTemperatureRasterList = None
gc.collect()

src_dataset = gdal.Open(dayTimeTemperatureFileList[0], gdal.GA_ReadOnly)
geotransform = src_dataset.GetGeoTransform()
spatialreference = src_dataset.GetProjection()
ncol = meanDayTimeTemperatureRaster.shape[1]
nrow = meanDayTimeTemperatureRaster.shape[0]
nband = 1
src_dataset = None

# write the tif files
driver = gdal.GetDriverByName("GTiff")
dst_dataset = driver.Create(aimFolder + "\\temp\\2015_daytime_mean.tif", ncol, nrow, nband, gdal.GDT_Float32) 
#### ^^^^^ Change this line
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)
dst_dataset.GetRasterBand(1).WriteArray(meanDayTimeTemperatureRaster)
dst_dataset = None

# write the tif files
driver = gdal.GetDriverByName("GTiff")
dst_dataset = driver.Create(aimFolder + "\\temp\\2015_daytime_std.tif", ncol, nrow, nband, gdal.GDT_Float32) 
#### ^^^^^ Change this line
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)
dst_dataset.GetRasterBand(1).WriteArray(stdDayTimeTemperatureRaster)
dst_dataset = None

### resample and reproject
raster_rprj = gdal.Warp(aimFolder + "\\temp\\2015_daytime_mean_re.tif", 
                        aimFolder + "\\temp\\2015_daytime_mean.tif", dstSRS = "EPSG:4326",
                        xRes = 0.008, yRes = 0.008, resampleAlg = "average", srcNodata = math.nan)
raster_rprj = None

raster_rprj = gdal.Warp(aimFolder + "\\temp\\2015_daytime_std_re.tif", 
                        aimFolder + "\\temp\\2015_daytime_std.tif", dstSRS = "EPSG:4326",
                        xRes = 0.008, yRes = 0.008, resampleAlg = "average", srcNodata = math.nan)
raster_rprj = None

### Night time Temp
nightTimeTemperatureFileList = glob.glob(aimFolder + "\\LST_Night_1km\\M*2015*.tif")

nightTimeTemperatureRasterList = []
for nightTimeTemperatureFile in nightTimeTemperatureFileList:
    nightTimeTemperatureRasterRaw = gdal.Open(nightTimeTemperatureFile, gdal.GA_ReadOnly)
    nightTimeTemperatureRaster = nightTimeTemperatureRasterRaw.ReadAsArray()
    nightTimeTemperatureRasterRaw = None
    nightTimeTemperatureRaster = nightTimeTemperatureRaster.astype("float")
    nightTimeTemperatureRaster[nightTimeTemperatureRaster == 0] = np.nan
    nightTimeTemperatureRaster = nightTimeTemperatureRaster * 0.02 - 273.16
    nightTimeTemperatureRasterList.append(nightTimeTemperatureRaster)

meanNightTimeTemperatureRaster = np.nanmean(nightTimeTemperatureRasterList, axis = 0)
stdNightTimeTemperatureRaster = np.nanstd(nightTimeTemperatureRasterList, axis = 0)
nightTimeTemperatureRasterList = None
gc.collect()

# write the tif files
driver = gdal.GetDriverByName("GTiff")
dst_dataset = driver.Create(aimFolder + "\\temp\\2015_nighttime_mean.tif", ncol, nrow, nband, gdal.GDT_Float32) 
#### ^^^^^ Change this line
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)
dst_dataset.GetRasterBand(1).WriteArray(meanNightTimeTemperatureRaster)
dst_dataset = None

# write the tif files
driver = gdal.GetDriverByName("GTiff")
dst_dataset = driver.Create(aimFolder + "\\temp\\2015_nighttime_std.tif", ncol, nrow, nband, gdal.GDT_Float32) 
#### ^^^^^ Change this line
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)
dst_dataset.GetRasterBand(1).WriteArray(stdNightTimeTemperatureRaster)
dst_dataset = None

### resample and reproject
raster_rprj = gdal.Warp(aimFolder + "\\temp\\2015_nighttime_mean_re.tif", 
                        aimFolder + "\\temp\\2015_nighttime_mean.tif", dstSRS = "EPSG:4326",
                        xRes = 0.008, yRes = 0.008, resampleAlg = "average", srcNodata = math.nan)
raster_rprj = None

raster_rprj = gdal.Warp(aimFolder + "\\temp\\2015_nighttime_std_re.tif", 
                        aimFolder + "\\temp\\2015_nighttime_std.tif", dstSRS = "EPSG:4326",
                        xRes = 0.008, yRes = 0.008, resampleAlg = "average", srcNodata = math.nan)
raster_rprj = None

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

def coordExtractionFromRaster(RasterName, GeoPandasDataFrame, NewColumnName):
    rasterFile = rasterio.open(RasterName)
    coords_extration = GeoPandasDataFrame.copy()
    aimPoint = coords_extration
    rasterArray = rasterFile.read(1)
    
    valueArray = []
    for point in aimPoint['geometry']:
        x = point.xy[0][0]
        y = point.xy[1][0]
        row, col = rasterFile.index(x, y)
        valueArray.append(rasterArray[row, col])
        
    valueArray = np.array(valueArray)
    coords_extration[NewColumnName] = valueArray
    rasterFile = None
    return coords_extration

coords_extration = coordExtractionFromRaster(aimFolder + "\\temp\\2015_daytime_mean_re.tif",
                                             coords_extration, 'dayTimeMeanTemp_'+str(year))
coords_extration = coordExtractionFromRaster(aimFolder + "\\temp\\2015_daytime_std_re.tif",
                                             coords_extration, 'dayTimeStdTemp_'+str(year))
coords_extration = coordExtractionFromRaster(aimFolder + "\\temp\\2015_nighttime_mean_re.tif",
                                             coords_extration, 'nightTimeMeanTemp_'+str(year))
coords_extration = coordExtractionFromRaster(aimFolder + "\\temp\\2015_nighttime_std_re.tif",
                                             coords_extration, 'nightTimeStdTemp_'+str(year))

colname = coords_extration.columns
print(coords_extration[colname[4]].isna().sum())
print(coords_extration[colname[5]].isna().sum())
print(coords_extration[colname[6]].isna().sum())
print(coords_extration[colname[7]].isna().sum())

coords_extration.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/03_2015_Temp.pkl")

dropList = glob.glob(aimFolder + "\\temp\\*")
for dropFile in dropList:
    os.remove(dropFile)

os.rmdir(aimFolder + "\\temp")
