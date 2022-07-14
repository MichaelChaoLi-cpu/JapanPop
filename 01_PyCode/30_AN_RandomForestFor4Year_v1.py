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
from sklearn.metrics import r2_score
from joblib import dump
from sklearn.model_selection import train_test_split

#single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
single_dataset_location = "DP17/98_20yearPickles/"
result_location = "DP17/04_Result/"

bigX = pd.read_csv(single_dataset_location + "99_mergedDataset.csv")
bigX.G04c_001 = bigX.G04c_001.astype("int32")
bigX.year = bigX.year.astype("int32")
bigX = bigX.set_index(['G04c_001', 'year'])
bigX = bigX.fillna(0)

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

df_merged = pd.merge(y, bigX, on = ['G04c_001', 'year'], how='inner')
df_merged.shape

df_merged = df_merged.dropna()
df_merged.shape
X = df_merged.iloc[:, 1:54]
X = X.fillna(0)
y = df_merged.iloc[:, 0:1]

model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model.fit(X, y)

model.oob_score_
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
r2

bigX_to_pred = bigX.copy()
bigy_pred = model.predict(bigX_to_pred)
bigX_to_pred['bigy_pred'] = bigy_pred
bigy_pred = bigX_to_pred[['bigy_pred']].copy()
bigy_pred.head()

bigy_pred.to_csv(result_location + "SKlearn_1000tree_total_pop_log.csv")

dump(model, result_location + 'model_1000tree_total_pop_log_allyear.joblib') 

### create log file:
f = open(result_location + "log.txt", "w")
f.close()

f = open(result_location + "log.txt", "a")
f.write("Total Year Total pop log OOB rate: " + str(model.oob_score_) + "\n")
f.write("Total Year Total pop log R2 rate: " + str(r2) + "\n")
f.write("Total Year Total pop log model Location: " + result_location + 'model_1000tree_total_pop_log_allyear.joblib' + "\n")
f.write("Total Year Total pop log predict result: " + result_location + "SKlearn_1000tree_total_pop_log.csv" + "\n")
f.close()

# cross validation
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, train_size = 0.8,
                                                random_state=1)
model_cv = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_cv.fit(Xtrain, ytrain)
ytest_cv = model_cv.predict(Xtest)

r2_cv = r2_score(ytest, ytest_cv)
r2_cv

f = open(result_location + "log.txt", "a")
f.write("Total Year Total pop log CV R2 rate: " + str(r2_cv) + "\n")
f.close()

#### cross year 
#### except 2005
X_except2005 = X.query("year != 2005")
X_except2005.head()
X_2005 = X.query("year == 2005")
X_2005.head()
y_except2005 = y.query("year != 2005")
y_except2005.head()
y_2005 = y.query("year == 2005")
y_2005.head()
model_except_2005 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2005.fit(X_except2005, y_except2005)
y_pred2005 = model_except_2005.predict(X_2005)
r2_cv_2005 = r2_score(y_2005, y_pred2005)
r2_cv_2005
f = open(result_location + "log.txt", "a")
f.write("Total Year Total pop log CV R2 rate 2005: " + str(r2_cv_2005) + "\n")
f.close()
model_except_2005.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Total pop log OOB rate 2005: " + str(model_except_2005.oob_score_) + "\n")
f.close()

#### except 2010
X_except2010 = X.query("year != 2010")
X_except2010.head()
X_2010 = X.query("year == 2010")
X_2010.head()
y_except2010 = y.query("year != 2010")
y_except2010.head()
y_2010 = y.query("year == 2010")
y_2010.head()
model_except_2010 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2010.fit(X_except2010, y_except2010)
y_pred2010 = model_except_2010.predict(X_2010)
r2_cv_2010 = r2_score(y_2010, y_pred2010)
r2_cv_2010
model_except_2010.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Total pop log CV R2 rate 2010: " + str(r2_cv_2010) + "\n")
f.write("Total Year Total pop log OOB rate 2010: " + str(model_except_2010.oob_score_) + "\n")
f.close()

