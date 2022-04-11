# install lipdR library using remotes package
# remotes::install_github("nickmckay/LiPD-Utilities", subdir = "R", quiet = TRUE)

# load in LiPD and NetCDF packages
library("lipdR") 
library("ncdf4")

# call to R adapter package
#library(rpresto)

# TODO: A way to persist the adapter between the main function file call and 
# HTTP Server

fakeModel = function(adapter) {
  # check to see inside function
  print("\n---\nStart of the fake_model function\n---\n")
  
  
  # files handed to function
  lipd.file <- adapter$getFiles()
  lipd.file <- lipd.file$weldeab
  
  
  lipd.results <- readLipd(lipd.file)
  
  if (!(length(lipd.results))) {
    return("Invalid LiPD file")
  } else {
    print("\n---\nLIPD file is valid\n---\n")
  }
  
  adapter$setOutputFiles("lipd-files/GeoB9307_3.Weldeab.2014.lpd")
  adapter$setOutputFiles("nc-files/WMI_Lear.nc")
  
  print("\n---\nEnd of the fake_model function\n---\n")
}

global.adapter$register("fakeModel(global.adapter)")
global.adapter$startServer()