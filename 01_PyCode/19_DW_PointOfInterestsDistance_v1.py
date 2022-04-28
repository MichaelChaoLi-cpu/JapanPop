# -*- coding: utf-8 -*-
"""
Point of interest

Created on Wed Apr 27 16:40:00 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import pandas as pd
import zipfile
import glob
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

### school
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\school"

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder)
     
fileName = glob.glob(aimFolder + "\\*\\*.shp")
schoolShapeFile = gpd.read_file(fileName[0])
schoolShapeFile = schoolShapeFile[['geometry']]
schoolShapeFile.crs
schoolShapeFile = schoolShapeFile.to_crs(epsg = 4326)
schoolShapeFile = schoolShapeFile.dissolve()

coords_extration = coords_extration.sjoin_nearest(schoolShapeFile, distance_col = "school_dist")

### hospital
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\hospital"

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder)
        
fileName = glob.glob(aimFolder + "\\*\\*.shp")
hospitalShapeFile = gpd.read_file(fileName[0])
hospitalShapeFile = hospitalShapeFile[['geometry']]
hospitalShapeFile.crs
hospitalShapeFile = hospitalShapeFile.set_crs(epsg = 6668)
hospitalShapeFile = hospitalShapeFile.to_crs(epsg = 4326)
hospitalShapeFile = hospitalShapeFile.dissolve()

coords_extration = coords_extration.drop(columns = ['index_right'])
coords_extration = coords_extration.sjoin_nearest(hospitalShapeFile, distance_col = "hospital_dist")

### park
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\park"
os.mkdir(aimFolder + "\\temp")

### park
### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="100.0.4896.60").install(), chrome_options = chromeOptions)

locationService = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P13.html"
driver.get(locationService)

# /html/body/main/div/table/tbody/tr[2]/td[6]/a
# /html/body/main/div/table/tbody/tr[3]/td[6]/a
# ...
# /html/body/main/div/table/tbody/tr[48]/td[6]/a

### download the zip file
beginIndex = 2

while beginIndex < 49:
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
    
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf = gdf[['geometry']]
gdf.to_file(aimFolder + "\\MergedPark.shp")

### remove the temp folder 
for root, dirs, files in os.walk(aimFolder + "\\temp", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(aimFolder + "\\temp")

gdf.crs
gdf = gdf.set_crs(epsg = 6668)
gdf = gdf.to_crs(epsg = 4326)

coords_extration = coords_extration.drop(columns = ['index_right'])
coords_extration = coords_extration.sjoin_nearest(gdf, distance_col = "park_dist")



### welfare facility
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\welfare"
try:
    os.mkdir(aimFolder)
except:
    pass
os.mkdir(aimFolder + "\\temp")

### welfare
### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="100.0.4896.60").install(), chrome_options = chromeOptions)

locationService = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P14.html"
driver.get(locationService)

# /html/body/main/div/table/tbody/tr[2]/td[6]/a
# /html/body/main/div/table/tbody/tr[3]/td[6]/a
# ...
# /html/body/main/div/table/tbody/tr[94]/td[6]/a

### download the zip file
beginIndex = 2

while beginIndex < 95:
    driver.find_element_by_xpath("/html/body/main/div/table/tbody/tr[" + str(beginIndex) + "]/td[6]/a").click()
    time.sleep(2)
    
    driver.switch_to.alert.accept()
    time.sleep(2)
    
    beginIndex += 1

driver.quit()

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\temp" + "\\P14-15*.zip")
fileAdd = glob.glob(aimFolder + "\\temp" + "\\P14-11_27*.zip")
fileList = fileList.append(fileAdd[0])
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")
        
### read the shapefile        
shapeFileList = glob.glob(aimFolder + "\\temp" + "\\*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf = gdf[['geometry']]
gdf.to_file(aimFolder + "\\MergedWelfare.shp")

### remove the temp folder 
for root, dirs, files in os.walk(aimFolder + "\\temp", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(aimFolder + "\\temp")

gdf.crs
gdf = gdf.set_crs(epsg = 6668)
gdf = gdf.to_crs(epsg = 4326)

coords_extration = coords_extration.drop(columns = ['index_right'])
coords_extration = coords_extration.sjoin_nearest(gdf, distance_col = "welfare_dist")

### fire station
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\fireStation"
try:
    os.mkdir(aimFolder)
except:
    pass
os.mkdir(aimFolder + "\\temp")

### fire station
### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="100.0.4896.60").install(), chrome_options = chromeOptions)

locationService = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P17.html"
driver.get(locationService)

# /html/body/main/div/table/tbody/tr[2]/td[6]/a
# /html/body/main/div/table/tbody/tr[3]/td[6]/a
# ...
# /html/body/main/div/table/tbody/tr[48]/td[6]/a

### download the zip file
beginIndex = 2

while beginIndex < 49:
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
shapeFileList = glob.glob(aimFolder + "\\temp" + "\\*Station.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf = gdf[['geometry']]
gdf.to_file(aimFolder + "\\MergedFirestation.shp")

### remove the temp folder 
for root, dirs, files in os.walk(aimFolder + "\\temp", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(aimFolder + "\\temp")

gdf.crs
gdf = gdf.set_crs(epsg = 6668)
gdf = gdf.to_crs(epsg = 4326)

coords_extration = coords_extration.drop(columns = ['index_right'])
coords_extration = coords_extration.sjoin_nearest(gdf, distance_col = "firestation_dist")

### post office
aimFolder = "F:\\17_Article\\01_Data\\07_PointOfInterest\\postOffice"
try:
    os.mkdir(aimFolder)
except:
    pass

fileList = glob.glob(aimFolder + "\\*.shp")

gdf = gpd.read_file(fileList[0])

gdf.crs
gdf = gdf.to_crs(epsg = 4326)

coords_extration = coords_extration.drop(columns = ['index_right'])
coords_extration = coords_extration.sjoin_nearest(gdf, distance_col = "postOffice_dist")

coords_extration.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/09_PoiDist.pkl")
