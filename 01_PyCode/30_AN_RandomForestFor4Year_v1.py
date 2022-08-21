# -*- coding: utf-8 -*-
"""
#NOTE: this script only works on HPC

Created on Mon Jul 11 13:33:29 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import pandas as pd
import numpy as np
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression


#single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
single_dataset_location = "DP17/98_20yearPickles/"
result_location = "DP17/04_Result/"

log_name = "AccuracyReport0819_log.txt"
### create log file:
f = open(result_location + log_name, "w")
f.close()

bigX = pd.read_csv(single_dataset_location + "99_mergedDataset.csv")
bigX.G04c_001 = bigX.G04c_001.astype("int32")
bigX.year = bigX.year.astype("int32")
bigX = bigX.set_index(['G04c_001', 'year'])
bigX = bigX.fillna(0)
#bigX = bigX.drop(columns='index')

pointLonLatAll = pd.read_csv(single_dataset_location + "98_pointLonLatALL.csv")
pointLonLatAll.G04c_001 = pointLonLatAll.G04c_001.astype("int32")
pointLonLatAll.year = pointLonLatAll.year.astype("int32")
pointLonLatAll = pointLonLatAll.set_index(['G04c_001', 'year'])
bigX = pd.concat([bigX, pointLonLatAll], axis=1)

##### y
realPopDf_Y = pd.read_csv(single_dataset_location + "03_population.csv")
realPopDf_Y.G04c_001 = realPopDf_Y.G04c_001.astype("int32")
realPopDf_Y.year = realPopDf_Y.year.astype("int32")
realPopDf_Y['TotalPopLog'] = np.log(realPopDf_Y['TotalPop'] + 1)
realPopDf_Y['MalePopLog'] = np.log(realPopDf_Y['MalePop'] + 1)
realPopDf_Y['FemalePopLog'] = np.log(realPopDf_Y['FemalePop'] + 1)
realPopDf_Y = realPopDf_Y.set_index(['G04c_001', 'year'])

##### total population
y=realPopDf_Y[['TotalPopLog']]

df_merged = pd.concat([y, bigX], axis=1)
df_merged.shape
df_merged = df_merged.fillna(0)
df_merged = df_merged.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
df_merged.shape

df_merged = df_merged.dropna()
df_merged.shape
X = df_merged.iloc[:, 1:57]
X = X.fillna(0)
y = df_merged.iloc[:, 0:1]

model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model.fit(X, y)

model.oob_score_
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
r2
mae = mean_absolute_error(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
#r = np.corrcoef(np.array(y), np.array(y_pred))
#r = r[0,1]
reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
reg.coef_
reg.intercept_

r2_count = r2_score(np.exp(y), np.exp(y_pred))
r2_count
mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
rmse_count = np.sqrt(mse_count)
reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
reg_count.coef_
reg_count.intercept_

bigX_to_pred = bigX.copy()
bigy_pred = model.predict(bigX_to_pred)
bigX_to_pred['bigy_pred'] = bigy_pred
bigy_pred = bigX_to_pred[['bigy_pred']].copy()
bigy_pred.head()

bigy_pred.to_csv(result_location + "SKlearn_1000tree_total_pop_log.csv")

dump(model, result_location + 'model_1000tree_total_pop_log_allyear.joblib') 

f = open(result_location + log_name, "a")
f.write("Total Year Total pop log OOB rate: " + str(model.oob_score_) + "\n")
f.write("Total Year Total pop log R2 rate: " + str(r2) + "\n")
f.write("Total Year Total pop log MAE rate: " + str(mae) + "\n")
f.write("Total Year Total pop log RMSE rate: " + str(rmse) + "\n")
f.write("Total Year Total pop log intercept: " + str(reg.intercept_) + "\n")
f.write("Total Year Total pop log coefficient: " + str(reg.coef_) + "\n")

f.write("Total Year Total pop count R2 rate: " + str(r2_count) + "\n")
f.write("Total Year Total pop count MAE rate: " + str(mae_count) + "\n")
f.write("Total Year Total pop count RMSE rate: " + str(rmse_count) + "\n")
f.write("Total Year Total pop count intercept: " + str(reg_count.intercept_) + "\n")
f.write("Total Year Total pop count coefficient: " + str(reg_count.coef_) + "\n")
f.write("Total Year Total pop log model Location: " + result_location + 'model_1000tree_total_pop_log_allyear.joblib' + "\n")
f.write("Total Year Total pop log predict result: " + result_location + "SKlearn_1000tree_total_pop_log.csv" + "\n")
f.close()

importances = model.feature_importances_
model_importances = pd.Series(importances, index=X.columns)
model_importances.to_csv(result_location + "Importance_SKlearn_1000tree_total_pop_log.csv")

##### male population
y=realPopDf_Y[['MalePopLog']]

df_merged = pd.concat([y, bigX], axis=1)
df_merged.shape
df_merged = df_merged.fillna(0)
df_merged = df_merged.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
df_merged.shape

df_merged = df_merged.dropna()
X = df_merged.iloc[:, 1:57]
X = X.fillna(0)
y = df_merged.iloc[:, 0:1]

model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model.fit(X, y)

model.oob_score_
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
r2
mae = mean_absolute_error(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
#r = np.corrcoef(np.array(y), np.array(y_pred))
#r = r[0,1]
reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
reg.coef_
reg.intercept_

r2_count = r2_score(np.exp(y), np.exp(y_pred))
r2_count
mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
rmse_count = np.sqrt(mse_count)
reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
reg_count.coef_
reg_count.intercept_

bigy_pred = model.predict(bigX)
bigX_to_pred = bigX.copy()
bigX_to_pred['bigy_pred'] = bigy_pred
bigy_pred = bigX_to_pred[['bigy_pred']].copy()
bigy_pred.head()

result_location = "DP17/04_Result/"
bigy_pred.to_csv(result_location + "SKlearn_1000tree_male_pop_log.csv")
dump(model, result_location + 'model_1000tree_male_pop_log_allyear.joblib') 

f = open(result_location + log_name, "a")
f.write("Total Year Male pop log OOB rate: " + str(model.oob_score_) + "\n")
f.write("Total Year Male pop log R2 rate: " + str(r2) + "\n")
f.write("Total Year Male pop log MAE rate: " + str(mae) + "\n")
f.write("Total Year Male pop log RMSE rate: " + str(rmse) + "\n")
f.write("Total Year Male pop log intercept: " + str(reg.intercept_) + "\n")
f.write("Total Year Male pop log coefficient: " + str(reg.coef_) + "\n")

f.write("Total Year Male pop count R2 rate: " + str(r2_count) + "\n")
f.write("Total Year Male pop count MAE rate: " + str(mae_count) + "\n")
f.write("Total Year Male pop count RMSE rate: " + str(rmse_count) + "\n")
f.write("Total Year Male pop count intercept: " + str(reg_count.intercept_) + "\n")
f.write("Total Year Male pop count coefficient: " + str(reg_count.coef_) + "\n")
f.write("Total Year Male pop log model Location: " + result_location + 'model_1000tree_male_pop_log_allyear.joblib' + "\n")
f.write("Total Year Male pop log predict result: " + result_location + "SKlearn_1000tree_male_pop_log.csv" + "\n")
f.close()

importances = model.feature_importances_
model_importances = pd.Series(importances, index=X.columns)
model_importances.to_csv(result_location + "Importance_SKlearn_1000tree_male_pop_log.csv")


##### female population
y=realPopDf_Y[['FemalePopLog']]

df_merged = pd.concat([y, bigX], axis=1)
df_merged.shape
df_merged = df_merged.fillna(0)
df_merged = df_merged.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
df_merged.shape

df_merged = df_merged.dropna()
X = df_merged.iloc[:, 1:57]
X = X.fillna(0)
y = df_merged.iloc[:, 0:1]

model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model.fit(X, y)

model.oob_score_
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
r2
mae = mean_absolute_error(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
#r = np.corrcoef(np.array(y), np.array(y_pred))
#r = r[0,1]
reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
reg.coef_
reg.intercept_

r2_count = r2_score(np.exp(y), np.exp(y_pred))
r2_count
mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
rmse_count = np.sqrt(mse_count)
reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
reg_count.coef_
reg_count.intercept_

bigy_pred = model.predict(bigX)
bigX_to_pred = bigX.copy()
bigX_to_pred['bigy_pred'] = bigy_pred
bigy_pred = bigX_to_pred[['bigy_pred']].copy()
bigy_pred.head()

result_location = "DP17/04_Result/"
bigy_pred.to_csv(result_location + "SKlearn_1000tree_female_pop_log.csv")
dump(model, result_location + 'model_1000tree_female_pop_log_allyear.joblib') 

f = open(result_location + log_name, "a")
f.write("Total Year Female pop log OOB rate: " + str(model.oob_score_) + "\n")
f.write("Total Year Female pop log R2 rate: " + str(r2) + "\n")
f.write("Total Year Female pop log MAE rate: " + str(mae) + "\n")
f.write("Total Year Female pop log RMSE rate: " + str(rmse) + "\n")
f.write("Total Year Female pop log intercept: " + str(reg.intercept_) + "\n")
f.write("Total Year Female pop log coefficient: " + str(reg.coef_) + "\n")

f.write("Total Year Female pop count R2 rate: " + str(r2_count) + "\n")
f.write("Total Year Female pop count MAE rate: " + str(mae_count) + "\n")
f.write("Total Year Female pop count RMSE rate: " + str(rmse_count) + "\n")
f.write("Total Year Female pop count intercept: " + str(reg_count.intercept_) + "\n")
f.write("Total Year Female pop count coefficient: " + str(reg_count.coef_) + "\n")
f.write("Total Year Female pop log model Location: " + result_location + 'model_1000tree_female_pop_log_allyear.joblib' + "\n")
f.write("Total Year Female pop log predict result: " + result_location + "SKlearn_1000tree_female_pop_log.csv" + "\n")
f.close()

importances = model.feature_importances_
model_importances = pd.Series(importances, index=X.columns)
model_importances.to_csv(result_location + "Importance_SKlearn_1000tree_female_pop_log.csv")
