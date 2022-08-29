# -*- coding: utf-8 -*-
"""
Training RNN

Created on Tue Aug 23 12:28:19 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import dask.dataframe as dd

data_location = "F:/17_Article/09_DataAdvanceProject/02_TokyoData/"
X = dd.read_csv(data_location + "01_Xtokyo.csv")
y = dd.read_csv(data_location + "02_ytokyo.csv")

#X = X.drop(['G04c_001', 'year'], axis = 1)
#y = y.drop(['G04c_001', 'year'], axis = 1)

from tensorflow import keras

model = keras.models.Sequential([
    
    ])