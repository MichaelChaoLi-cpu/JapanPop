# -*- coding: utf-8 -*-
"""
merge final dataset

Created on Mon Jul 11 10:02:33 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import geopandas as gpd
import glob
import pandas as pd
import numpy as np

single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"

##### y
realPopDf_Y = pd.read_pickle(single_dataset_location + "03_population.pkl")

##### X G04c_001 int32 year int32
landCoverDf = pd.read_pickle(single_dataset_location + "01_LandCoverClassDistance.pkl") 
remoteSensingDf = pd.read_pickle(single_dataset_location + "02_NtlNppPrecTemp.pkl")
bigX = pd.concat([landCoverDf, remoteSensingDf], axis=1)
del landCoverDf
del remoteSensingDf
bigX.reset_index(inplace=True)
bigX.G04c_001 = bigX.G04c_001.astype('int32')
bigX.year = bigX.year.astype('int32')
bigX = bigX.set_index(['G04c_001', 'year'])

# not full
roadLengthDf = pd.read_pickle(single_dataset_location + "04_RoadLength.pkl")
roadLengthDf = pd.DataFrame(roadLengthDf)
# 02 03 04 10
# get 02 to 01
roadLengthDf2002 = roadLengthDf.query("year == 2002") 
roadLengthDf2001 = roadLengthDf2002.rename(index={2002:2001})

roadLengthDf2003 = roadLengthDf.query("year == 2003") 

# get 04 to 05 06 07
roadLengthDf2004 = roadLengthDf.query("year == 2004") 
roadLengthDf2005 = roadLengthDf2004.rename(index={2004:2005})
roadLengthDf2006 = roadLengthDf2004.rename(index={2004:2006})
roadLengthDf2007 = roadLengthDf2004.rename(index={2004:2007})

# get 10 to 08 09 11 - 20
roadLengthDf2010 = roadLengthDf.query("year == 2010") 
roadLengthDf2008 = roadLengthDf2010.rename(index={2010:2008})
roadLengthDf2009 = roadLengthDf2010.rename(index={2010:2009})
roadLengthDf2011 = roadLengthDf2010.rename(index={2010:2011})
roadLengthDf2012 = roadLengthDf2010.rename(index={2010:2012})
roadLengthDf2013 = roadLengthDf2010.rename(index={2010:2013})
roadLengthDf2014 = roadLengthDf2010.rename(index={2010:2014})
roadLengthDf2015 = roadLengthDf2010.rename(index={2010:2015})
roadLengthDf2016 = roadLengthDf2010.rename(index={2010:2016})
roadLengthDf2017 = roadLengthDf2010.rename(index={2010:2017})
roadLengthDf2018 = roadLengthDf2010.rename(index={2010:2018})
roadLengthDf2019 = roadLengthDf2010.rename(index={2010:2019})
roadLengthDf2020 = roadLengthDf2010.rename(index={2010:2020})

roadLengthDf = pd.concat([roadLengthDf2001, roadLengthDf2002, roadLengthDf2003, 
                          roadLengthDf2004, roadLengthDf2005, roadLengthDf2006, 
                          roadLengthDf2007, roadLengthDf2008, roadLengthDf2009, 
                          roadLengthDf2010, roadLengthDf2011, roadLengthDf2012, 
                          roadLengthDf2013, roadLengthDf2014, roadLengthDf2015, 
                          roadLengthDf2016, roadLengthDf2017, roadLengthDf2018, 
                          roadLengthDf2019, roadLengthDf2020 ])

del roadLengthDf2001, roadLengthDf2002, roadLengthDf2003
del roadLengthDf2004, roadLengthDf2005, roadLengthDf2006
del roadLengthDf2007, roadLengthDf2008, roadLengthDf2009 
del roadLengthDf2010, roadLengthDf2011, roadLengthDf2012 
del roadLengthDf2013, roadLengthDf2014, roadLengthDf2015 
del roadLengthDf2016, roadLengthDf2017, roadLengthDf2018 
del roadLengthDf2019, roadLengthDf2020

roadLengthDf.reset_index(inplace=True)
roadLengthDf.G04c_001 = roadLengthDf.G04c_001.astype('int32')
roadLengthDf.year = roadLengthDf.year.astype('int32')
roadLengthDf = roadLengthDf.set_index(['G04c_001', 'year'])

bigX = pd.merge(bigX, roadLengthDf, on = ['G04c_001', 'year'], how='left')
del roadLengthDf

elevationSlopeDf = pd.read_pickle(single_dataset_location + "05_ElevationSlope.pkl")
elevationSlopeDf.reset_index(inplace=True)
elevationSlopeDf.G04c_001 = elevationSlopeDf.G04c_001.astype('int32')
elevationSlopeDf.year = elevationSlopeDf.year.astype('int32')
elevationSlopeDf = elevationSlopeDf.set_index(['G04c_001', 'year'])

elevationSlopeDfAll = pd.concat([
    elevationSlopeDf.rename(index={2011:2001}), elevationSlopeDf.rename(index={2011:2002}),
    elevationSlopeDf.rename(index={2011:2003}), elevationSlopeDf.rename(index={2011:2004}),
    elevationSlopeDf.rename(index={2011:2005}), elevationSlopeDf.rename(index={2011:2006}),
    elevationSlopeDf.rename(index={2011:2007}), elevationSlopeDf.rename(index={2011:2008}),
    elevationSlopeDf.rename(index={2011:2009}), elevationSlopeDf.rename(index={2011:2010}),
    elevationSlopeDf.rename(index={2011:2011}), elevationSlopeDf.rename(index={2011:2012}),
    elevationSlopeDf.rename(index={2011:2013}), elevationSlopeDf.rename(index={2011:2014}),
    elevationSlopeDf.rename(index={2011:2015}), elevationSlopeDf.rename(index={2011:2016}),
    elevationSlopeDf.rename(index={2011:2017}), elevationSlopeDf.rename(index={2011:2018}),
    elevationSlopeDf.rename(index={2011:2019}), elevationSlopeDf.rename(index={2011:2020})
                                 ])
bigX = pd.concat([bigX, elevationSlopeDfAll], axis=1)
del elevationSlopeDfAll
del elevationSlopeDf

riverDist = pd.read_pickle(single_dataset_location + "05_RiverDist.pkl")
riverDist.reset_index(inplace=True)
riverDist.G04c_001 = riverDist.G04c_001.astype('int32')
riverDist.year = riverDist.year.astype('int32')
riverDist = riverDist.set_index(['G04c_001', 'year'])

riverDistAll = pd.concat([
    riverDist.rename(index={2010:2001}), riverDist.rename(index={2010:2002}),
    riverDist.rename(index={2010:2003}), riverDist.rename(index={2010:2004}),
    riverDist.rename(index={2010:2005}), riverDist.rename(index={2010:2006}),
    riverDist.rename(index={2010:2007}), riverDist.rename(index={2010:2008}),
    riverDist.rename(index={2010:2009}), riverDist.rename(index={2010:2010}),
    riverDist.rename(index={2010:2011}), riverDist.rename(index={2010:2012}),
    riverDist.rename(index={2010:2013}), riverDist.rename(index={2010:2014}),
    riverDist.rename(index={2010:2015}), riverDist.rename(index={2010:2016}),
    riverDist.rename(index={2010:2017}), riverDist.rename(index={2010:2018}),
    riverDist.rename(index={2010:2019}), riverDist.rename(index={2010:2020})
                                 ])
bigX = pd.concat([bigX, riverDistAll], axis=1)
del riverDistAll
del riverDist

CoastLine = pd.read_pickle(single_dataset_location + "06_CoastLine.pkl")
CoastLine.reset_index(inplace=True)
CoastLine.G04c_001 = CoastLine.G04c_001.astype('int32')
CoastLine.year = CoastLine.year.astype('int32')
CoastLine = CoastLine.set_index(['G04c_001', 'year'])

CoastLineAll = pd.concat([
    CoastLine.rename(index={2010:2001}), CoastLine.rename(index={2010:2002}),
    CoastLine.rename(index={2010:2003}), CoastLine.rename(index={2010:2004}),
    CoastLine.rename(index={2010:2005}), CoastLine.rename(index={2010:2006}),
    CoastLine.rename(index={2010:2007}), CoastLine.rename(index={2010:2008}),
    CoastLine.rename(index={2010:2009}), CoastLine.rename(index={2010:2010}),
    CoastLine.rename(index={2010:2011}), CoastLine.rename(index={2010:2012}),
    CoastLine.rename(index={2010:2013}), CoastLine.rename(index={2010:2014}),
    CoastLine.rename(index={2010:2015}), CoastLine.rename(index={2010:2016}),
    CoastLine.rename(index={2010:2017}), CoastLine.rename(index={2010:2018}),
    CoastLine.rename(index={2010:2019}), CoastLine.rename(index={2010:2020})
                                 ])
bigX = pd.concat([bigX, CoastLineAll], axis=1)
del CoastLineAll
del CoastLine

popHighDensity = pd.read_pickle(single_dataset_location + "07_PopulationDensityClass.pkl")
popHighDensity.reset_index(inplace=True)
popHighDensity.G04c_001 = popHighDensity.G04c_001.astype('int32')
popHighDensity.year = popHighDensity.year.astype('int32')
popHighDensity = popHighDensity.set_index(['G04c_001', 'year'])

popHighDensity2000 = popHighDensity.query("year == 2000") 
popHighDensity2005 = popHighDensity.query("year == 2005") 
popHighDensity2010 = popHighDensity.query("year == 2010") 
popHighDensity2015 = popHighDensity.query("year == 2015") 
popHighDensityAll = pd.concat([
    popHighDensity2000.rename(index={2000:2001}), popHighDensity2000.rename(index={2000:2002}),
    popHighDensity2000.rename(index={2000:2003}), popHighDensity2005.rename(index={2005:2004}),
    popHighDensity2005.rename(index={2005:2005}), popHighDensity2005.rename(index={2005:2006}),
    popHighDensity2005.rename(index={2005:2007}), popHighDensity2005.rename(index={2005:2008}),
    popHighDensity2010.rename(index={2010:2009}), popHighDensity2010.rename(index={2010:2010}),
    popHighDensity2010.rename(index={2010:2011}), popHighDensity2010.rename(index={2010:2012}),
    popHighDensity2010.rename(index={2010:2013}), popHighDensity2015.rename(index={2015:2014}),
    popHighDensity2015.rename(index={2015:2015}), popHighDensity2015.rename(index={2015:2016}),
    popHighDensity2015.rename(index={2015:2017}), popHighDensity2015.rename(index={2015:2018}),
    popHighDensity2015.rename(index={2015:2019}), popHighDensity2015.rename(index={2015:2020})
                                 ])
bigX = pd.concat([bigX, popHighDensityAll], axis=1)
del popHighDensityAll, popHighDensity
del popHighDensity2000, popHighDensity2005, popHighDensity2010, popHighDensity2015

distancePoi = pd.read_pickle(single_dataset_location + "08_distancePoi.pkl")
distancePoi.reset_index(inplace=True)
distancePoi.G04c_001 = distancePoi.G04c_001.astype('int32')
distancePoi.year = distancePoi.year.astype('int32')
distancePoi = distancePoi.set_index(['G04c_001', 'year'])

distancePoiAll = pd.concat([
    distancePoi.rename(index={2006:2001}), distancePoi.rename(index={2006:2002}),
    distancePoi.rename(index={2006:2003}), distancePoi.rename(index={2006:2004}),
    distancePoi.rename(index={2006:2005}), distancePoi.rename(index={2006:2006}),
    distancePoi.rename(index={2006:2007}), distancePoi.rename(index={2006:2008}),
    distancePoi.rename(index={2006:2009}), distancePoi.rename(index={2006:2010}),
    distancePoi.rename(index={2006:2011}), distancePoi.rename(index={2006:2012}),
    distancePoi.rename(index={2006:2013}), distancePoi.rename(index={2006:2014}),
    distancePoi.rename(index={2006:2015}), distancePoi.rename(index={2006:2016}),
    distancePoi.rename(index={2006:2017}), distancePoi.rename(index={2006:2018}),
    distancePoi.rename(index={2006:2019}), distancePoi.rename(index={2006:2020})
                                 ])
bigX = pd.concat([bigX, distancePoiAll], axis=1)
del distancePoiAll, distancePoi

distRailwayStation = pd.read_pickle(single_dataset_location + "09_distRailwayStation.pkl")
distRailwayStation.reset_index(inplace=True)
distRailwayStation.G04c_001 = distRailwayStation.G04c_001.astype('int32')
distRailwayStation.year = distRailwayStation.year.astype('int32')
distRailwayStation = distRailwayStation.set_index(['G04c_001', 'year'])

distRailwayStation2005 = distRailwayStation.query("year == 2005") 
distRailwayStation2008 = distRailwayStation.query("year == 2008") 
distRailwayStation2011 = distRailwayStation.query("year == 2011") 

distRailwayStationAll = pd.concat([
    distRailwayStation, distRailwayStation2005.rename(index={2005:2001}),
    distRailwayStation2005.rename(index={2005:2002}), distRailwayStation2005.rename(index={2005:2003}),
    distRailwayStation2005.rename(index={2005:2004}), distRailwayStation2008.rename(index={2008:2009}),
    distRailwayStation2011.rename(index={2011:2010})
    ])

bigX = pd.concat([bigX, distRailwayStationAll], axis=1)
del distRailwayStationAll, distRailwayStation
del distRailwayStation2005, distRailwayStation2008, distRailwayStation2011

bigX.roadLength = bigX.roadLength.fillna(0)
bigX.to_pickle("F:/17_Article/01_Data/98_20yearPickles/99_mergedDataset.pkl")

#### make csv to supercomputer
#####
bigX.to_csv("F:/17_Article/01_Data/98_20yearPickles/99_mergedDataset.csv")
##### y
realPopDf_Y = pd.read_pickle(single_dataset_location + "03_population.pkl")
