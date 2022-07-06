# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:24:56 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import zipfile
import glob

aimFolder = "F:\\17_Article\\01_Data\\06_HighDensityPopulation\\A16-00_GML"
### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="103.0.5060.53").install(), chrome_options = chromeOptions)

locationService = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A16-v2_3.html"
driver.get(locationService)

# /html/body/main/div/table/tbody/tr[10]/td[6]/a
# /html/body/main/div/table/tbody/tr[22]/td[6]/a
# ...
# /html/body/main/div/table/tbody/tr[550]/td[6]/a
# /html/body/main/div/table/tbody/tr[560]/td[6]/a

# file name
# /html/body/main/div/table/tbody/tr[2]/td[5]
# ...
# /html/body/main/div/table/tbody/tr[563]/td[5]

beginIndex = 2
xpathList = []
while beginIndex < 563:
    judgeFile = driver.find_element_by_xpath("/html/body/main/div/table/tbody/tr[" + str(beginIndex) + "]/td[5]").text
    time.sleep(0.5)
    if judgeFile[4:6] == '00':
        xpathList.append("/html/body/main/div/table/tbody/tr[" + str(beginIndex) + "]/td[6]/a")
    beginIndex += 1

for xpath in xpathList:
    driver.find_element_by_xpath(xpath).click()
    time.sleep(2)
    
    driver.switch_to.alert.accept()
    time.sleep(2)

### unzip downloaded files
fileList = glob.glob(aimFolder + "\\*.zip")
for filename in fileList:
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(aimFolder)

