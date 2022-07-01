# -*- coding: utf-8 -*-
"""
Download 500 meter population

URL: https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521&toukeiYear=2000&aggregateUnit=H&serveyId=H002005112000&statsId=T000386

Created on Fri Jul  1 13:20:18 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import zipfile
import glob
import pandas as pd

aimFolder = "F:\\17_Article\\01_Data\\09_populationMesh\\500m"
os.mkdir(aimFolder + "\\temp")

### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="102.0.5005.61").install(), \
                          chrome_options = chromeOptions)

locationService = "https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521&toukeiYear=2000&aggregateUnit=H&serveyId=H002005112000&statsId=T000386"
driver.get(locationService)

#/html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[4]/div/div/article[1]/div/ul/li[4]/a
#
#/html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[4]/div/div/article[20]/div/ul/li[4]/a

# next page
#/html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[5]/div/div[1]/span[8]

page = 1
while page < 1+8:
    beginIndex = 1
    
    while beginIndex < 1 + 20:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[4]/div/div/article[" + str(beginIndex) + "]/div/ul/li[4]/a").click()
            time.sleep(3)
        except:
            print(page, beginIndex)
        
        beginIndex += 1
        
    driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[5]/div/div[1]/span[8]")
    time.sleep(5)
    page += 1