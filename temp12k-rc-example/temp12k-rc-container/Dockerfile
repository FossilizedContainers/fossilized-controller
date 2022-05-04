FROM rocker/tidyverse

#RUN conda update -n base -c defaults conda

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
# CMD Rscript main.R
