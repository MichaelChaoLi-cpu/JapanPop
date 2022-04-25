# -*- coding: utf-8 -*-
"""
Source: GPM IMERG Final Precipitation L3 1 day 0.1 degree x 0.1 degree V06 (GPM_3IMERGDF)

####drop: Source: GPM DPR Precipitation Profile L2A 1.5 hours 5 km V06 (GPM_2ADPR)

Year: 2015

Created on Wed Apr 20 15:04:28 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import numpy as np
import os
from osgeo import gdal
import glob
import geopandas as gpd
import rasterio

rawFileLocation = "F:/17_Article/01_Data/11_precipitation/"

os.mkdir(rawFileLocation + "/temp")

year = 2015
rawFileList = glob.glob(rawFileLocation + "*.HDF5")

annualAveragePrecipitation = []
for hdf5File in rawFileList:
    hdflayer = gdal.Open(hdf5File, gdal.GA_ReadOnly)
    #for line in hdflayer.GetSubDatasets(): print(line)
    
    subhdflayer = hdflayer.GetSubDatasets()[3][0]
    rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)
    rlayerArray = rlayer.ReadAsArray()
    rlayerArray[rlayerArray < 0] = np.nan
    annualAveragePrecipitation.append(rlayerArray)
    rlayerArray = None

annualAveragePrecipitation = np.nanmean(annualAveragePrecipitation, axis = 0)   
annualAveragePrecipitation = annualAveragePrecipitation.transpose()
    
outputAnnualRasterName = rawFileLocation + "/temp/" + str(year) + "_precipitation_m.tif"

ncol = annualAveragePrecipitation.shape[1]
nrow = annualAveragePrecipitation.shape[0]
nband = 1
geotransform = (-180.0, 0.1, 0.0, -90.0, 0.0, 0.1)

src_dataset = gdal.Open("D:/10_Article/08_MonthlyRaster/IDW_REM/200702.tif")
#geotransform = src_dataset.GetGeoTransform()
spatialreference = src_dataset.GetProjection()
src_dataset = None

# write the tif files
driver = gdal.GetDriverByName("GTiff")
dst_dataset = driver.Create(outputAnnualRasterName, ncol, nrow, nband, gdal.GDT_Float32)
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)
dst_dataset.GetRasterBand(1).WriteArray(annualAveragePrecipitation)
dst_dataset = None

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

coords_extration = coordExtractionFromRaster(outputAnnualRasterName,
                                             coords_extration, 'precipitation_'+str(year))

coords_extration.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/04_precipitation.pkl")

dropList = glob.glob(rawFileLocation  + "\\temp\\*")
for dropFile in dropList:
    os.remove(dropFile)

os.rmdir(rawFileLocation  + "\\temp")