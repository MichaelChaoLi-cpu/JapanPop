#NOTE: this script only works on HPC

#### out of memory 
#### 2022/7/30 9:40 test 16 nodes 
#### run 288 cores; 3072GB

import pandas as pd
import numpy as np
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import psutil
import multiprocessing

#single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
single_dataset_location = "DP17/98_20yearPickles/"
result_location = "DP17/04_Result/"

log_name = "CV82_0812.txt"

### create log file:
f = open(result_location + log_name, "w")
f.close()

f = open(result_location + log_name, "a")
f.write("Core:" + str(multiprocessing.cpu_count()) + '\n')
f.write(str(psutil.virtual_memory()) + '\n')
f.close()

def df_mergedPrepare(aimGroup):
    single_dataset_location = "DP17/98_20yearPickles/"
    bigX = pd.read_csv(single_dataset_location + "99_mergedDataset.csv")
    bigX.G04c_001 = bigX.G04c_001.astype("int32")
    bigX.year = bigX.year.astype("int32")
    bigX = bigX.set_index(['G04c_001', 'year'])
    bigX = bigX.fillna(0)
    
    pointLonLatAll = pd.read_csv(single_dataset_location + "98_pointLonLatALL.csv")
    pointLonLatAll.G04c_001 = pointLonLatAll.G04c_001.astype("int32")
    pointLonLatAll.year = pointLonLatAll.year.astype("int32")
    pointLonLatAll = pointLonLatAll.set_index(['G04c_001', 'year'])
    bigX = pd.concat([bigX, pointLonLatAll], axis=1)
    bigX = bigX.drop(columns='index')
    bigX = bigX.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    
    ##### y
    realPopDf_Y = pd.read_csv(single_dataset_location + "03_population.csv")
    realPopDf_Y.G04c_001 = realPopDf_Y.G04c_001.astype("int32")
    realPopDf_Y.year = realPopDf_Y.year.astype("int32")
    realPopDf_Y['TotalPopLog'] = np.log(realPopDf_Y['TotalPop'] + 1)
    realPopDf_Y['MalePopLog'] = np.log(realPopDf_Y['MalePop'] + 1)
    realPopDf_Y['FemalePopLog'] = np.log(realPopDf_Y['FemalePop'] + 1)
    realPopDf_Y = realPopDf_Y.set_index(['G04c_001', 'year'])
    
    selectVariable = aimGroup + 'PopLog'
    ##### total population
    y=realPopDf_Y[[selectVariable]]
    df_merged = pd.concat([y, bigX], axis=1)
    df_merged.shape
    df_merged = df_merged.fillna(0)
    df_merged = df_merged.query("year == 2005 | year == 2010 | year == 2015 | year == 2020")
    
    df_merged.to_csv(single_dataset_location + "00_temp_merge_" + aimGroup + ".csv")


