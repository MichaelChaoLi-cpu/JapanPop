# -*- coding: utf-8 -*-
"""
Source: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v2_3.html

Created on Wed Apr 27 11:58:43 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import zipfile
import glob
import geopandas as gpd

aimFolder = "F:\\17_Article\\01_Data\\15_RailWay"
os.mkdir(aimFolder + "\\temp")

### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="100.0.4896.60").install(), chrome_options = chromeOptions)

locationService = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v2_3.html"
driver.get(locationService)

# /html/body/main/div/table/tbody/tr[2]/td[6]/a
# /html/body/main/div/table/tbody/tr[3]/td[6]/a
# ...
# /html/body/main/div/table/tbody/tr[15]/td[6]/a

### download the zip file
beginIndex = 2

while beginIndex < 16:
    driver.find_element_by_xpath("/html/body/main/div/table/tbody/tr[" + str(beginIndex) + "]/td[6]/a").click()
    time.sleep(2)
    
    driver.switch_to.alert.accept()
    time.sleep(2)
    
    beginIndex += 1

driver.quit()

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\temp" + "\\*15*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")
        
for fileName in fileList:
    railwayShapeFile = gpd.read_file(fileName)
### remember here should be the loop   
railwayShapeFile = railwayShapeFile.dissolve()
railwayShapeFile = railwayShapeFile.to_crs(epsg = 4326)
railwayShapeFile = railwayShapeFile[['geometry']]

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

joinDistance = coords_extration.sjoin_nearest(railwayShapeFile, distance_col = "dist")
joinDistance = joinDistance.rename(columns = {"dist" : "rail_dist"})
joinDistance.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/08_RailwayDist.pkl")
