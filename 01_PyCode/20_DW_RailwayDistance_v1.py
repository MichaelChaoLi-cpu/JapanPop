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
railwayShapeFile2007 = gpd.read_file(aimFolder + "\\temp\\N02-07-g_RailroadSection.shp" )
railwayShapeFile2007 = railwayShapeFile2007.dissolve()
railwayShapeFile2007 = railwayShapeFile2007.set_crs(epsg = 4326)
railwayShapeFile2007 = railwayShapeFile2007[['geometry']]

toRailway2007 = coords_extration.sjoin_nearest(railwayShapeFile2007, distance_col = "distRailway")
toRailway2007 = pd.DataFrame(toRailway2007.drop(columns=['geometry', 'index_right']))
toRailway2007['year'] = 2007
toRailway2007 = toRailway2007.set_index(['G04c_001', 'year'])

stationShapeFile2007 = gpd.read_file(aimFolder + "\\temp\\N02-07-g_Station.shp" )
stationShapeFile2007 = stationShapeFile2007.dissolve()
stationShapeFile2007 = stationShapeFile2007.set_crs(epsg = 4326)
stationShapeFile2007 = stationShapeFile2007[['geometry']]

toStation2007 = coords_extration.sjoin_nearest(stationShapeFile2007, distance_col = "distStation")
toStation2007 = pd.DataFrame(toStation2007.drop(columns=['geometry', 'index_right']))
toStation2007['year'] = 2007
toStation2007 = toStation2007.set_index(['G04c_001', 'year'])

railStation2007 = pd.concat([toRailway2007, toStation2007], axis=1)

### 2008
railwayShapeFile2008 = gpd.read_file(aimFolder + "\\temp\\N02-08-g_RailroadSection.shp" )
railwayShapeFile2008 = railwayShapeFile2008.dissolve()
railwayShapeFile2008 = railwayShapeFile2008.set_crs(epsg = 4326)
railwayShapeFile2008 = railwayShapeFile2008[['geometry']]

toRailway2008 = coords_extration.sjoin_nearest(railwayShapeFile2008, distance_col = "distRailway")
toRailway2008 = pd.DataFrame(toRailway2008.drop(columns=['geometry', 'index_right']))
toRailway2008['year'] = 2008
toRailway2008 = toRailway2008.set_index(['G04c_001', 'year'])

stationShapeFile2008 = gpd.read_file(aimFolder + "\\temp\\N02-08-g_Station.shp" )
stationShapeFile2008 = stationShapeFile2008.dissolve()
stationShapeFile2008 = stationShapeFile2008.set_crs(epsg = 4326)
stationShapeFile2008 = stationShapeFile2008[['geometry']]

toStation2008 = coords_extration.sjoin_nearest(stationShapeFile2008, distance_col = "distStation")
toStation2008 = pd.DataFrame(toStation2008.drop(columns=['geometry', 'index_right']))
toStation2008['year'] = 2008
toStation2008 = toStation2008.set_index(['G04c_001', 'year'])

railStation2008 = pd.concat([toRailway2008, toStation2008], axis=1)

### 2011
railwayShapeFile2011 = gpd.read_file(aimFolder + "\\temp\\N02-11_RailroadSection.shp" )
railwayShapeFile2011 = railwayShapeFile2011.dissolve()
railwayShapeFile2011 = railwayShapeFile2011.set_crs(epsg = 4326)
railwayShapeFile2011 = railwayShapeFile2011[['geometry']]

toRailway2011 = coords_extration.sjoin_nearest(railwayShapeFile2011, distance_col = "distRailway")
toRailway2011 = pd.DataFrame(toRailway2011.drop(columns=['geometry', 'index_right']))
toRailway2011['year'] = 2011
toRailway2011 = toRailway2011.set_index(['G04c_001', 'year'])

stationShapeFile2011 = gpd.read_file(aimFolder + "\\temp\\N02-11_Station.shp" )
stationShapeFile2011 = stationShapeFile2011.dissolve()
stationShapeFile2011 = stationShapeFile2011.set_crs(epsg = 4326)
stationShapeFile2011 = stationShapeFile2011[['geometry']]

toStation2011 = coords_extration.sjoin_nearest(stationShapeFile2011, distance_col = "distStation")
toStation2011 = pd.DataFrame(toStation2011.drop(columns=['geometry', 'index_right']))
toStation2011['year'] = 2011
toStation2011 = toStation2011.set_index(['G04c_001', 'year'])

railStation2011 = pd.concat([toRailway2011, toStation2011], axis=1)

