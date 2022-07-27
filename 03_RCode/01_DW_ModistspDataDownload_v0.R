library(MODIStsp)

#### NDVI A1 is 16day 500m
MODIStsp_get_prodlayers("M*D13A1")

MODIStsp(
  gui = F, out_folder = "F:/17_Article/01_Data/16_NDVI",
  out_folder_mod = "F:/17_Article/01_Data/16_NDVI",
  selprod = "Vegetation_Indexes_16Days_500m (M*D13A1)", bandsel = "NDVI",
  user = NASAuser, password = NASAuser,
  start_date = "2001.01.01", end_date = "2020.12.31",
  spatmeth= "file", spafile= "F:/15_Article/01_RawData/theWholeJapan.shp",
  out_projsel = 'Native', output_proj = "MODIS Sinusoidal",
  delete_hdf = T, out_format = "GTiff",
  parallel = 8
)

#### land cover 2000 there is no 2000
MODIStsp_get_prodlayers("MCD12Q1")

MODIStsp(
  gui = F, out_folder = "F:\\17_Article\\01_Data\\01_LandCover\\LandCoverMerge",
  out_folder_mod = "F:\\17_Article\\01_Data\\01_LandCover\\LandCoverMerge",
  selprod = "LandCover_Type_Yearly_500m (MCD12Q1)", bandsel = "LC2",
  user = NASAuser, password = NASAuser,
  start_date = "2000.01.01", end_date = "2000.12.31",
  spatmeth= "file", spafile= "F:/15_Article/01_RawData/theWholeJapan.shp",
  out_projsel = 'Native', output_proj = "MODIS Sinusoidal",
  delete_hdf = T, out_format = "GTiff",
  parallel = 8
)
