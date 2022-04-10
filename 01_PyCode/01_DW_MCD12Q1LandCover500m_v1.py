# -*- coding: utf-8 -*-
"""
Convert hdf to tif

Data Source: MODIS MCD12Q1 

Resolution: 500m

Data: Land cover 

Created on Fri Apr  8 10:52:26 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from osgeo import gdal
import os

landCoverDir = "F:/17_Article/01_Data/LandCover"
rasterFiles = os.listdir(landCoverDir)

loop = 0

while (loop < len(rasterFiles)):
    #Get File Name Prefix
    rasterFilePre = rasterFiles[loop][:-3]
    
    fileExtension = "BBOX.tif"
    
    ## Open HDF file
    hdflayer = gdal.Open(landCoverDir + "/" + rasterFiles[loop], gdal.GA_ReadOnly)
    
    #print (hdflayer.GetSubDatasets())
    
    # Open raster layer
    #hdflayer.GetSubDatasets()[0][0] - for first layer
    #hdflayer.GetSubDatasets()[1][0] - for second layer ...etc
    subhdflayer = hdflayer.GetSubDatasets()[1][0]
    rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)
    #outputName = rlayer.GetMetadata_Dict()['long_name']
    
    outputNameFinal = rasterFilePre + fileExtension
    print(outputNameFinal)
    
    outputFolder = "F:/17_Article/01_Data/LandCover500Tif/"
    
    outputRaster = outputFolder + outputNameFinal

    gdal.Translate(outputRaster,rlayer)
    
    #Display image in QGIS (run it within QGIS python Console) - remove comment to display
    #iface.addRasterLayer(outputRaster, outputNameFinal)
    
    loop = loop + 1