def Mdodel82CV(aimGroup, log_name):
    single_dataset_location = "DP17/98_20yearPickles/"
    result_location = "DP17/04_Result/"
    selectVariable = aimGroup + 'PopLog'
    
    df_merged = pd.read_csv(single_dataset_location + "00_temp_merge_" + aimGroup + ".csv")
    df_merged = df_merged.set_index(['G04c_001', 'year'])
    
    f = open(result_location + log_name, "a")
    f.write("Read Data!\n")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    df_merged = df_merged.dropna()
    df_merged.shape
    X = df_merged.iloc[:, 1:55]
    X = X.fillna(0)
    y = df_merged.iloc[:, 0:1]
    
    # cross validation
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, train_size = 0.8,
                                                    random_state=1)
    
    f = open(result_location + log_name, "a")
    f.write("Before cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    model_cv = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=36)
    model_cv.fit(Xtrain, ytrain)
    
    f = open(result_location + log_name, "a")
    f.write("After cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    ytest_cv = model_cv.predict(Xtest)
    
    DF_cv_3_7 = ytest.copy()
    DF_cv_3_7['y_pred'] = ytest_cv
    DF_cv_3_7.to_csv(result_location + "SKlearn_1000tree_" + selectVariable + "_DF_cv_3_7.csv")
    
    y = ytest
    y_pred = ytest_cv
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
    #r_count = np.corrcoef(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    #r_count = r_count[0,1]
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + log_name, "a")
    f.write("##### Cross-Validation:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    #f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    #f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()

def TemporalCV(aimGroup, log_name):
    single_dataset_location = "DP17/98_20yearPickles/"
    result_location = "DP17/04_Result/"
    selectVariable = aimGroup + 'PopLog'
    
    df_merged = pd.read_csv(single_dataset_location + "00_temp_merge_" + aimGroup + ".csv")
    df_merged = df_merged.set_index(['G04c_001', 'year'])
    
    f = open(result_location + log_name, "a")
    f.write("Read Data!\n")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    df_merged = df_merged.dropna()
    df_merged.shape
    X = df_merged.iloc[:, 1:55]
    X = X.fillna(0)
    y = df_merged.iloc[:, 0:1]
    y_raw = y.copy()
    
    f = open(result_location + log_name, "a")
    f.write("X Y prepared!\n")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    df_merged = None
    
    f = open(result_location + log_name, "a")
    f.write("df_merged=0!\n")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    #### cross year 
    #### except 2005
    X_except2005 = X.query("year != 2005")
    X_except2005.head()
    X_2005 = X.query("year == 2005")
    X_2005.head()
    y_except2005 = y_raw.query("year != 2005")
    y_except2005.head()
    y_2005 = y_raw.query("year == 2005")
    y_2005.head()
    
    f = open(result_location + log_name, "a")
    f.write("Before 2005 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()

    model_except_2005 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
    model_except_2005.fit(X_except2005, y_except2005)
    
    f = open(result_location + log_name, "a")
    f.write("After 2005 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    y_pred2005 = model_except_2005.predict(X_2005)
    
    DF_cv_2005 = y_2005.copy()
    DF_cv_2005['y_pred2005'] = y_pred2005
    DF_cv_2005.to_csv(result_location + "SKlearn_1000tree_" + selectVariable + "_DF_cv_2005.csv")
    DF_cv_2005 = None
    
    y_pred = y_pred2005
    y = y_2005
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
    #r_count = np.corrcoef(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    #r_count = r_count[0,1]
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + log_name, "a")
    f.write("##### Temporal Cross-Validation 2005:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    #f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    #f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()
    
    model_except_2005 = None
    X_except2005 = None
    X_2005 = None
    y_except2005 = None
    y_2005 = None
    
    #### except 2010
    X_except2010 = X.query("year != 2010")
    X_except2010.head()
    X_2010 = X.query("year == 2010")
    X_2010.head()
    y_except2010 = y_raw.query("year != 2010")
    y_except2010.head()
    y_2010 = y_raw.query("year == 2010")
    y_2010.head()
    
    f = open(result_location + log_name, "a")
    f.write("Before 2010 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    model_except_2010 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
    model_except_2010.fit(X_except2010, y_except2010)
    
    f = open(result_location + log_name, "a")
    f.write("After 2010 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    y_pred2010 = model_except_2010.predict(X_2010)
    
    DF_cv_2010 = y_2010.copy()
    DF_cv_2010['y_pred2010'] = y_pred2010
    DF_cv_2010.to_csv(result_location + "SKlearn_1000tree_" + selectVariable + "_DF_cv_2010.csv")
    DF_cv_2010 = None
    
    y_pred = y_pred2010
    y = y_2010
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
    #r_count = np.corrcoef(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    #r_count = r_count[0,1]
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + log_name, "a")
    f.write("##### Temporal Cross-Validation 2010:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    #f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    #f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()
    
    model_except_2010 = None
    X_except2010 = None
    X_2010 = None
    y_except2010 = None
    y_2010 = None
    
    #### except 2015
    X_except2015 = X.query("year != 2015")
    X_except2015.head()
    X_2015 = X.query("year == 2015")
    X_2015.head()
    y_except2015 = y_raw.query("year != 2015")
    y_except2015.head()
    y_2015 = y_raw.query("year == 2015")
    y_2015.head()
    
    f = open(result_location + log_name, "a")
    f.write("Before 2015 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    model_except_2015 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
    model_except_2015.fit(X_except2015, y_except2015)
    
    f = open(result_location + log_name, "a")
    f.write("After 2015 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    y_pred2015 = model_except_2015.predict(X_2015)
    
    DF_cv_2015 = y_2015.copy()
    DF_cv_2015['y_pred2015'] = y_pred2015
    DF_cv_2015.to_csv(result_location + "SKlearn_1000tree_" + selectVariable + "_DF_cv_2015.csv")
    DF_cv_2015 = None
    
    y_pred = y_pred2015
    y = y_2015
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
    #r_count = np.corrcoef(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    #r_count = r_count[0,1]
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + log_name, "a")
    f.write("##### Temporal Cross-Validation 2015:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    #f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    #f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()
    
    model_except_2015 = None
    X_except2015 = None
    X_2015 = None
    y_except2015 = None
    y_2015 = None
    
    #### except 2020
    X_except2020 = X.query("year != 2020")
    X_except2020.head()
    X_2020 = X.query("year == 2020")
    X_2020.head()
    y_except2020 = y_raw.query("year != 2020")
    y_except2020.head()
    y_2020 = y_raw.query("year == 2020")
    y_2020.head()
    
    f = open(result_location + log_name, "a")
    f.write("Before 2020 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    model_except_2020 = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
    model_except_2020.fit(X_except2020, y_except2020)
    
    f = open(result_location + log_name, "a")
    f.write("After 2020 cv modelling!")
    f.write(str(psutil.virtual_memory()) + '\n')
    f.close()
    
    y_pred2020 = model_except_2020.predict(X_2020)
    
    DF_cv_2020 = y_2020.copy()
    DF_cv_2020['y_pred2005'] = y_pred2020
    DF_cv_2020.to_csv(result_location + "SKlearn_1000tree_" + selectVariable + "_DF_cv_2020.csv")
    DF_cv_2020 = None
    
    y_pred = y_pred2020
    y = y_2020
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
    #r_count = np.corrcoef(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    #r_count = r_count[0,1]
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + log_name, "a")
    f.write("##### Temporal Cross-Validation 2020:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    #f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    #f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    #f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()
    
    model_except_2020 = None
    X_except2020 = None
    X_2020 = None
    y_except2020 = None
    y_2020 = None


f = open(result_location + log_name, "a")
f.write("BASE DONE!\n\n")
f.write(str(psutil.virtual_memory()) + '\n')
f.close()

df_mergedPrepare("Total")
f = open(result_location + log_name, "a")
f.write("Finish total data!\n\n")
f.write(str(psutil.virtual_memory()) + '\n')
f.close()

Mdodel82CV("Total", log_name)
f = open(result_location + log_name, "a")
f.write("Total Pop 1 stage\n\n")
f.write(str(psutil.virtual_memory()) + '\n')
f.close()

df_mergedPrepare("Male")
f = open(result_location + log_name, "a")
f.write("Finish male data!\n\n")
f.write(str(psutil.virtual_memory()) + '\n')
f.close()

Mdodel82CV("Male", log_name)
f = open(result_location + log_name, "a")
f.write("Male Pop 1 stage\n\n")
f.write(str(psutil.virtual_memory()) + '\n')
f.close()

df_mergedPrepare("Female")
f = open(result_location + log_name, "a")
f.write("Finish female data!\n\n")
f.write(str(psutil.virtual_memory()) + '\n')
f.close()

Mdodel82CV("Female", log_name)
f = open(result_location + log_name, "a")
f.write("Female Pop 1 stage\n\n")
f.write(str(psutil.virtual_memory()) + '\n')
f.close()
