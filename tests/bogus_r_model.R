# Might cause issues if environment does not already have lipdR installed

# install lipdR library using remotes package
# remotes::install_github("nickmckay/LiPD-Utilities", subdir = "R", quiet = TRUE)

# load in LiPD and NetCDF packages
library("lipdR") 
library("ncdf4")

fakeModel = function(bogus, lipd_file) {
  
  lipd_results <- readLipd(lipd_file)
  
  if (!(length(lipd_results))) {
    return("Invalid LiPD file")
  }
  
  net_cdf_path <- 
    "C:/Users/mumbi/Documents/spring 2022/cs 486/fossilized-controller/test/nc-files/WMI_Lear.nc"
  
  return(net_cdf_path)
}
