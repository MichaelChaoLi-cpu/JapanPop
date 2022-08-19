# -*- coding: utf-8 -*-
"""
Point of interest

year: 2006

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

POIpolice = pointOfInterestDf[pointOfInterestDf.POItype == 14]
POIpolice = POIpolice[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIpolice = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIpolice, distance_col = "POIpoliceDist")

POIfireStation = pointOfInterestDf[pointOfInterestDf.POItype == 15]
POIfireStation = POIfireStation[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIfireStation = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIfireStation, distance_col = "POIfireStationDist")

POIschool = pointOfInterestDf[pointOfInterestDf.POItype == 16]
POIschool = POIschool[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIschool = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIschool, distance_col = "POIschoolDist")

POIhospital = pointOfInterestDf[pointOfInterestDf.POItype == 17]
POIhospital = POIhospital[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIhospital = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIhospital, distance_col = "POIhospitalDist")

POIpost = pointOfInterestDf[pointOfInterestDf.POItype == 18]
POIpost = POIpost[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIpost = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIpost, distance_col = "POIpostDist")

POIdisable = pointOfInterestDf[pointOfInterestDf.POItype == 19]
POIdisable = POIpost[['geometry']].dissolve().set_crs(epsg = 4326)

distPOIdisable = coords_extration.set_crs(epsg = 4326).sjoin_nearest(POIdisable, distance_col = "POIdisableDist")

### unified the function
distPOImuseum = pd.DataFrame(distPOImuseum.drop(columns=['geometry', 'index_right'])) 
distPOImuseum['year'] = 2006 
distPOImuseum = distPOImuseum.set_index(['G04c_001', 'year'])

distPOIgovernment = pd.DataFrame(distPOIgovernment.drop(columns=['geometry', 'index_right'])) 
distPOIgovernment['year'] = 2006 
distPOIgovernment = distPOIgovernment.set_index(['G04c_001', 'year'])

distPOIpolice = pd.DataFrame(distPOIpolice.drop(columns=['geometry', 'index_right'])) 
distPOIpolice['year'] = 2006 
distPOIpolice = distPOIpolice.set_index(['G04c_001', 'year'])

distPOIschool = pd.DataFrame(distPOIschool.drop(columns=['geometry', 'index_right'])) 
distPOIschool['year'] = 2006 
distPOIschool = distPOIschool.set_index(['G04c_001', 'year'])

distPOIhospital = pd.DataFrame(distPOIhospital.drop(columns=['geometry', 'index_right'])) 
distPOIhospital['year'] = 2006 
distPOIhospital = distPOIhospital.set_index(['G04c_001', 'year'])

distPOIpost = pd.DataFrame(distPOIpost.drop(columns=['geometry', 'index_right'])) 
distPOIpost['year'] = 2006 
distPOIpost = distPOIpost.set_index(['G04c_001', 'year'])

distPOIdisable = pd.DataFrame(distPOIdisable.drop(columns=['geometry', 'index_right'])) 
distPOIdisable['year'] = 2006 
distPOIdisable = distPOIdisable.set_index(['G04c_001', 'year'])

distPOI = pd.concat([distPOImuseum, distPOIgovernment, distPOIpolice, distPOIfireStation,
                     distPOIschool, distPOIhospital, distPOIpost, distPOIdisable], axis=1)

distPOI.to_pickle("F:/17_Article/01_Data/98_20yearPickles/08_distancePoi.pkl")
