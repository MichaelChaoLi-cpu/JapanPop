# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 13:29:59 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import geopandas as gpd
import pandas as pd

### extraction
coords_extration = gpd.read_file("F:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")


pointOfInterestDf =  gpd.read_file("F:\\17_Article\\01_Data\\07_PointOfInterest\\merged2006POI.shp")
pointOfInterestDf = pointOfInterestDf[['P02_001', 'P02_002', 'P02_003', 'geometry']]

pointOfInterestDf['POItype'] = pointOfInterestDf['P02_003'].astype('int')//1000
pointOfInterestDf = pointOfInterestDf[['POItype', 'geometry']]

POImuseum = pointOfInterestDf[pointOfInterestDf.POItype == 3]
POImuseum = POImuseum[['geometry']].dissolve().set_crs(epsg = 4326)

distPOImuseum = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POImuseum, distance_col = "POImuseumDist")

POIgovernment = pointOfInterestDf[pointOfInterestDf.POItype == 12]
POIgovernment = POIgovernment[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIgovernment = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIgovernment, distance_col = "POIgovernmentDist")

POIpolice = pointOfInterestDf[pointOfInterestDf.POItype == 13]
POIpolice = POIpolice[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIpolice = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIpolice, distance_col = "POIpoliceDist")

POIfireStation = pointOfInterestDf[pointOfInterestDf.POItype == 13]
POIfireStation = POIfireStation[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIfireStation = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIfireStation, distance_col = "POIfireStationDist")
