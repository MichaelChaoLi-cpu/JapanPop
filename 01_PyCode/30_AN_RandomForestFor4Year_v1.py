# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:33:29 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import pandas as pd
import numpy as np
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor

#single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
single_dataset_location = "DP17/98_20yearPickles/"

bigX = pd.read_csv(single_dataset_location + "99_mergedDataset.csv")
bigX.G04c_001 = bigX.G04c_001.astype("int32")
bigX.year = bigX.year.astype("int32")
bigX = bigX.set_index(['G04c_001', 'year'])

##### y
realPopDf_Y = pd.read_csv(single_dataset_location + "03_population.csv")
realPopDf_Y.G04c_001 = realPopDf_Y.G04c_001.astype("int32")
realPopDf_Y.year = realPopDf_Y.year.astype("int32")
realPopDf_Y['TotalPopLog'] = np.log(realPopDf_Y['TotalPop'] + 1)
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

model.oob_score_

y_pred = model.predict(X)
from sklearn.metrics import r2_score
r2 = r2_score(y, y_pred)
r2

bigX_to_pred = bigX.copy()
bigX_to_pred = bigX_to_pred.fillna(0)

bigy_pred = model.predict(bigX_to_pred)
bigX_to_pred['bigy_pred'] = bigy_pred
bigy_pred = bigX_to_pred[['bigy_pred']].copy()
bigy_pred.head()

result_location = "DP17/04_Result/"
bigy_pred.to_csv(result_location + "SKlearn_1000tree_total_pop_log.csv")

from joblib import dump
dump(model, result_location + 'model_1000tree_total_pop_log_allyear.joblib') 

f = open(result_location + "log.txt", "a")
f.close()