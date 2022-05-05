---
title: "Adding Adapter Library"
keywords: guide
tags: [guide]
sidebar: index_sidebar
permalink: r_adding_adapter.html
summary: Modifying our main file using our adapter library
---


# For R Models

**The instructions below are tailored for the R adapter**

## 1. Loading Libraries

The first line of your code will be:

```r
source("adapter.R")
```

## 2. Register model
All of your code, including your library function calls will be in a wrapper function.

The reason for this is because we need a structure to register into our R adapter library. This is what allows us to communicate with the container with our CLI. We will use some example code from [Temp 12k Regional Composites](/gathering_files_temp12k.html) to demonstrate how to wrap and register your code.

The snippets you see are not functional code. Any `...` that you see means there is code between the lines, it is just hidden for demonstration purposes.

---

Example code formatting:
```r
library(lipdR)
library(geoChronR)
library(magrittr)

...

params <- jsonlite::read_json("temp12k-rc-example/params.json")

D <- readLipd("https://lipdverse.org/Temp12k/1_0_2/Temp12k1_0_2.zip")

...

readr::write_csv(outRecs,file.path(params$outDir,"recEnsemble.csv"))
```

### 2.1 Wrapping the model code
This is likely the general structure of your main file,
```r
# library statements
library(ggplot2)

...

# climate code
recon_param = 1

...

# output file creation
readr::write_csv(outRecs,file.path("output","recEnsemble.csv"))
```

We want to wrap all climate code into a function such as below
```r
source("adapter.R")

code_wrapper = function(adapter):
  # library statements
  library("egg")

  ...

  # climate code
  recon_param = 1

  ...

  # output file creation
  readr::write_csv(outRecs,file.path("output","recEnsemble.csv"))
```
It is important that you pass in the adapter.

### 2.2 Register function to the adapter
Now that the model is within a function, we can register it to the adapter. These are three lines added to the end of your file **outside of the wrapper function** that remain mostly unchanged regardless of what model you are working on.
```r
source("adapter.R")

code_wrapper = function(adapter):
  # library statements
  library("egg")

  ...

  # climate code
  recon_param = 1

  ...

  # output file creation
  readr::write_csv(outRecs,file.path("output","recEnsemble.csv"))
}
global.adapter$register("code_wrapper(global.adapter)")
global.adapter$startServer()
```


## 3. Getting parameters
**If you already have a function that will read a configuration file you do not need to do this step, you can move on to Step 3 and follow the instructions there**

```r
adapter$parameters
```
The parameters from the metadata file are accessed through the adapter's "inputs". This will return a `dictionary` that uses the same key names and values as the metadata function. Below is an example of how you would grab two parameters from an example metadata file.


```r
source("adapter.R")

code_wrapper = function(adapter):
  # library statements
  library("egg")

  ...

  # climate code
  recon_param = $


  ...

  # output file creation
  readr::write_csv(outRecs,file.path("output","recEnsemble.csv"))
}
global.adapter$register("code_wrapper(global.adapter)")
global.adapter$startServer()
```

## 4. Getting files
```r
adapter$inputs
```
The parameters from the metadata file are accessed through the `get_files` function. This will return a `dictionary` containing file objects that use the same key names and values as the metadata function. Below is an example of how you would grab a file from an example metadata file.
```r
source("adapter.R")

code_wrapper = function(adapter):
  #=== Grabbing Parameters Here ===#
  parameters = adapter$parameters
  # grabbing the specific parameter and saving it
  recon_param = parameters$recon_iterations
  figure_type = parameters$figure_type

  #=== Grabbing Files Here ===#
  files = adapter$inputs
  config = files#$configs

  # This function creates output files
  readr::write_csv(outRecs,file.path(parameters$output_dir,"recEnsemble.csv"))

# send in the name of your reconstruction wrapper function
global.adapter$register("code_wrapper(global.adapter)")
global.adapter$startServer()
```

## 5. Setting output files
```r
adapter$setOutputFiles("path")
```
In order to receive files from the container, we need to set which files will be returned from the model. Typically you will have functions that produce files. It is right after those functions that you want to set the output files. `set_output_files` takes in the name of the path and works with the adapter to return those files back to you after the run. You are able to specify either entire folders or single files. The adapter can handle both.

Below is an example of setting a folder as an output file.
```pr
source("adapter.R")

code_wrapper = function(adapter):
  #=== Grabbing Parameters Here ===#
  parameters = adapter$parameters
  # grabbing the specific parameter and saving it
  recon_param = parameters$recon_iterations
  figure_type = parameters$figure_type

  #=== Grabbing Files Here ===#
  files = adapter$inputs
  config = files#$configs

  # This function creates output files
  readr::write_csv(outRecs,file.path(parameters$output_dir,"recEnsemble.csv"))
  adapter$setOutputFiles("recEnsemble.csv")

# send in the name of your reconstruction wrapper function
global.adapter$register("code_wrapper(global.adapter)")
global.adapter$startServer()
```

Once you have made the changes explained above, you are now ready to start containerizing your model.
## [Next](https://fossilizedcontainers.github.io/fossilized-controller/containerize_model.html)
