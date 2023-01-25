# JapanPop
This repo is the project to estimate the population distribution in Japan from 2001 to 2020. (DP17)

## Title
Gridded Datasets for Japanese Total, Male, and Female Population from 2001-2020  
  
## Author  
Chao Li, Shunsuke Managi  

## Results:  
### Animation of Total Population Distribution (2001 - 2020):
![](05_Figure/zzz_total_log.gif)
   
### Animation of Male Population Distribution (2001 - 2020):
![](05_Figure/zzz_male_log.gif)
   
### Animation of Female Population Distribution (2001 - 2020):
![](05_Figure/zzz_female_log.gif)
  
### Total Population Distribution (2001 - 2020):
![](05_Figure/Figure2.jpg)
   
### Male Population Distribution (2001 - 2020):
![](05_Figure/Figure3.jpg)
   
### Female Population Distribution (2001 - 2020):
![](05_Figure/Figure4.jpg)
   
## Manuscript
[Gridded datasets for Japanese total, male, and female population over 2001-2020](07_Manuscript/DP17_manu.pdf)  
  
## Python Code
**Note:** in the folder, the scripts are more than here listed, but you can just ignore
theme since they are discarded in the project. We keep them just in case.
**Reminder:** you need to revise the path/address by youself if you going to use. The mesh
id and time stamp are named as ['G04c_001', 'year'].
  
### Base Mesh File
[24_DW_DownloadMergeJapanMesh500_v1.py](01_PyCode/24_DW_DownloadMergeJapanMesh500_v1.py): This script is to 
build 500m mesh base datasets, including a *point shapefile* and polygon shapefile. 
   
### Output Variables (in total 3 Output Variables)
[26_DW_DownloadJapanPopulation500_v1.py](01_PyCode/26_DW_DownloadJapanPopulation500_v1.py): This script is 
to download population data from Japan government <https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521&toukeiYear=2015&aggregateUnit=Q&serveyId=Q002005112015&statsId=T000876>.  
[27_DW_StandardDataframeJapanPopulation500_v1.py](01_PyCode/27_DW_StandardDataframeJapanPopulation500_v1.py): This script is to obtain output variables, total, male, and female population counts in 2005, 2010, and 2015.  
  
### Features (in total 53 Features)
[01_DW_MCD12Q1LandCover500m_v1.py](01_PyCode/01_DW_MCD12Q1LandCover500m_v1.py): This script is to convert 
the hdf files from NASA MCD12Q1 in to GTiff, which is yearly land cover dataset.   
[02_DW_MergeLandCover500m_v1.py](01_PyCode/02_DW_MergeLandCover500m_v1.py): This script is to merge the 
sperated GTiff data into one by year.  
[23_DW_LandCoverMultiYears_v1.ipynb](01_PyCode/23_DW_LandCoverMultiYears_v1.ipynb): This Script is to extract the land cover binary data and distance data to the mesh *point shapefile* mentioned in [24_DW_DownloadMergeJapanMesh500_v1.py](01_PyCode/24_DW_DownloadMergeJapanMesh500_v1.py).
In this script, 32 features are obtained.  
[25_DW_NppNtlPrecipitationTemperature_v1.ipynb](01_PyCode/25_DW_NppNtlPrecipitationTemperature_v1.ipynb): This 
script is to obtain NTL, NPP, 4 temperature-related data, and precipitation. In this script: 7 features are obtained.  
[28_DW_PointOfInterestDistance2006_v1.py](01_PyCode/28_DW_PointOfInterestDistance2006_v1.py): This script is to
obtain distances to POIs, including museum, government, police station, fireman station, hospital, postal 
office, and disable supporter. In this script: 8 features are obtained.   
[18_DW_HighPopulationClassAndDistance_v1.py](01_PyCode/18_DW_HighPopulationClassAndDistance_v1.py): This script is to obtain the distance to high populaiton area (1 feature).  
[15_DW_RoadDensity_v1.py](01_PyCode/15_DW_RoadDensity_v1.py): This script is to obtain road density (1 feature).   
[16_DW_RiverDistance_v1.py](01_PyCode/16_DW_RiverDistance_v1.py): This script is to obtain the distance to river (1 feature).  
[17_DW_CoastlineDistance_v1.py](01_PyCode/17_DW_CoastlineDistance_v1.py): This script is to obtain the distance to coastal lines (1 feature).   
[20_DW_RailwayDistance_v1](01_PyCode/20_DW_RailwayDistance_v1): This script is to obtain the distance to railway and stations (2 features).   
[29_DW_MergeCompleteDataset_v1.py](01_PyCode/29_DW_MergeCompleteDataset_v1.py): This script is to build the datasets for analyses.   
[30_AN_RandomForestFor4Year_v1.py](01_PyCode/30_AN_RandomForestFor4Year_v1.py): This script is to run random forest models and do the cross-validation and predictions.   
[32_VI_PlotEachYearJapanesePop_v1.py](01_PyCode/32_VI_PlotEachYearJapanesePop_v1.py): This script is to visualize sperated figures.  
[33_VI_PlotTemporalCrossValidation_v1.py](01_PyCode/33_VI_PlotTemporalCrossValidation_v1.py): This script is to visualize the results of temporal cross-validation.  
[34_VI_AnimatePopulationDistribution_v1.py](01_PyCode/34_VI_AnimatePopulationDistribution_v1.py): This script is to make the animation shown in the front of this file. 
[35_AN_RandomForestAccuracy_v1.py](01_PyCode/35_AN_RandomForestAccuracy_v1.py): This script is to check the accuracy of the models.  
[36_VI_MergeEachYearJapanesePop_v1.py](01_PyCode/36_VI_MergeEachYearJapanesePop_v1.py): This script is to visualize merged figures.   
[37_AN_CVworldPop_v1.py](01_PyCode/37_AN_CVworldPop_v1.py): This script is to compare the accuracy of the predictions in this study to the results of WorldPop.  
[38_VI_ScatterPlotFittingModel_v1.py](01_PyCode/38_VI_ScatterPlotFittingModel_v1.py): This script is to visualize accuary of the fitting models.   
   
## Workflows:
The scripts are organized in this order:  
**24 -> 26-> 27-> 01 -> 02 -> 23 -> 25 -> 28 -> 18 -> 15 -> 16 -> 17 -> 20 -> 29 -> 30 -> 32 ->33 -> 34 -> 35 -> 36 -> 37 -> 38**  
  
## Data Archieve
**Forthcoming**  
  
## Projection and Resolution
Projection: WGS84; Spatial Resolution: 500m; Temporal Resolution:  yearly
   
## Contact Us:
- Email: Prof. Shunsuke Managi <managi@doc.kyushu-u.ac.jp>  
- Email: Chao Li <chaoli0394@gmail.com>
  
## Term of Use:
Authors/funders retain copyright (where applicable) of code on this Github repo. This GitHub repo and its contents herein, including data, link to data source, and analysis code that are intended solely for reproducing the results in the manuscript "Gridded datasets for Japanese total, male, and female population over 2001-2020". The analyses rely upon publicly available data from multiple sources, that are often updated without advance notice. We hereby disclaim any and all representations and warranties with respect to the site, including accuracy, fitness for use, and merchantability. By using this site, its content, information, and software you agree to assume all risks associated with your use or transfer of information and/or software. You agree to hold the authors harmless from any claims relating to the use of this site.  