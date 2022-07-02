# JapanPop
This repo is the project to estimate the population distribution in Japan. (DP17)

## Projection and Resolution
WGS84 0.004 degree  

## Industry Standard Guidelines (ISG)   
Due to my poor memory, I cannot remember too many things. To reduce the recalling 
time, we set this ISG.     
**Within this Repo and Project, all datasets and procedures should follow this ISG**    
     
### Pandas.DataFrame
1. the indexes are ['G04c_001', 'year'].     
2. all invidual variable should be merged by pd.concat([df, vari], axis=1).    


### Raster
1. the resolutions should be 0.004 or 0.004*n.    
2. the projection should be WGS84.     
3. the raw data from NASA should be using naive projection.