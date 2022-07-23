#NOTE: this script only works on HPC

import pandas as pd
import numpy as np
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

#single_dataset_location = "F:\\17_Article\\01_Data\\98_20yearPickles\\"
single_dataset_location = "DP17/98_20yearPickles/"
result_location = "DP17/04_Result/"

### create log file:
f = open(result_location + "log_indicators.txt", "w")
f.close()

def getRawData():
    single_dataset_location = "DP17/98_20yearPickles/"
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
    
    return bigX, realPopDf_Y

def MdodelandCV(bigX, realPopDf_Y, aimGroup):
    result_location = "DP17/04_Result/"
    selectVariable = aimGroup + 'PopLog'
    ##### total population
    y=realPopDf_Y[[selectVariable]]
    
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
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r, pvalue = pearsonr(np.array(y), np.array(y_pred))
    reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
    reg.coef_
    reg.intercept_
    
    r2_count = r2_score(np.exp(y), np.exp(y_pred))
    r2_count
    mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
    mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
    rmse_count = np.sqrt(mse_count)
    r_count, pvalue_count = pearsonr(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + "log_indicators.txt", "a")
    f.write(aimGroup + "pop log ####\n")
    f.write("Total Year " + aimGroup + " pop log OOB rate: " + str(model.oob_score_) + "\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()
    
    # cross validation
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, train_size = 0.8,
                                                    random_state=1)
    model_cv = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1, n_jobs=-1)
    model_cv.fit(Xtrain, ytrain)
    ytest_cv = model_cv.predict(Xtest)
    
    y = ytest
    y_pred = ytest_cv
    r2 = r2_score(y, y_pred)
    r2
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r, pvalue = pearsonr(np.array(y), np.array(y_pred))
    reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
    reg.coef_
    reg.intercept_
    
    r2_count = r2_score(np.exp(y), np.exp(y_pred))
    r2_count
    mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
    mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
    rmse_count = np.sqrt(mse_count)
    r_count, pvalue_count = pearsonr(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + "log_indicators.txt", "a")
    f.write("##### Cross-Validation:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()

def TemporalCV(bigX, realPopDf_Y, aimGroup):
    result_location = "DP17/04_Result/"
    selectVariable = aimGroup + 'PopLog'
    ##### total population
    y=realPopDf_Y[[selectVariable]]
    
    df_merged = pd.merge(y, bigX, on = ['G04c_001', 'year'], how='inner')
    df_merged.shape
    
    df_merged = df_merged.dropna()
    df_merged.shape
    X = df_merged.iloc[:, 1:54]
    X = X.fillna(0)
    y = df_merged.iloc[:, 0:1]
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
    
    y_pred = y_pred2005
    y = y_2005
    r2 = r2_score(y, y_pred)
    r2
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r, pvalue = pearsonr(np.array(y), np.array(y_pred))
    reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
    reg.coef_
    reg.intercept_
    
    r2_count = r2_score(np.exp(y), np.exp(y_pred))
    r2_count
    mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
    mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
    rmse_count = np.sqrt(mse_count)
    r_count, pvalue_count = pearsonr(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + "log_indicators.txt", "a")
    f.write("##### Temporal Cross-Validation 2005:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
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
    
    y_pred = y_pred2010
    y = y_2010
    r2 = r2_score(y, y_pred)
    r2
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r, pvalue = pearsonr(np.array(y), np.array(y_pred))
    reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
    reg.coef_
    reg.intercept_
    
    r2_count = r2_score(np.exp(y), np.exp(y_pred))
    r2_count
    mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
    mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
    rmse_count = np.sqrt(mse_count)
    r_count, pvalue_count = pearsonr(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + "log_indicators.txt", "a")
    f.write("##### Temporal Cross-Validation 2010:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
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
    
    y_pred = y_pred2015
    y = y_2015
    r2 = r2_score(y, y_pred)
    r2
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r, pvalue = pearsonr(np.array(y), np.array(y_pred))
    reg = LinearRegression().fit(pd.DataFrame(y), np.array(y_pred))
    reg.coef_
    reg.intercept_
    
    r2_count = r2_score(np.exp(y), np.exp(y_pred))
    r2_count
    mae_count = mean_absolute_error(np.exp(y), np.exp(y_pred))
    mse_count = mean_squared_error(np.exp(y), np.exp(y_pred))
    rmse_count = np.sqrt(mse_count)
    r_count, pvalue_count = pearsonr(np.array(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count = LinearRegression().fit(pd.DataFrame(np.exp(y)), np.array(np.exp(y_pred)))
    reg_count.coef_
    reg_count.intercept_
    
    f = open(result_location + "log_indicators.txt", "a")
    f.write("##### Temporal Cross-Validation 2015:\n")
    f.write("Total Year " + aimGroup + " pop log R2 rate: " + str(r2) + "\n")
    f.write("Total Year " + aimGroup + " pop log MAE rate: " + str(mae) + "\n")
    f.write("Total Year " + aimGroup + " pop log RMSE rate: " + str(rmse) + "\n")
    f.write("Total Year " + aimGroup + " pop log r rate: " + str(r) + "\n")
    f.write("Total Year " + aimGroup + " pop log p value: " + str(pvalue) + "\n")
    f.write("Total Year " + aimGroup + " pop log intercept: " + str(reg.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop log coeffciet: " + str(reg.coef_) + "\n")
    f.write("Total Year " + aimGroup + " pop R2 rate: " + str(r2_count) + "\n")
    f.write("Total Year " + aimGroup + " pop MAE rate: " + str(mae_count) + "\n")
    f.write("Total Year " + aimGroup + " pop RMSE rate: " + str(rmse_count) + "\n")
    f.write("Total Year " + aimGroup + " pop r rate: " + str(r_count) + "\n")
    f.write("Total Year " + aimGroup + " pop p value: " + str(pvalue_count) + "\n")
    f.write("Total Year " + aimGroup + " pop intercept: " + str(reg_count.intercept_) + "\n")
    f.write("Total Year " + aimGroup + " pop coeffciet: " + str(reg_count.coef_) + "\n\n")
    f.close()

print("BASE DONE!")
bigX, realPopDf_Y = getRawData()
print("We get the data!")
MdodelandCV(bigX, realPopDf_Y, "Total")
print("Total Pop 1 stage")
TemporalCV(bigX, realPopDf_Y, "Total")
print("Total Pop 2 stage")
MdodelandCV(bigX, realPopDf_Y, "Male")
print("Total Male 1 stage")
TemporalCV(bigX, realPopDf_Y, "Male")
print("Total Male 2 stage")
MdodelandCV(bigX, realPopDf_Y, "Female")
print("Total Female 1 stage")
TemporalCV(bigX, realPopDf_Y, "Female")
print("Total Female 2 stage")