#### except 2015
X_except2015 = X.query("year != 2015")
X_except2015.head()
X_2015 = X.query("year == 2015")
X_2015.head()
y_except2015 = y.query("year != 2015")
y_except2015.head()
y_2015 = y.query("year == 2015")
y_2015.head()
model_except_2015 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2015.fit(X_except2015, y_except2015)
y_pred2015 = model_except_2015.predict(X_2015)
r2_cv_2015 = r2_score(y_2015, y_pred2015)
r2_cv_2015
model_except_2015.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Total pop log CV R2 rate 2015: " + str(r2_cv_2015) + "\n")
f.write("Total Year Total pop log OOB rate 2015: " + str(model_except_2015.oob_score_) + "\n")
f.close()

##### male population
y=realPopDf_Y[['MalePopLog']]

df_merged = pd.merge(y, bigX, on = ['G04c_001', 'year'], how='inner')
df_merged = df_merged.dropna()
X = df_merged.iloc[:, 1:54]
X = X.fillna(0)
y = df_merged.iloc[:, 0:1]

model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model.fit(X, y)

model.oob_score_
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
r2

bigy_pred = model.predict(bigX)
bigX_to_pred = bigX.copy()
bigX_to_pred['bigy_pred'] = bigy_pred
bigy_pred = bigX_to_pred[['bigy_pred']].copy()
bigy_pred.head()

result_location = "DP17/04_Result/"
bigy_pred.to_csv(result_location + "SKlearn_1000tree_male_pop_log.csv")
dump(model, result_location + 'model_1000tree_male_pop_log_allyear.joblib') 

f = open(result_location + "log.txt", "a")
f.write("\n##### Male Prediction\n")
f.write("Total Year Male pop log OOB rate: " + str(model.oob_score_) + "\n")
f.write("Total Year Male pop log R2 rate: " + str(r2) + "\n")
f.write("Total Year Male pop log model Location: " + result_location + 'model_1000tree_male_pop_log_allyear.joblib' + "\n")
f.write("Total Year Male pop log predict result: " + result_location + "SKlearn_1000tree_male_pop_log.csv" + "\n")
f.close()

# cross validation
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, train_size = 0.8,
                                                random_state=1)
model_cv = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_cv.fit(Xtrain, ytrain)
ytest_cv = model_cv.predict(Xtest)

r2_cv = r2_score(ytest, ytest_cv)
r2_cv

f = open(result_location + "log.txt", "a")
f.write("Total Year Male pop log CV R2 rate: " + str(r2_cv) + "\n")
f.close()

#### cross year 
#### except 2005
X_except2005 = X.query("year != 2005")
X_2005 = X.query("year == 2005")
y_except2005 = y.query("year != 2005")
y_2005 = y.query("year == 2005")
model_except_2005 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2005.fit(X_except2005, y_except2005)
y_pred2005 = model_except_2005.predict(X_2005)
r2_cv_2005 = r2_score(y_2005, y_pred2005)
r2_cv_2005
model_except_2005.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Male pop log CV R2 rate 2005: " + str(r2_cv_2005) + "\n")
f.write("Total Year Male pop log OOB rate 2005: " + str(model_except_2005.oob_score_) + "\n")
f.close()

#### except 2010
X_except2010 = X.query("year != 2010")
X_2010 = X.query("year == 2010")
y_except2010 = y.query("year != 2010")
y_2010 = y.query("year == 2010")
model_except_2010 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2010.fit(X_except2010, y_except2010)
y_pred2010 = model_except_2010.predict(X_2010)
r2_cv_2010 = r2_score(y_2010, y_pred2010)
r2_cv_2010
model_except_2010.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Male pop log CV R2 rate 2010: " + str(r2_cv_2010) + "\n")
f.write("Total Year Male pop log OOB rate 2010: " + str(model_except_2010.oob_score_) + "\n")
f.close()

#### except 2015
X_except2015 = X.query("year != 2015")
X_2015 = X.query("year == 2015")
y_except2015 = y.query("year != 2015")
y_2015 = y.query("year == 2015")
model_except_2015 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2015.fit(X_except2015, y_except2015)
y_pred2015 = model_except_2015.predict(X_2015)
r2_cv_2015 = r2_score(y_2015, y_pred2015)
r2_cv_2015
model_except_2015.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Male pop log CV R2 rate 2015: " + str(r2_cv_2015) + "\n")
f.write("Total Year Male pop log OOB rate 2015: " + str(model_except_2015.oob_score_) + "\n")
f.close()

