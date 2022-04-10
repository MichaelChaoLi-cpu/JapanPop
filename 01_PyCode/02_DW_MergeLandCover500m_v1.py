# -*- coding: utf-8 -*-
"""
Merge the Tiff from python 01_DW into Yearly data of the Whole Japan

Created on Fri Apr  8 13:36:13 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from osgeo import gdal
import os
import subprocess
import glob

mergeFolder = "F:/17_Article/01_Data/LandCoverMerge/"

os.chdir("F:/17_Article/01_Data/LandCover500Tif/")

year = ["2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010",
        "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]

loop = 0
while (loop < len(year)):
    aimYearFileName = "MCD12Q1.A" + year[loop] + "*.tif"
    fileList = glob.glob(aimYearFileName)
    
    fileNamePre = "LandCover_UMD_"
    fileExtention = "_500m.tif"
    outputFullName = mergeFolder + fileNamePre  + year[loop] + fileExtention
    
    vrt = gdal.BuildVRT("merged.vrt", fileList)
    gdal.Translate(outputFullName, vrt)
    vrt = None
    
    loop = loop + 1
