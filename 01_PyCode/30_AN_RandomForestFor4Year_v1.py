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
single_dataset_location = "DP17/98_20yearPickles/"

bigX = pd.read_csv(single_dataset_location + "99_mergedDataset.csv")
bigX.G04c_001 = bigX.G04c_001.astype("int32")
bigX.year = bigX.year.astype("int32")
bigX = bigX.set_index(['G04c_001', 'year'])

##### y
realPopDf_Y = pd.read_csv(single_dataset_location + "03_population.csv")
realPopDf_Y.G04c_001 = realPopDf_Y.G04c_001.astype("int32")
realPopDf_Y.year = realPopDf_Y.year.astype("int32")
realPopDf_Y['TotalPopLog'] = np.log(realPopDf_Y['TotalPop'])
realPopDf_Y = realPopDf_Y.set_index(['G04c_001', 'year'])

y=realPopDf_Y[['TotalPopLog']]

df_merged = pd.merge(y, bigX, on = ['G04c_001', 'year'], how='inner')
df_merged.shape

df_merged = df_merged.dropna()
df_merged.shape
X = df_merged.iloc[:, 1:54]
y = df_merged.iloc[:, 0:1]

model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model.fit(X, y)