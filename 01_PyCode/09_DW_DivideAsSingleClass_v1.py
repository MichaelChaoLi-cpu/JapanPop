# -*- coding: utf-8 -*-
"""
Convert mutliclasses into Single Class

Resolution: 0.008

Created on Mon Apr 11 16:42:38 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from osgeo import gdal
import numpy as np
import os

original_raster = gdal.Open("F:/17_Article/01_Data/01_LandCover/LandCoverMerge/LandCover_UMD_2015_500m.tif")

aimFolder = "F:/17_Article/01_Data/01_LandCover/LandCover0008WGS/"
raster_rprj = gdal.Warp(aimFolder + "LandCover_UMD_2015_0008_WGS.tif", original_raster, dstSRS = "EPSG:4326", 
                        xRes = 0.008, yRes = 0.008, resampleAlg = "mode")

original_raster.FlushCache()
original_raster = None

year = 2015

band = raster_rprj.GetRasterBand(1)

multiLista = band.ReadAsArray()

# reclassification
singleRasterLocation = "F:/17_Article/01_Data/01_LandCover/LandCoverSingleClass/"
driver = gdal.GetDriverByName("GTiff")
aim = 0
while aim < 16:
    print(aim)
    originalToSingleLista = multiLista.copy()
    orignialToSingleListaClip = originalToSingleLista[:,37750:41750].copy()
    #orignialToSingleListaClip = 
    orignialToSingleListaClip[orignialToSingleListaClip == aim] = 100
    orignialToSingleListaClip[orignialToSingleListaClip != 100] = 0
    
    #for j in range(raster_rprj.RasterXSize):
    #    for i in range(raster_rprj.RasterYSize):
    #        if originalToSingleLista[i, j] == aim:
    #            originalToSingleLista[i, j] = 1
    #        else:
    #            originalToSingleLista[i, j] = 0
                
    # create new file
    name = "year_" + str(year) + "_class_" + str(aim) + ".tif"
    singleRaster = driver.Create(singleRasterLocation + name, 4000,3750, 1)
    singleRaster.GetRasterBand(1).WriteArray(orignialToSingleListaClip)
    
    proj = raster_rprj.GetProjection()
    georef = (122.0, 0.008, 0.0, 50.0, 0.0, -0.008)
    singleRaster.SetProjection(proj)
    singleRaster.SetGeoTransform(georef)
    singleRaster.FlushCache()
    singleRaster = None
    aim += 1
    
raster_rprj = None   

os.remove(aimFolder + "LandCover_UMD_2015_0008_WGS.tif")
