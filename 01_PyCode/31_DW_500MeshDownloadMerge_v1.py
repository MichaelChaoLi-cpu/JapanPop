# -*- coding: utf-8 -*-
"""
Download: https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=H&coordsys=2&format=shape

Created on Tue Jul 12 09:25:57 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

aimFolder = "F:\\17_Article\\01_Data\\17_meshData500m"
os.mkdir(aimFolder + "\\temp")

### change the default path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : aimFolder + "\\temp"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager(version="102.0.5005.61").install(), \
                          chrome_options = chromeOptions)

locationService = "https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=H&coordsys=2&format=shape"
driver.get(locationService)

# /html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[4]/div/div/article[1]/div/ul/li[3]/a
# ...
# /html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[4]/div/div/article[20]/div/ul/li[3]/a

# next page
# /html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[5]/div/div[1]/span[8]

page = 1
while page < 1+8:
    beginIndex = 1
    
    while beginIndex < 1 + 20:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[4]/div/div/article[" + str(beginIndex) + "]/div/ul/li[3]/a").click()
            time.sleep(3)
        except:
            print(page, beginIndex)
        
        beginIndex += 1
        
    driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/section/div[2]/main/section/div[5]/div/div[1]/span[8]").click()
    time.sleep(5)
    page += 1
    
driver.quit()