### read the shapefile        
shapeFileList = glob.glob(aimFolder + "\\*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)
### merge the file into one
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf_2000 = gdf[['geometry']].dissolve().set_crs(epsg = 4326)
gdf_2000['hidhPopDensity'] = 1

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")

### 2000
with2000HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin(gdf_2000)
dist2000HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin_nearest(gdf_2000, distance_col = "dist")
with2000HighPopDensity = pd.DataFrame(with2000HighPopDensity.drop(columns='geometry')).set_index('G04c_001')
with2000HighPopDensity['hidhPopDensity'] = 1
with2000HighPopDensity = with2000HighPopDensity.drop(columns='index_right')
dist2000HighPopDensity = pd.DataFrame(dist2000HighPopDensity.drop(columns=['index_right', 'geometry'])).set_index('G04c_001')
HighPopDensity2000 = pd.concat([dist2000HighPopDensity, with2000HighPopDensity], axis=1)
HighPopDensity2000 = HighPopDensity2000.fillna(0)
HighPopDensity2000['year'] = 2000
HighPopDensity2000.reset_index(inplace = True)
HighPopDensity2000 = HighPopDensity2000.set_index(['G04c_001', 'year'])

### 2005
### read the shapefile     
aimFolder = "F:\\17_Article\\01_Data\\06_HighDensityPopulation\\A16-05_GML"   
shapeFileList = glob.glob(aimFolder + "\\*.shp")
gdpFileArray = []
for shapeFileName in shapeFileList:
    gdpFile = gpd.read_file(shapeFileName)
    gdpFileArray.append(gdpFile)
### merge the file into one
gdf = gpd.GeoDataFrame(pd.concat(gdpFileArray))
gdf_2005 = gdf[['geometry']].dissolve().set_crs(epsg = 4326)

with2005HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin(gdf_2005)
dist2005HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin_nearest(gdf_2005, distance_col = "dist")
with2005HighPopDensity = pd.DataFrame(with2005HighPopDensity.drop(columns='geometry')).set_index('G04c_001')
with2005HighPopDensity['hidhPopDensity'] = 1
with2005HighPopDensity = with2005HighPopDensity.drop(columns='index_right')
dist2005HighPopDensity = pd.DataFrame(dist2005HighPopDensity.drop(columns=['index_right', 'geometry'])).set_index('G04c_001')
HighPopDensity2005 = pd.concat([dist2005HighPopDensity, with2005HighPopDensity], axis=1)
HighPopDensity2005 = HighPopDensity2005.fillna(0)
HighPopDensity2005['year'] = 2005
HighPopDensity2005.reset_index(inplace = True)
HighPopDensity2005 = HighPopDensity2005.set_index(['G04c_001', 'year'])

### 2010
gdf_2010 = gpd.read_file("F:/17_Article/01_Data/06_HighDensityPopulation/A16-10_GML/A16-10_00_DID.shp")
gdf_2010 = gdf_2010[['geometry']].dissolve().to_crs(epsg = 4326)

with2010HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin(gdf_2010)
dist2010HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin_nearest(gdf_2010, distance_col = "dist")
with2010HighPopDensity = pd.DataFrame(with2010HighPopDensity.drop(columns='geometry')).set_index('G04c_001')
with2010HighPopDensity['hidhPopDensity'] = 1
with2010HighPopDensity = with2010HighPopDensity.drop(columns='index_right')
dist2010HighPopDensity = pd.DataFrame(dist2010HighPopDensity.drop(columns=['index_right', 'geometry'])).set_index('G04c_001')
HighPopDensity2010 = pd.concat([dist2010HighPopDensity, with2010HighPopDensity], axis=1)
HighPopDensity2010 = HighPopDensity2010.fillna(0)
HighPopDensity2010['year'] = 2010
HighPopDensity2010.reset_index(inplace = True)
HighPopDensity2010 = HighPopDensity2010.set_index(['G04c_001', 'year'])

### 2015
gdf_2015 = gpd.read_file("F:/17_Article/01_Data/06_HighDensityPopulation/A16-15_GML/A16-15_00_DID.shp")
gdf_2015 = gdf_2015.buffer(0)
gdf_2015 = gpd.GeoDataFrame(geometry = gdf_2015, crs="EPSG:4326")
gdf_2015 = gdf_2015[['geometry']].dissolve().to_crs(epsg = 4326)

with2015HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin(gdf_2015)
dist2015HighPopDensity = coords_extration.set_crs(epsg = 4326).sjoin_nearest(gdf_2015, distance_col = "dist")
with2015HighPopDensity = pd.DataFrame(with2015HighPopDensity.drop(columns='geometry')).set_index('G04c_001')
with2015HighPopDensity['hidhPopDensity'] = 1
with2015HighPopDensity = with2015HighPopDensity.drop(columns='index_right')
dist2015HighPopDensity = pd.DataFrame(dist2015HighPopDensity.drop(columns=['index_right', 'geometry'])).set_index('G04c_001')
HighPopDensity2015 = pd.concat([dist2015HighPopDensity, with2015HighPopDensity], axis=1)
HighPopDensity2015 = HighPopDensity2015.fillna(0)
HighPopDensity2015['year'] = 2015
HighPopDensity2015.reset_index(inplace = True)
HighPopDensity2015 = HighPopDensity2015.set_index(['G04c_001', 'year'])

#### previous code, discarded
### extraction
#coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")

#highDensityShapeFile = gpd.read_file("F:/17_Article/01_Data/06_HighDensityPopulation/A16-15_GML/A16-15_00_DID.shp")
#highDensityShapeFile = highDensityShapeFile.set_crs(epsg = 4326)
#highDensityShapeFile = highDensityShapeFile[['geometry']]
#highDensityShapeFileRepair = highDensityShapeFile.buffer(0)
#highDensityShapeFile = gpd.GeoDataFrame(geometry = highDensityShapeFileRepair, crs="EPSG:4326")
#highDensityShapeFileDissolved = highDensityShapeFile.dissolve()
#highDensityShapeFileDissolved['within'] = 1

#joinShape = coords_extration.sjoin(highDensityShapeFileDissolved)
#joinDistance = coords_extraction.sjoin_nearest(highDensityShapeFileDissolved, distance_col = "dist")
#joinDistance = joinDistance.drop(columns = ["within"]) 

#joinShape = joinShape[["id", "within"]]

#result = pd.merge(joinDistance, joinShape, on='id', how='left')
#result['within'] = result['within'].fillna(0)
#result = result.drop(columns = ["index_right"]) 

HighPopDensity = pd.concat([HighPopDensity2000, HighPopDensity2005,
                            HighPopDensity2010, HighPopDensity2015], axis=0)

HighPopDensity.to_pickle("F:/17_Article/01_Data/98_20yearPickles/07_PopulationDensityClass.pkl")
