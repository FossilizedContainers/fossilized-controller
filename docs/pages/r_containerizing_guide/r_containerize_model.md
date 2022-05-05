---
title: "Containerizing a model"
keywords: guide
tags: [guide]
sidebar: index_sidebar
permalink: r_containerize_model.html
summary: Containerize your reconstruction model
---

For this step, you will want to navigate back to your `Container` folder.

## 1. Verify files
Make sure your folder has all of the necessary files from before.
```
Reconstruction
├── Container
│   ├── adapter.R
│   ├── main.R
│   ├── predetermined_inputs
│   │   ├── some_data.csv
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
- Rscript main.R
- sh main.sh

> : python3 main.py
Dockerfile created!
```
---

You should now see a Dockerfile in your directory:
```
Reconstruction
├── Container
│   ├── adapter.R
│   ├── Dockerfile
│   ├── main.R
│   ├── predetermined_inputs
│   │   ├── some_data.csv
```

The Dockerfile should look like the following:
```Dockerfile
FROM rocker/tidyverse

# Copy all files to the root directory of the container
COPY . /

# Download GitHub packages and their dependencies
RUN apt-get -y update
RUN apt-get -y install libcurl4-gnutls-dev libxml2-dev libssl-dev \
                       libudunits2-dev libgdal-dev gdal-bin libproj-dev \
                       proj-data proj-bin libgeos-dev libfontconfig1-dev \
                       libglpk-dev

RUN R -e 'install.packages(c("usethis", "devtools", "sf", "leaflet", "raster", \
                            "leafem", "pracma", "igraph", "egg", "httpuv", \
                            "rjson", "Rook"))'

RUN R -e 'devtools::install_github("neotomadb/neotoma2")'
RUN R -e 'remotes::install_github("nickmckay/lipdr")'
RUN R -e 'remotes::install_github("nickmckay/compositer")'
RUN R -e 'remotes::install_github("nickmckay/geochronr")'

SHELL ["/bin/bash", "--login", "-c"]

# run the command in the context of the environment we made
CMD Rscript main.R
```

***Add any GitHub packages HERE IN THE DOCKERFILE as pictured above***

## 3. Build the Docker image

More information about what Docker Images are can be found
[here](/docker.html#docker-images). Images are essentially what your container uses to run so they need to be built first.

Run `presto build <name of your container>` to start building the image. This
process can take a while. You should get a message when the image is done
building.

This process will take time to complete. On my personal machine it took 8-10 minutes but it might take more on other systems. You can leave this running in the background until it has completed.

```console
presto build model
```

```console
mumbi@WSL:~/.../r-container$ presto build model
Building the image.... This might take a while
```

Use this command to see the logs for the build process:
```console
docker build --no-cache --progress=plain -t <my-image> .
```

When the image has finished building you should see a lot of Docker logs as well as the following message
`Building model image complete`

We are now ready to start running the reconstruction model!
## [Next](https://fossilizedcontainers.github.io/fossilized-controller/run_model.html)
