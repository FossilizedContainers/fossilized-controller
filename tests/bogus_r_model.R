# install lipdR library using remotes package
# remotes::install_github("nickmckay/LiPD-Utilities", subdir = "R", quiet = TRUE)

# load in LiPD and NetCDF packages
library("lipdR") 
library("ncdf4")

# call to R adapter package
# library(rpresto)

# TODO: A way to persist the adapter between the main function file call and 
# HTTP Server

fakeModel = function(bogus, lipd.file) {
  # Register the main function / process
  # adapter.register(registerFunction)
}

registerFunction = function () {
  # adapter.getParams()
  
  lipd.results <- readLipd(lipd.file)
  
  if (!(length(lipd.results))) {
    return("Invalid LiPD file")
  }
  
  net.cdf.path <- 
    "C:/Users/mumbi/Documents/spring 2022/cs 486/fossilized-controller/test/nc-files/WMI_Lear.nc"
  
  # adapter.send(net.cdf.path)
}