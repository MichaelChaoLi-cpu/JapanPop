# -*- coding: utf-8 -*-
"""


####drop: Source: GPM DPR Precipitation Profile L2A 1.5 hours 5 km V06 (GPM_2ADPR)

Year: 2015

Created on Wed Apr 20 15:04:28 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import glob
import os
from osgeo import gdal

rawFileLocation = "F:/17_Article/01_Data/11_precipitation/"

os.mkdir(rawFileLocation + "/temp")
#months = ["01", "02", "03", "04", "05", "06", 
#          "07", "08", "09", "10", "11", "12"]
rawFileList = glob.glob(rawFileLocation + "2A.GPM.DPR.V8-20180723." + "*.HDF5")

for rawFileName in rawFileList:
    hdflayer = gdal.Open(rawFileName, gdal.GA_ReadOnly)
    #print(hdflayer.GetSubDatasets())
    
    ### precipitation rate at near surface range bin
    #a = 0
    #for line in hdflayer.GetSubDatasets(): print(line); print(a); a+=1
    #print(hdflayer.GetSubDatasets()[92])
    subhdflayer = hdflayer.GetSubDatasets()[92][0]
    rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)
    singleRasterArray = rlayer.ReadAsArray()
