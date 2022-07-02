# -*- coding: utf-8 -*-
"""
Download Road Density Mesh 2010 (H22)

unziped them, and merge them into one shapefile

year: 2011 (h22)

Created on Sun Apr 10 17:47:31 2022

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
import numpy as np

aimFolder = "F:\\17_Article\\01_Data\\04_Road"
os.mkdir(aimFolder + "\\temp")

### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="100.0.4896.60").install(), chrome_options = chromeOptions)

locationService = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N04.html"
driver.get(locationService)

# /html/body/main/div/table/tbody/tr[6]/td[6]/a
# /html/body/main/div/table/tbody/tr[11]/td[6]/a
# ...
# /html/body/main/div/table/tbody/tr[775]/td[6]/a

### download the zip file
beginIndex = 6

while beginIndex < 776:
    driver.find_element_by_xpath("/html/body/main/div/table/tbody/tr[" + str(beginIndex) + "]/td[6]/a").click()
    time.sleep(2)
    
    driver.switch_to.alert.accept()
    time.sleep(2)
    
    beginIndex += 1

driver.quit()

### unzip downloaded files 2010 
fileList = glob.glob(aimFolder + "\\temp" + "\\N04-10*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")

### read the shapefile 2010        
shapeFileList = glob.glob(aimFolder + "\\temp" + "\\*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)

### merge the file into one 2010
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf.to_file(aimFolder + "\\MeshRoad2011.shp")

### unzip downloaded files 2002 
fileList = glob.glob(aimFolder + "\\temp" + "\\N04-02*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")

### read the shapefile 2002        
shapeFileList = glob.glob(aimFolder + "\\temp" + "\\N04_14*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)
    
### merge the file into one 2002
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf.to_file(aimFolder + "\\MeshRoad2002.shp")

### unzip downloaded files 2003 
fileList = glob.glob(aimFolder + "\\temp" + "\\N04-03*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")

### read the shapefile 2003        
shapeFileList = glob.glob(aimFolder + "\\temp" + "\\N04_15*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)
    
### merge the file into one 2003
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf.to_file(aimFolder + "\\MeshRoad2003.shp")

### unzip downloaded files 2004 
fileList = glob.glob(aimFolder + "\\temp" + "\\N04-04*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")

### read the shapefile 2003        
shapeFileList = glob.glob(aimFolder + "\\temp" + "\\N04_16*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)
    
### merge the file into one 2003
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf.to_file(aimFolder + "\\MeshRoad2004.shp")

### remove the temp folder 
for root, dirs, files in os.walk(aimFolder + "\\temp", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(aimFolder + "\\temp")

##### this mesh 2002
aimFolder = "F:\\17_Article\\01_Data\\04_Road"
gdpFile2002 = gpd.read_file(aimFolder + "\\MeshRoad2002.shp")
gdpFile2002.replace('unknown', np.nan, inplace=True)
gdpFile2002.iloc[:,2:38] = gdpFile2002.iloc[:,2:38].astype('float')
gdpFile2002['roadLength'] = gdpFile2002.iloc[:,2:38].sum(axis=1)
gdpFile2002 = gdpFile2002.iloc[:,[0,40]]
gdpFile2002['N04_001'] = gdpFile2002['N04_001'].astype('int')
gdpFile2002_1 = gdpFile2002.copy()
gdpFile2002_1['G04c_001'] = gdpFile2002['N04_001']*10 + 1
gdpFile2002_2 = gdpFile2002.copy()
gdpFile2002_2['G04c_001'] = gdpFile2002['N04_001']*10 + 2
gdpFile2002_3 = gdpFile2002.copy()
gdpFile2002_3['G04c_001'] = gdpFile2002['N04_001']*10 + 3
gdpFile2002_4 = gdpFile2002.copy()
gdpFile2002_4['G04c_001'] = gdpFile2002['N04_001']*10 + 4
gdpFile2002 = pd.concat([gdpFile2002_1, gdpFile2002_2, gdpFile2002_3, 
                         gdpFile2002_4], axis=0)
gdpFile2002['year'] = 2002
gdpFile2002 = pd.DataFrame(gdpFile2002)
gdpFile2002 = gdpFile2002.set_index(['G04c_001', 'year'])
gdpFile2002 = gdpFile2002.loc[:,'roadLength']

##### 2003
gdpFile2003 = gpd.read_file(aimFolder + "\\MeshRoad2003.shp")
gdpFile2003.replace('unknown', np.nan, inplace=True)
gdpFile2003.iloc[:,2:38] = gdpFile2003.iloc[:,2:38].astype('float')
gdpFile2003['roadLength'] = gdpFile2003.iloc[:,2:38].sum(axis=1)
gdpFile2003 = gdpFile2003.iloc[:,[0,40]]
gdpFile2003['N04_001'] = gdpFile2003['N04_001'].astype('int')
gdpFile2003_1 = gdpFile2003.copy()
gdpFile2003_1['G04c_001'] = gdpFile2003['N04_001']*10 + 1
gdpFile2003_2 = gdpFile2003.copy()
gdpFile2003_2['G04c_001'] = gdpFile2003['N04_001']*10 + 2
gdpFile2003_3 = gdpFile2003.copy()
gdpFile2003_3['G04c_001'] = gdpFile2003['N04_001']*10 + 3
gdpFile2003_4 = gdpFile2003.copy()
gdpFile2003_4['G04c_001'] = gdpFile2003['N04_001']*10 + 4
gdpFile2003 = pd.concat([gdpFile2003_1, gdpFile2003_2, gdpFile2003_3, 
                         gdpFile2003_4], axis=0)
gdpFile2003['year'] = 2003
gdpFile2003 = pd.DataFrame(gdpFile2003)
gdpFile2003 = gdpFile2003.set_index(['G04c_001', 'year'])
gdpFile2003 = gdpFile2003.loc[:,'roadLength']

gdpFile2004 = gpd.read_file(aimFolder + "\\MeshRoad2004.shp")
gdpFile2004.replace('unknown', np.nan, inplace=True)
gdpFile2004.iloc[:,2:38] = gdpFile2004.iloc[:,2:38].astype('float')
gdpFile2004['roadLength'] = gdpFile2004.iloc[:,2:38].sum(axis=1)
gdpFile2004 = gdpFile2004.iloc[:,[0,40]]
gdpFile2004['N04_001'] = gdpFile2004['N04_001'].astype('int')
gdpFile2004_1 = gdpFile2004.copy()
gdpFile2004_1['G04c_001'] = gdpFile2004['N04_001']*10 + 1
gdpFile2004_2 = gdpFile2004.copy()
gdpFile2004_2['G04c_001'] = gdpFile2004['N04_001']*10 + 2
gdpFile2004_3 = gdpFile2004.copy()
gdpFile2004_3['G04c_001'] = gdpFile2004['N04_001']*10 + 3
gdpFile2004_4 = gdpFile2004.copy()
gdpFile2004_4['G04c_001'] = gdpFile2004['N04_001']*10 + 4
gdpFile2004 = pd.concat([gdpFile2004_1, gdpFile2004_2, gdpFile2004_3, 
                         gdpFile2004_4], axis=0)
gdpFile2004['year'] = 2004
gdpFile2004 = pd.DataFrame(gdpFile2004)
gdpFile2004 = gdpFile2004.set_index(['G04c_001', 'year'])
gdpFile2004 = gdpFile2004.loc[:,'roadLength']

gdpFile2010 = gpd.read_file(aimFolder + "\\MeshRoad2011.shp")
gdpFile2010.replace('unknown', np.nan, inplace=True)
gdpFile2010.iloc[:,2:38] = gdpFile2010.iloc[:,2:38].astype('float')
gdpFile2010['roadLength'] = gdpFile2010.iloc[:,2:38].sum(axis=1)
gdpFile2010 = gdpFile2010.iloc[:,[0,57]]
gdpFile2010['N04_001'] = gdpFile2010['N04_001'].astype('int')
gdpFile2010_1 = gdpFile2010.copy()
gdpFile2010_1['G04c_001'] = gdpFile2010['N04_001']*10 + 1
gdpFile2010_2 = gdpFile2010.copy()
gdpFile2010_2['G04c_001'] = gdpFile2010['N04_001']*10 + 2
gdpFile2010_3 = gdpFile2010.copy()
gdpFile2010_3['G04c_001'] = gdpFile2010['N04_001']*10 + 3
gdpFile2010_4 = gdpFile2010.copy()
gdpFile2010_4['G04c_001'] = gdpFile2010['N04_001']*10 + 4
gdpFile2010 = pd.concat([gdpFile2010_1, gdpFile2010_2, gdpFile2010_3, 
                         gdpFile2010_4], axis=0)
gdpFile2010['year'] = 2010
gdpFile2010 = pd.DataFrame(gdpFile2010)
gdpFile2010 = gdpFile2010.set_index(['G04c_001', 'year'])
gdpFile2010 = gdpFile2010.loc[:,'roadLength']

roadLengthDf = pd.concat([gdpFile2002, gdpFile2003, gdpFile2004, 
                          gdpFile2010], axis=0)
roadLengthDf.to_pickle("F:/17_Article/01_Data/98_20yearPickles/04_RoadLength.pkl")
