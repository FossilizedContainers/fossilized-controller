---
title: "Adding adapter library"
keywords: guide
tags: [guide]
sidebar: index_sidebar
permalink: adding_adapter.html
summary: Modifying our main file using our adapter library
---

**The instructions below are tailored for the Python adapter**
## 1. Imports
The following libraries are needed for the adapter to work properly. Please make sure to import them at the top of your Python file
* os
* sys
* lipd
* adapter

You do not need to install the lipd package yourself, this will happen inside the container.

## 2. Register model
Everything after the imports is code relating to the model that we need to wrap around a function. The reason for this is because we need a structure to register into our adapter libraries. This is what allows us to communicate with the container with our CLI. I will use some example code from [LMRt](https://fossilizedcontainers.github.io/fossilized-controller/gathering_files.html) to demonstrate how to wrap and register your code. The snippets you see are not functional code. Any `...` that you see means there is code between the lines, it is just hidden for demonstration purposes.

Example code
```python
import adapter
# import the rest of the libraries as well, I excluded them to save space.
recon_param = 1

job = LMRt.ReconJob()
# This functions creates output files in a folder named recon
job.run(recon_seeds=np.arange(recon_param), verbose=True)
```

### 2.1 Wrapping the model code
This is likely the general structure of your main file,
```python
# imports
import adapter

# climate code
recon_param = 1

job = LMRt.ReconJob()
# This function creates output files in a folder named recon
job.run(recon_seeds=np.arange(recon_param), verbose=True)

```

We want to wrap all climate code into a function such as below
```python
import adapter

def code_wrapper(adapter):
  # climate code
  recon_param = 1

  job = LMRt.ReconJob()
  # This function creates output files in a folder named recon
  job.run(recon_seeds=np.arange(recon_param), verbose=True)

```
It is important that you pass in the adapter.

### 2.2 Register function to the adapter
Now that the model is within a function, we can register it to the adapter. These are three lines added to the end of your file **outside of the wrapper function** that remain mostly unchanged regardless of what model you are working on.
```python
import adapter

def code_wrapper(adapter):
  # climate code
  recon_param = 1

  job = LMRt.ReconJob()
  # This function creates output files in a folder named recon
  job.run(recon_seeds=np.arange(recon_param), verbose=True)

# have to call adapter in the adapter.py file as adapter.adapter
adapter = adapter.global_adapter
# send in the name of your reconstruction wrapper function
adapter.register(code_wrapper)
adapter.start_server()
```

For the following steps I will use the following metadata file as an example
```json
{
    "parameters": {
        "recon_iterations": 1,
        "figure_type": "graph"
    },
    "inputs": {
        "configs": "configs.yml"
    }
}
```

## 3. Getting parameters
**If you already have a function that will read a a configuration file you do not need to do this step, you can move on to Step 3 and follow the instructions there**
```python
adapter.get_parameters()
```
The parameters from the metadata file are accessed through the `get_parameters` function. This will return a `dictionary` that uses the same key names and values as the metadata function. Below is an example of how you would grab two parameters from an exmaple metadata file.

```python
import adapter

def code_wrapper(adapter):
  #=== Grabbing Parameters Here ===#
  parameters = adapter.get_parameters()
  # grabbing the specific parameter and saving it
  recon_param = parameters['recon_iterations']
  figure_type = parameters['figure_type']

  job = LMRt.ReconJob()
  # This function creates output files in a folder named recon
  job.run(recon_seeds=np.arange(recon_param), verbose=True)

# have to call adapter in the adapter.py file as adapter.adapter
adapter = adapter.global_adapter
# send in the name of your reconstruction wrapper function
adapter.register(code_wrapper)
adapter.start_server()
```

## 4. Getting files
```python
adapter.get_files()
```
The parameters from the metadata file are accessed through the `get_files` function. This will return a `dictionary` containing file objects that use the same key names and values as the metadata function. Below is an example of how you would grab a file from an exmaple metadata file.
```python
import adapter

def code_wrapper(adapter):
  #=== Grabbing Parameters Here ===#
  parameters = adapter.get_parameters()
  # grabbing the specific parameter and saving it
  recon_param = parameters['recon_iterations']
  figure_type = parameters['figure_type']

  #=== Grabbing Files Here ===#
  files = adapter.get_files()
  config = files['configs']

  job = LMRt.ReconJob()
  # This function creates output files in a folder named recon
  job.run(recon_seeds=np.arange(recon_param), verbose=True)

# have to call adapter in the adapter.py file as adapter.adapter
adapter = adapter.global_adapter
# send in the name of your reconstruction wrapper function
adapter.register(code_wrapper)
adapter.start_server()
```

## 5. Setting output files
```python
adapter.set_output_files(path)
```
In order to receive files from the container, we need to set which files will be returned from the model. Typically you will have functions that produce files. It is right after those functions that you want to set the output files. `set_output_files` takes in the name of the path and works with the adapter to return those files back to you after the run. You are able to specify either entire folders or single files. The adapter can handle both.

Below is an example of setting a folder as an output file.
```python
import adapter

def code_wrapper(adapter):
  #=== Grabbing Parameters Here ===#
  parameters = adapter.get_parameters()
  # grabbing the specific parameter and saving it
  recon_param = parameters['recon_iterations']
  figure_type = parameters['figure_type']

  #=== Grabbing Files Here ===#
  files = adapter.get_files()
  config = files['configs']

  job = LMRt.ReconJob()
  # This function creates output files in a folder named recon
  job.run(recon_seeds=np.arange(recon_param), verbose=True)

  # it is reccomended to use abspath()
  nc_path = os.path.abspath('recon/')
  adapter.set_output_files(nc_path)

# have to call adapter in the adapter.py file as adapter.adapter
adapter = adapter.global_adapter
# send in the name of your reconstruction wrapper function
adapter.register(code_wrapper)
adapter.start_server()
```

Once you have made the changes explained above, you are now ready to start containerizing your model. 
## [Next](https://fossilizedcontainers.github.io/fossilized-controller/containerize_model.html)
