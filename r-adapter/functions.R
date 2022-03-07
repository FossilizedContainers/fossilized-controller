required.libraries = c("rjson")

for ( pkg in required.libraries ) {
  if ( !requireNamespace(pkg) ) {
    install.packages(pkg)
  }
}

# TODO: A way to persist the adapter between the main function file call and 
# HTTP Server

# What is called by the adapter's HTTP server to run the model
registerModel = function (env, lambda) {
}

# TODO: Run lambda from registerModel
runModel = function (env, lambda) {
  
}

# TODO: Params in a JSON file;parses the JSON file and converts strings to actual, 
# expected values, e.g. ints, arrays, etc. Returns map with string keys
# 
# Params are supplied by the model's documentation
# If config = adapter.getParams: config.get("spread") = relevant value in 
# metadata.JSON
getFcParams = function () {
}

# TODO: Run the HTTP server in the container
runFcServer = function () {
  
}

# TODO: Signals to adapter what files to send back in the HTTP Response message.
#
# Always assumes that you are appending file to list of files to send back as 
# output.
setOutFiles = function (file.location) {
  
}

# TODO: Gets files at setFcFiles 
getOutFiles = function () {
  
}