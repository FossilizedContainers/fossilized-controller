# Fossilized Controller

This repository contains a command line interface used to help Paleoclimatologists containerize their code in order to make collaboration easier.

### Use case 1:
~~~bash
# command to create a Dockerfile in the current directory
$ presto create

# command to build an image using the Dockerfile created above
$ presto build imageName

# command to upload the built image to the docker repository
$ presto upload
~~~

### Use case 2:
