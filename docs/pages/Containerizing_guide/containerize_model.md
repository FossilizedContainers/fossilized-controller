---
title: "Containerizing a model"
keywords: guide
tags: [guide]
sidebar: index_sidebar
permalink: containerize_model.html
summary: Containerize your reconstruction model
---

For this step, you will want to navigate back to your `Container` folder.

## 1. Verify files
Make sure your folder has all of the necessary files from before.
```
Container
├── adapter.py
├── data
│   ├── py4493.pk
│   ├── ad3010.pk
│   ├── adverse30501.pk
├── main.py
├── utils.py
├── presto_environment.yml
```

## 2. Create the Dockerfile
A Dockerfile is a file that is essentially a list of instructions Docker uses to create a container. Luckily, we don't need to know much about how to create the file by hand as `presto create` does it for us! All it takes in is the language we are using and the file that holds all of our reconstruction code.

```
presto create
```

```console
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
```
Container
├── adapter.py
├── data
│   ├── py4493.pk
│   ├── ad3010.pk
│   ├── adverse30501.pk
├── Dockerfile
├── main.py
├── utils.py
├── presto_environment.yml
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

If you didn't change the name of your environment files, you will want to make sure you edit the Dockerfile and change the names of `presto_environment.yml` and `presto_container`

## 3. Build the Docker image

More information about what Docker Images are can be found
[here](/docker.html#docker-images). Images are essentially what your container uses to run so they need to be built first.

Run `presto build <name of your container>` to start building the image. This
process can take a while. You should get a message when the image is done
building.

This process will take time to complete. On my personal machine it took 8-10 minutes but it might take more on other systems. You can leave this running in the background until it has completed

```console
presto build model
```

```console
emily@VM:~/.../LMRt-container$ presto build model
Building the image.... This might take a while
```

When the image has finished building you should see a lot of Docker logs as well as the following message
`Building model image complete`

We are now ready to start running the reconstruction model!
## [Next](https://fossilizedcontainers.github.io/fossilized-controller/run_model.html)
