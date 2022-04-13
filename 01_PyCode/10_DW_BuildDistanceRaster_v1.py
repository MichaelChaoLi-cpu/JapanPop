# -*- coding: utf-8 -*-
"""


Created on Wed Apr 13 12:08:49 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import pandas as pd
import geopandas as gpd
import numpy as np

# make the raster -180 -60 180 90
nx = 4000                                       # number of cells in the x direction
ny = 3750                                     # number of cells in the y direction
xmin = 122.0                                  # x coordinate of lower, left cell center 
ymin = 30.0                                     # y coordinate of lower, left cell center 
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
  
coords = addCoord(nx,xmin,xsize,ny,ymin,ysize, epsg)
