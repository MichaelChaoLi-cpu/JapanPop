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
import pandas as pd

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
fileList = glob.glob(aimFolder + "\\temp" + "\\*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder + "\\temp")

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")

### remember here should be the loop 
### 2005
railwayShapeFile2005 = gpd.read_file(aimFolder + "\\temp\\N02-05-g_RailroadSection.shp" )
railwayShapeFile2005 = railwayShapeFile2005.dissolve()
railwayShapeFile2005 = railwayShapeFile2005.set_crs(epsg = 4326)
railwayShapeFile2005 = railwayShapeFile2005[['geometry']]

toRailway2005 = coords_extration.sjoin_nearest(railwayShapeFile2005, distance_col = "distRailway")
toRailway2005 = pd.DataFrame(toRailway2005.drop(columns=['geometry', 'index_right']))
toRailway2005['year'] = 2005
toRailway2005 = toRailway2005.set_index(['G04c_001', 'year'])

stationShapeFile2005 = gpd.read_file(aimFolder + "\\temp\\N02-05-g_Station.shp" )
stationShapeFile2005 = stationShapeFile2005.dissolve()
stationShapeFile2005 = stationShapeFile2005.set_crs(epsg = 4326)
stationShapeFile2005 = stationShapeFile2005[['geometry']]

toStation2005 = coords_extration.sjoin_nearest(stationShapeFile2005, distance_col = "distStation")
toStation2005 = pd.DataFrame(toStation2005.drop(columns=['geometry', 'index_right']))
toStation2005['year'] = 2005
toStation2005 = toStation2005.set_index(['G04c_001', 'year'])

railStation2005 = pd.concat([toRailway2005, toStation2005], axis=1)

### 2006
railwayShapeFile2006 = gpd.read_file(aimFolder + "\\temp\\N02-06-g_RailroadSection.shp" )
railwayShapeFile2006 = railwayShapeFile2006.dissolve()
railwayShapeFile2006 = railwayShapeFile2006.set_crs(epsg = 4326)
railwayShapeFile2006 = railwayShapeFile2006[['geometry']]

toRailway2006 = coords_extration.sjoin_nearest(railwayShapeFile2006, distance_col = "distRailway")
toRailway2006 = pd.DataFrame(toRailway2006.drop(columns=['geometry', 'index_right']))
toRailway2006['year'] = 2006
toRailway2006 = toRailway2006.set_index(['G04c_001', 'year'])

stationShapeFile2006 = gpd.read_file(aimFolder + "\\temp\\N02-06-g_Station.shp" )
stationShapeFile2006 = stationShapeFile2006.dissolve()
stationShapeFile2006 = stationShapeFile2006.set_crs(epsg = 4326)
stationShapeFile2006 = stationShapeFile2006[['geometry']]

toStation2006 = coords_extration.sjoin_nearest(stationShapeFile2006, distance_col = "distStation")
toStation2006 = pd.DataFrame(toStation2006.drop(columns=['geometry', 'index_right']))
toStation2006['year'] = 2006
toStation2006 = toStation2006.set_index(['G04c_001', 'year'])

railStation2006 = pd.concat([toRailway2006, toStation2006], axis=1)

### 2007
railwayShapeFile2007 = gpd.read_file(aimFolder + "\\temp\\N02-06-g_RailroadSection.shp" )
railwayShapeFile2007 = railwayShapeFile2007.dissolve()
railwayShapeFile2007 = railwayShapeFile2007.set_crs(epsg = 4326)
railwayShapeFile2007 = railwayShapeFile2007[['geometry']]

toRailway2007 = coords_extration.sjoin_nearest(railwayShapeFile2007, distance_col = "distRailway")
toRailway2007 = pd.DataFrame(toRailway2007.drop(columns=['geometry', 'index_right']))
toRailway2007['year'] = 2007
toRailway2007 = toRailway2007.set_index(['G04c_001', 'year'])

stationShapeFile2007 = gpd.read_file(aimFolder + "\\temp\\N02-06-g_Station.shp" )
stationShapeFile2007 = stationShapeFile2007.dissolve()
stationShapeFile2007 = stationShapeFile2007.set_crs(epsg = 4326)
stationShapeFile2007 = stationShapeFile2007[['geometry']]

toStation2007 = coords_extration.sjoin_nearest(stationShapeFile2007, distance_col = "distStation")
toStation2007 = pd.DataFrame(toStation2007.drop(columns=['geometry', 'index_right']))
toStation2007['year'] = 2007
toStation2007 = toStation2007.set_index(['G04c_001', 'year'])

railStation2007 = pd.concat([toRailway2007, toStation2007], axis=1)


joinDistance = coords_extration.sjoin_nearest(railwayShapeFile, distance_col = "dist")
joinDistance = joinDistance.rename(columns = {"dist" : "rail_dist"})
joinDistance.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/08_RailwayDist.pkl")
