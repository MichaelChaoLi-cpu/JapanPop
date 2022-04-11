# -*- coding: utf-8 -*-
"""
Download coastline

unziped them, and merge them into one shapefile

Created on Mon Apr 11 15:04:37 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import zipfile
import glob
import pandas as pd
import geopandas as gpd

aimFolder = "F:\\17_Article\\01_Data\\13_CoastLine"
os.mkdir(aimFolder + "\\temp")

### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="100.0.4896.60").install(), chrome_options = chromeOptions)

locationService = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-C23.html"
driver.get(locationService)

# /html/body/main/div/table/tbody/tr[2]/td[6]/a
# /html/body/main/div/table/tbody/tr[3]/td[6]/a
# ...
# /html/body/main/div/table/tbody/tr[40]/td[6]/a

### download the zip file
beginIndex = 2

while beginIndex < 41:
    driver.find_element_by_xpath("/html/body/main/div/table/tbody/tr[" + str(beginIndex) + "]/td[6]/a").click()
    time.sleep(2)
    
    driver.switch_to.alert.accept()
    time.sleep(2)
    
    beginIndex += 1

driver.quit()

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\temp" + "\\*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")

### read the shapefile        
shapeFileList = glob.glob(aimFolder + "\\temp" + "\\*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)

### merge the file into one
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf.to_file(aimFolder + "\\MergedCoastline.shp")

### remove the temp folder 
for root, dirs, files in os.walk(aimFolder + "\\temp", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(aimFolder + "\\temp")