### 2012
railwayShapeFile2012 = gpd.read_file(aimFolder + "\\temp\\N02-12_RailroadSection.shp" )
railwayShapeFile2012 = railwayShapeFile2012.dissolve()
railwayShapeFile2012 = railwayShapeFile2012.set_crs(epsg = 4326)
railwayShapeFile2012 = railwayShapeFile2012[['geometry']]

toRailway2012 = coords_extration.sjoin_nearest(railwayShapeFile2012, distance_col = "distRailway")
toRailway2012 = pd.DataFrame(toRailway2012.drop(columns=['geometry', 'index_right']))
toRailway2012['year'] = 2012
toRailway2012 = toRailway2012.set_index(['G04c_001', 'year'])

stationShapeFile2012 = gpd.read_file(aimFolder + "\\temp\\N02-12_Station.shp" )
stationShapeFile2012 = stationShapeFile2012.dissolve()
stationShapeFile2012 = stationShapeFile2012.set_crs(epsg = 4326)
stationShapeFile2012 = stationShapeFile2012[['geometry']]

toStation2012 = coords_extration.sjoin_nearest(stationShapeFile2012, distance_col = "distStation")
toStation2012 = pd.DataFrame(toStation2012.drop(columns=['geometry', 'index_right']))
toStation2012['year'] = 2012
toStation2012 = toStation2012.set_index(['G04c_001', 'year'])

railStation2012 = pd.concat([toRailway2012, toStation2012], axis=1)

### 2013
railwayShapeFile2013 = gpd.read_file(aimFolder + "\\temp\\N02-13_RailroadSection.shp" )
railwayShapeFile2013 = railwayShapeFile2013.dissolve()
railwayShapeFile2013 = railwayShapeFile2013.set_crs(epsg = 4326)
railwayShapeFile2013 = railwayShapeFile2013[['geometry']]

toRailway2013 = coords_extration.sjoin_nearest(railwayShapeFile2013, distance_col = "distRailway")
toRailway2013 = pd.DataFrame(toRailway2013.drop(columns=['geometry', 'index_right']))
toRailway2013['year'] = 2013
toRailway2013 = toRailway2013.set_index(['G04c_001', 'year'])

stationShapeFile2013 = gpd.read_file(aimFolder + "\\temp\\N02-13_Station.shp" )
stationShapeFile2013 = stationShapeFile2013.dissolve()
stationShapeFile2013 = stationShapeFile2013.set_crs(epsg = 4326)
stationShapeFile2013 = stationShapeFile2013[['geometry']]

toStation2013 = coords_extration.sjoin_nearest(stationShapeFile2013, distance_col = "distStation")
toStation2013 = pd.DataFrame(toStation2013.drop(columns=['geometry', 'index_right']))
toStation2013['year'] = 2013
toStation2013 = toStation2013.set_index(['G04c_001', 'year'])

railStation2013 = pd.concat([toRailway2013, toStation2013], axis=1)

### 2014
railwayShapeFile2014 = gpd.read_file(aimFolder + "\\temp\\N02-14_RailroadSection.shp" )
railwayShapeFile2014 = railwayShapeFile2014.dissolve()
railwayShapeFile2014 = railwayShapeFile2014.set_crs(epsg = 4326)
railwayShapeFile2014 = railwayShapeFile2014[['geometry']]

toRailway2014 = coords_extration.sjoin_nearest(railwayShapeFile2014, distance_col = "distRailway")
toRailway2014 = pd.DataFrame(toRailway2014.drop(columns=['geometry', 'index_right']))
toRailway2014['year'] = 2014
toRailway2014 = toRailway2014.set_index(['G04c_001', 'year'])

stationShapeFile2014 = gpd.read_file(aimFolder + "\\temp\\N02-14_Station.shp" )
stationShapeFile2014 = stationShapeFile2014.dissolve()
stationShapeFile2014 = stationShapeFile2014.set_crs(epsg = 4326)
stationShapeFile2014 = stationShapeFile2014[['geometry']]

toStation2014 = coords_extration.sjoin_nearest(stationShapeFile2014, distance_col = "distStation")
toStation2014 = pd.DataFrame(toStation2014.drop(columns=['geometry', 'index_right']))
toStation2014['year'] = 2014
toStation2014 = toStation2014.set_index(['G04c_001', 'year'])

railStation2014 = pd.concat([toRailway2014, toStation2014], axis=1)

joinDistance = coords_extration.sjoin_nearest(railwayShapeFile, distance_col = "dist")
joinDistance = joinDistance.rename(columns = {"dist" : "rail_dist"})
joinDistance.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/08_RailwayDist.pkl")
