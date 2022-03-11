---
title: "Docker Basics"
nav_order: 21
keywords: docker
tags: [docker, guide]
sidebar: index_sidebar
permalink: docker.html
summary: A short guide into how Docker containers work.
---

Docker is a service that allows you to construct and share computer
environments.

Docker does this through containers. Containers are instances of a computer
built from a Docker image.

A Docker image is a blueprint for how to run a container and the files that
belong to that container.

This tutorial will guide you on installing Docker on Ubuntu, how to view, create
and destroy Docker images on your machine, and how to view, run, and destroy
Docker containers on your machine.

Docker Hub is a website used to share containers. (Will our users need accounts
on Docker Hub?) (Will our users need to know how to pause/unpause or
stop/restart or kill Docker containers?) (Should we include information about
how to create a Dockerfile?) (Should we include information about how to
push a Docker image to Docker Hub?)

IMPORTANT: Docker images and containers can take up a lot of space, with the
latter taking up the most space. It’s important to be aware of how many images
and containers you have and to destroy the images and containers you no longer
need.

### Installing Docker on Linux

Run the following commands in your Linux terminal to install and use Docker
commands without sudo.

```bash
$ sudo apt-get update
```

```bash
$ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

```bash
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

```bash
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
```

```bash
$ sudo apt-get update
```

```bash
$ apt-cache policy docker-ce
```

```bash
$ sudo apt-get install docker-ce
```

Type and Enter “Y” when prompted


```bash
$ sudo systemctl status docker
```

“Ctrl + C” to quit


```bash
$ sudo usermod -aG docker {username}
```
```bash
$ su - {username}
```


### Docker Images

To view all Docker images use the command:

```bash
$ docker images
```

If this is your first time using Docker or you have no images, your output should look like this:



The first column, “REPOSITORY”, refers to the Docker Hub repository that holds the image and is the name of the Docker image. The second column, “TAG”, is a user-defined method to differentiate between images. It defaults to “latest”. The third column, “IMAGE ID”, is a unique identifier for that image. The fourth column, “CREATED”, states when the image was created. The fifth column, “SIZE”, refers to how large the image is, the units of measurement will be included in the column’s values.

To pull a Docker image from Docker Hub, all you need is the Docker image’s name and tag. For most cases, we can assume that the tag we want is “latest”. The command to pull a Docker image from Docker Hub is:

```bash
$ docker pull {IMAGE NAME}
```

To run a Docker image in a Docker container in interactive mode, use the command:

```bash
$ docker run -it {IMAGE ID} /bin/bash
```

You can use an image’s name instead of it’s ID. “-it” asks to start the container in interactive mode. “/bin/bash” gives an interactive shell for the container. For images built from the “ubuntu” Docker image, the “/bin/bash” argument is built into the “ubuntu” Dockerfile.

To destroy an image, use the following command:
```bash
$ docker rmi {IMAGEID}
```

You can acquire the image ID by listing all the Docker images on your machine with the command specified above.

### Docker Containers

To list all running Docker containers use the command:
```bash
$ docker ps
```

If this is your first time using Docker or you have no running containers, your output should look like this:



The first column, “CONTAINER ID”, refers to the unique ID for that container.

To list all containers, running or stopped, use the command:
```bash
$ docker ps -a
```

To exit and stop a Docker container started in interactive mode use the command:
```bash
$ exit
```

To connect back into a container use the command:
```bash
$ docker attach {CONTAINERID}
```

Using the “docker run” command will make a new container on top of the existing one. Do not do this.

To remove a container use the command:
```bash
$ docker rm {CONTAINERID}
```
