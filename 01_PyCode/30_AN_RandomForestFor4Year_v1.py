# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:33:29 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor

single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"

bigX = pd.read_pickle(single_dataset_location + "99_mergedDataset.pkl")

##### y
realPopDf_Y = pd.read_pickle(single_dataset_location + "03_population.pkl")
realPopDf_Y.to_pickle(single_dataset_location + "03_population.pkl", protocol = 1)
realPopDf_Y['TotalPop_log'] = np.log(realPopDf_Y['TotalPop'] + 1)
y=realPopDf_Y[['TotalPop_log']]

df_merged = pd.merge(y, bigX, on = ['G04c_001', 'year'], how='inner')
