# -*- coding: utf-8 -*-
"""
Get the Point Class and to Other Classes Distance

Point: Japanese 3rd time Mesh 1 Km centroid

Test Year: 2015

Created on Wed Apr 13 12:08:49 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from scipy.spatial import cKDTree

# make the raster -180 -60 180 90
nx = 4000                                       # number of cells in the x direction
ny = 3750                                     # number of cells in the y direction
xmin = 122.004                                  # x coordinate of lower, left cell center 
ymin = 30.004                                     # y coordinate of lower, left cell center 
xsize = 0.008                                   # extent of cells in x direction
ysize = 0.008                                   # extent of cells in y direction
epsg = 4326                                     # get projection

def addCoord(nx,xmin,xsize,ny,ymin,ysize, epsg): # Michael Pyrcz, March, 2018                      
  # makes a 2D dataframe with coordinates based on GSLIB specification
  coords = np.zeros([nx*ny, 3])
  ixy = 0
  for iy in range(nx):
    for ix in range(ny):
      coords[ixy,1] = xmin + ix*xsize  
      coords[ixy,2] = ymin + iy*ysize 
      coords[ixy,0] = ixy + 1
      ixy = ixy + 1
      
  coords = pd.DataFrame(coords, columns = ["order", "X", "Y"])
  gdf = gpd.GeoDataFrame(coords, geometry = gpd.points_from_xy(coords.X, coords.Y))
  gdf = gdf.set_crs(epsg = epsg)
  return (gdf)

def ckdnearest(gdA, gdB, column_name):

    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name=column_name)
        ], 
        axis=1)

    return gdf
  
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/mesh_center_point.shp")
coords_distance_raster_result = coords_extration.copy()
coords_distance_raster = addCoord(nx,xmin,xsize,ny,ymin,ysize, epsg)


# note: there is no open shrublands

#for type_num in range(16):
type_num = 0
while type_num < 16:
    year = 2015
    
    rasterLocation = "F:/17_Article/01_Data/01_LandCover/LandCoverSingleClass/year_" + str(year) + "_class_"+ str(type_num) +".tif"
    
    rasterFile = rasterio.open(rasterLocation)
    aimPoint = coords_extration
    rasterArray = rasterFile.read(1)
    
    valueArray = []
    for point in aimPoint['geometry']:
        x = point.xy[0][0]
        y = point.xy[1][0]
        row, col = rasterFile.index(x, y)
        valueArray.append(rasterArray[row, col])
        
    valueArray = np.array(valueArray)
    coords_extration['value'] = valueArray
    coords_extration_aim = coords_extration[coords_extration.value == 100]
    coords_extration_aim = coords_extration_aim[['geometry']]
    
    if coords_extration_aim.shape[0] > 0:
        dist = ckdnearest(coords_distance_raster, coords_extration_aim, "dist_class_"+str(type_num))
        dist_column = dist[["dist_class_"+str(type_num)]]
        coords_distance_raster_result["binary_class_"+str(type_num)] = valueArray / 100
        coords_distance_raster_result["dist_class_"+str(type_num)] = dist_column
    else:
        print("class_"+str(type_num)+" is not in japan")
    print("dist_class_"+str(type_num))
    type_num += 1

coords_distance_raster_result.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/00_2015_LandCover_CLASSandDIST.pkl")

