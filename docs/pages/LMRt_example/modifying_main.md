---
title: "Containerizing LMRt"
keywords: lmrt
tags: [lmrt]
sidebar: index_sidebar
permalink: modifying_main.html
summary: Modifying our main file using our adapter library
---

We should now have all of the necessary files to containerize LMRt. The only thing now is to modify the main file so that it is using the Python adapter library. This is what will allow our CLI to communicate with the container once it is built.


**For those with limited time**


If you find you don't have time to go through these steps, or just don't want to, the completed and changed main file can be found [here](https://github.com/FossilizedContainers/fossilized-controller/blob/trunk/LMRt-example/LMRt-container/main.py) and directly downloaded [here](https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/LMRt-container/main.py).

You can then compare this to our original file and see what was changed and added. When doing major adapter work the lines are denoted with `===Adapter work starts here===` comments.


## 1. Adding adapter library
In order to use the adapter library, we will need to import it and any depedent libraries. Same as before, do not worry about installing the following libraries

* os
* sys
* lipd
* adapter

You can add these directly to the import lines seen at the top of the main file. Since `os` was part of the original file, we can skip that one.

A snippet of the first lines of the file are as follows
```python
## These are ones you want to import for the adapter
import sys
import lipd
import adapter

# these are the original imports
import LMRt
import os
import numpy as np
import pandas as pd
import xarray as xr
```

## 2. Wrapping the model code
Everything after the imports is code relating to the model that we need to wrap around a function. The reason for this is because we need a structure to register into our adapter libraries. This is what allows us to communicate with the container with our CLI. The LMRt code is too long so I will show a condensed version with the first and last lines of the model. The `...` that you see means there is code between the lines, it is just hidden for demonstration purposes.

Currently this is the structure of your main file
```python
import adapter
...
# preprocessing
job = LMRt.ReconJob()
job.load_configs(cfg_path='/PAGES2k_CCSM4_GISTEMP/configs.yml', verbose=True)
...
fig, ax = res.vars['nino3.4'].validate(target_series, verbose=True).plot(xlim=[1880, 2000])
fig.savefig("/figure2.png")
```

We then create a new function, `lmrt_wrapper` and add all of the code after the imports into it. It is import that we pass the adapter into the function.
```python
import adapter
...

def lmrt_wrapper(adapter):
  # preprocessing
  job = LMRt.ReconJob()
  job.load_configs(cfg_path='/PAGES2k_CCSM4_GISTEMP/configs.yml', verbose=True)
  ...
  fig, ax = res.vars['nino3.4'].validate(target_series, verbose=True).plot(xlim=[1880, 2000])
  fig.savefig("/figure2.png")
```
## 3. Register the function to the adapter
Now that the model is within a function, we can register it to the adapter. These are three lines added to the end of your file **outside of the wrapper function** that remain mostly unchanged.

```python
import adapter
...

def lmrt_wrapper(adapter):
  # preprocessing
  job = LMRt.ReconJob()
  job.load_configs(cfg_path='/PAGES2k_CCSM4_GISTEMP/configs.yml', verbose=True)
  ...
  fig, ax = res.vars['nino3.4'].validate(target_series, verbose=True).plot(xlim=[1880, 2000])
  fig.savefig("/figure2.png")

# have to call adapter in the adapter.py file as adapter.adapter
adapter = adapter.global_adapter
# send in the name of your reconstruction wrapper function
adapter.register(lmrt_wrapper)
adapter.start_server()
```

## 4. Add necessary adapter lines
Now that we have the basis for our adapter, we want to start using the adapter. It can be easy to get lost during this step because the file is large and I can't show the entire thing after each step. If you find yourself lost, refer to the [finished file](https://github.com/FossilizedContainers/fossilized-controller/blob/trunk/LMRt-example/LMRt-container/main.py) to make sure what you have is correct.

### 4.1 Getting files and parameters
This step is based off a file we will introduce later that is outside the container that helps the CLI communicate. It is a metadata file that is introduced in a later step. You can look at the [file](https://github.com/FossilizedContainers/fossilized-controller/blob/trunk/LMRt-example/metadata.json) on the side to get a better understanding, but you can keep going by adding the following lines to your file.

Right before we start the code for the model, we will want to load in any files or parameters that will be sent into the container *after* it is built. This allows you to change the parameters after each run without having to create the container again.

We are only importing one file named `configs` that is downloaded at a later step.

There are two parameters that we are concerned with
* recon_iterations
* figure_type

`recon_iterations` is how many times we want the internal algorithm to iterate. It should be noted that 1 is the default is the only reccomended value when running on personal machines. Anything higher will require more computing power.

`figure_type` is a paramter we are adding to specify what figure we want output when the model finishes. The two types of figure the model works with is `graph` or `map`.

TO DO:
* Add the adapter work lines
* Specify where we are using the parameters

### 4.2 Setting output files
