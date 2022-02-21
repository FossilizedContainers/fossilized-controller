required.libraries = c("rjson")

for ( pkg in required.libraries ) {
  if ( !requireNamespace(pkg) ) {
    install.packages(pkg)
  }
}

# TODO: A way to persist the adapter between the main function file call and 
# HTTP Server

# What is called by the adapter's HTTP server to run the model
register = function (env, lambda) {
}

# TODO: Params in a JSON file;parses the JSON file and converts strings to actual, 
# expected values, e.g. ints, arrays, etc. Returns map with string keys
# 
# Params are supplied by the model's documentation
# If config = adapter.getParams: config.get("spread") = relevant value in 
# metadata.JSON
getFCParams = function () {
}

# TODO: Run the HTTP server in the container
runFCServer = function () {
  
}

# TODO: Signals to adapter what files to send back in the HTTP Response message
FCFilestoSend = function (file.location) {
  
}

# TODO: Gets files at FCFilestoSend 
sendFCFiles = function () {
  
}