##### female population
y=realPopDf_Y[['FemalePopLog']]

df_merged = pd.merge(y, bigX, on = ['G04c_001', 'year'], how='inner')
df_merged = df_merged.dropna()
X = df_merged.iloc[:, 1:54]
X = X.fillna(0)
y = df_merged.iloc[:, 0:1]

model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model.fit(X, y)

model.oob_score_
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
r2

bigy_pred = model.predict(bigX)
bigX_to_pred = bigX.copy()
bigX_to_pred['bigy_pred'] = bigy_pred
bigy_pred = bigX_to_pred[['bigy_pred']].copy()
bigy_pred.head()

result_location = "DP17/04_Result/"
bigy_pred.to_csv(result_location + "SKlearn_1000tree_female_pop_log.csv")
dump(model, result_location + 'model_1000tree_female_pop_log_allyear.joblib') 

f = open(result_location + "log.txt", "a")
f.write("\n##### Female Prediction\n")
f.write("Total Year Female pop log OOB rate: " + str(model.oob_score_) + "\n")
f.write("Total Year Female pop log R2 rate: " + str(r2) + "\n")
f.write("Total Year Female pop log model Location: " + result_location + 'model_1000tree_male_pop_log_allyear.joblib' + "\n")
f.write("Total Year Female pop log predict result: " + result_location + "SKlearn_1000tree_male_pop_log.csv" + "\n")
f.close()

# cross validation
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, train_size = 0.8,
                                                random_state=1)
model_cv = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_cv.fit(Xtrain, ytrain)
ytest_cv = model_cv.predict(Xtest)

r2_cv = r2_score(ytest, ytest_cv)
r2_cv

f = open(result_location + "log.txt", "a")
f.write("Total Year Female pop log CV R2 rate: " + str(r2_cv) + "\n")
f.close()

#### cross year 
#### except 2005
X_except2005 = X.query("year != 2005")
X_2005 = X.query("year == 2005")
y_except2005 = y.query("year != 2005")
y_2005 = y.query("year == 2005")
model_except_2005 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2005.fit(X_except2005, y_except2005)
y_pred2005 = model_except_2005.predict(X_2005)
r2_cv_2005 = r2_score(y_2005, y_pred2005)
r2_cv_2005
model_except_2005.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Female pop log CV R2 rate 2005: " + str(r2_cv_2005) + "\n")
f.write("Total Year Female pop log OOB rate 2005: " + str(model_except_2005.oob_score_) + "\n")
f.close()

#### except 2010
X_except2010 = X.query("year != 2010")
X_2010 = X.query("year == 2010")
y_except2010 = y.query("year != 2010")
y_2010 = y.query("year == 2010")
model_except_2010 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2010.fit(X_except2010, y_except2010)
y_pred2010 = model_except_2010.predict(X_2010)
r2_cv_2010 = r2_score(y_2010, y_pred2010)
r2_cv_2010
model_except_2010.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Female pop log CV R2 rate 2010: " + str(r2_cv_2010) + "\n")
f.write("Total Year Female pop log OOB rate 2010: " + str(model_except_2010.oob_score_) + "\n")
f.close()

#### except 2015
X_except2015 = X.query("year != 2015")
X_2015 = X.query("year == 2015")
y_except2015 = y.query("year != 2015")
y_2015 = y.query("year == 2015")
model_except_2015 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
model_except_2015.fit(X_except2015, y_except2015)
y_pred2015 = model_except_2015.predict(X_2015)
r2_cv_2015 = r2_score(y_2015, y_pred2015)
r2_cv_2015
model_except_2015.oob_score_
f = open(result_location + "log.txt", "a")
f.write("Total Year Female pop log CV R2 rate 2015: " + str(r2_cv_2015) + "\n")
f.write("Total Year Female pop log OOB rate 2015: " + str(model_except_2015.oob_score_) + "\n")
f.close()
