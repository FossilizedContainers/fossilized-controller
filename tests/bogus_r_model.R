# install lipdR library using remotes package
# remotes::install_github("nickmckay/LiPD-Utilities", subdir = "R", quiet = TRUE)

# load in LiPD and NetCDF packages
library("lipdR") 
library("ncdf4")

# call to R adapter package
# library(rpresto)

# TODO: A way to persist the adapter between the main function file call and 
# HTTP Server

fakeModel = function(adapter) {
  # check to see inside function
  print("\n---\nStart of the fake_model function\n---\n")
  
  
  # files handed to function
  # adapter.getFiles()
  
  lipd.results <- readLipd(lipd.file)
  
  if (!(length(lipd.results))) {
    return("Invalid LiPD file")
  }
  
  # adapter.setOutputFiles()
}

# adapter$register("fakeModel(adapter)")
# adapter$startServer()