library(MODIStsp)

#### NDVI
MODIStsp_get_prodlayers("M*D13C2")

MODIStsp(
  gui = F, out_folder = "F:/17_Article/01_Data/16_NDVI",
  out_folder_mod = "F:/17_Article/01_Data/16_NDVI",
  selprod = "Vegetation_Indexes_Monthly_005dg (M*D13C2)", bandsel = "NDVI",
  user = "chaoli0394", password = "097680Li",
  start_date = "2000.01.01", end_date = "2020.12.31",
  spatmeth= "file", spafile= "F:/15_Article/01_RawData/theWholeJapan.shp",
  out_projsel = 'Native', output_proj = "MODIS Sinusoidal",
  delete_hdf = T, out_format = "GTiff",
  parallel = 8
)
