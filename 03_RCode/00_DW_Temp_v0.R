# Author: M.L.

# end

library(rgdal)
library(sp)
library(tidyverse)
library(dplyr)
library(rgeos)

mesh <- readOGR(dsn = "F:/17_Article/01_Data/00_mesh", layer = "mesh1")
proj <- mesh@proj4string

mesh.center <- gCentroid(mesh,byid=TRUE)
mesh.center <- coordinates(mesh.center)
mesh.center <- as.data.frame(mesh.center)
mesh.center$id <- mesh$Name

xy <- mesh.center %>% dplyr::select(x, y)
mesh.center.point <- SpatialPointsDataFrame(coords = xy, data = mesh.center, proj4string = proj)

writeOGR(mesh.center.point, "F:/17_Article/01_Data/00_mesh", "mesh_center_point",driver = "ESRI Shapefile")
