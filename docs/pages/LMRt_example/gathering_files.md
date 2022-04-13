---
title: "Containerizing LMRt"
keywords: lmrt
tags: [lmrt]
sidebar: index_sidebar
permalink: gathering_files.html
summary: A page on containerizing LMRt
---

LMR Turbo ([LMRt](https://github.com/fzhu2e/LMRt)) is a public example that we will use to introduce users to the Fossilized Controller. At the end of this guide you should have a containerized LMRt that you can receive results from. Almost the entire process is done on the command line using an Ubuntu Linux distribution.

The original code and data for the climate model can be found [here](https://fzhu2e.github.io/LMRt/tutorial/quickstart_low-level-workflow.html)

## Setting up files
Before we can start containerizing LMRt, we need to make sure our code is ready for containerization. To get familiar with the process we will start with an "original" main file and then make changes to use our adapter libraries.

The first step is creating a new folder that is empty that will hold everything we want to put in the container. We will call it `LMRt-container`

### 1. Get our data
The first thing we will add to our folder is the dataset going inside the container.
The folder with the data can be found [here](https://drive.google.com/drive/folders/1VINQ33t9T7GW8gqn9g0q9uvSNXYOlCLN). You will want to download it as a zip and then unzip it
inside of your `LMRt-container`

! Warning !

Do not leave the zip inside of the `LMRt-container`, only have the unzipped folder

At this step this is what your folder should look like.
```bash
emily@VM:~/.../LMRt-container$ ls
data
```

### 2. Setting up our environment
One of the benefits of containerization is that you do not need to install endless dependencies for your project. Here, you only need to list out the dependencies and our tool will figure out the rest.

For this step we will want a `yml` file listing all of our dependencies. You can either download the file straight to your directory if you have `wget` capabilities or you can copy and paste the contents into a file named `presto_environment.yml`. You only need to do one of the options below.

**Downloading the file**
```bash
wget https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/LMRt-container/presto_environment.yml
```

**Copy and pasting contents**
```yml
# Test environment
name: presto_container
channels:
  - defaults
  - conda-forge
dependencies:
  - r-base=4.1
  - pip=21.2.4
  - python=3.9.7
  - cartopy
  - pyspharm
  - jupyterlab
  - pip:
    - requests==2.27.1
    - urllib3==1.26.8
    - LMRt
    - Flask
```

## 3. Getting the main file
Our main file is essentially the climate model itself. It has all the code to run and to give results. For LMRt, the file is a python (`.py`) file that you can either download directly if you have wget or you can copy the contents and save it to a file named `main.py`.

The file is too large to display in the documentation but an updated version can be found at the link [here](https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/main.py). You can either download it in your folder or you can use the wget command below.

**If you are donwloading the file from the link above, then you can simply right click and chose `Save As` in order to save it locally to your machine. Be careful when doing this as sometimes it will want to save the file as a txt, so it would try to save it as `main.py.txt`. Keep an eye out for this, all you need to do is delete the `.txt` part and you should be fine. If this gives you errors then you can just copy and paste the contents from the link in the appropriately named file**

```bash
wget https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/main.py
```
Do not worry about installing any of the libraries you see in the file. The main file should only be run inside of the container and our tool will worry about installing the libraries.

## 4. Getting the adapter library
Our adapter library provides a series of functions that allow you to communicate with containers. More information about the adapter libraries can be found in their respective Python and R pages. For this example, we are using the Python adapter.

The file is too large to display in the documentation but an updated version can be found at the link [here](https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/python-adapter/adapter.py). You can either download it in your folder or you can use the wget command below.You can either download it in your folder or you can use the wget command below.
```bash
wget https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/main.py
```

At this point, this is what your folder should look like
```bash
emily@VM:~/.../LMRt-container$ ls
adapter.py  data  main.py  presto_environment.yml
```

We are now ready to modify our main file so that is it adapter ready
## [Next](https://fossilizedcontainers.github.io/fossilized-controller/modifying_main.html)
