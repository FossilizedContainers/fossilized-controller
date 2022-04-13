---
title: "Containerizing LMRt"
keywords: lmrt
tags: [lmrt]
sidebar: index_sidebar
permalink: containerize_lmrt.html
summary: A page on containerizing LMRt
---

Our model should now be ready to containerize using our tool.

The first thing we want to do is make sure we are in the correct folder. Make sure you are in the folder with the model and data. It should look like below.
```bash
emily@VM:~/.../LMRt-container$ ls
adapter.py  data  main.py  presto_environment.yml
```
The second thing we want to do is make sure that our tool is installed correctly by running the following command.
```bash
emily@VM:~/.../LMRt-container$ presto guide
Click the following link for a guide on how to use the tool!
https://fossilizedcontainers.github.io/fossilized-controller/
```

## 1. Create the Dockerfile
A Dockerfile is a file that is essentially a list of instructions Docker uses to create a container. Luckily, we don't need to know much about how to create the file by hand as `presto create` does it for us! All it takes in is the language we are using and the file that holds all of our reconstruction code.

```
presto create
```

```bash
emily@VM:~/.../LMRt-container$ presto create
What is the command to run your main file?
Here are some examples:
- python3 main.py
- r main.R
- sh main.sh

> : python3 main.py
Dockerfile created!
```
---

You should now see a Dockerfile in your directory:
```bash
alpha@demo:~/.../LMRt-container$ ls
adapter.py  data  Dockerfile  main.py  presto_environment.yml
alpha@demo:~/.../LMRt-container$
```
The Dockerfile should look like the following:
```Dockerfile
FROM continuumio/anaconda3

RUN conda update -n base -c defaults conda

# setup conda environment
COPY presto_environment.yml .
RUN conda env create -f presto_environment.yml
RUN echo "conda activate presto_container" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
RUN conda activate presto_container

# copy all files to the root directory of the container
COPY . /

# run the command in the context of the environment we made
CMD conda run --no-capture-output -n presto_container python3 main.py
```

## 2. Build the Docker Image
More information about what Docker Images are can be found
[here](/docker.html#docker-images). Images are essentially what your container uses to run so they need to be built first.

Run `presto build <name of your container>` to start building the image. This
process can take a while. You should get a message when the image is done
building.

This process will take time to complete. On my personal machine it took 8-10 minutes but it might take more on other systems. You can leave this running in the background until it has completed

```console
presto build lmrt
```

```bash
emily@VM:~/.../LMRt-container$ presto build lmrt
Building the image.... This might take a while
```

When the image has finished building you should see a lot of Docker logs as well as the following message
`Building lmrt image complete`

We are now ready to start running the reconstruction model!
## [Next](https://fossilizedcontainers.github.io/fossilized-controller/run_lmrt.html)
