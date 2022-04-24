# -*- coding: utf-8 -*-
"""
Source: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N04.html

Year: 2011 (H22)

Created on Sun Apr 24 14:34:10 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd

aimFolder = "F:\\17_Article\\01_Data\\04_Road"

roadShapeFile = gpd.read_file(aimFolder + "\\MeshRoad2011.shp")

roadShapeFile = roadShapeFile[['N04_001', 'N04_056', 'geometry']]
roadShapeFile.N04_056 = roadShapeFile.N04_056.replace('unknown','0').astype("float")
roadShapeFile.N04_001 = roadShapeFile.N04_001.astype('int')

roadShapeFile = roadShapeFile[['N04_001', 'N04_056']]
roadShapeFile.columns = ['id', 'roadDensity']

roadShapeFile.to_pickle("F:/17_Article/01_Data/99_MiddleFileStation/05_roadDensity.pkl")
