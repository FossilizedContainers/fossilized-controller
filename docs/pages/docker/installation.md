---
title: "Installing Docker"
nav_order: 22
keywords: docker
tags: [docker, guide]
sidebar: index_sidebar
permalink: docker_install.html
summary: How to install Docker.
---

## Installing Docker on Linux

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

## Installing Docker on Windows with Windows Subsystem for Linux, or WSL 2, Integration

### Definitive guide to downloading Docker on Windows with WSL Integration

*Follow the guide linked to install Docker Desktop and upgrade WSL 1 to WSL 2:*

[https://docs.docker.com/desktop/windows/wsl/](https://docs.docker.com/desktop/windows/wsl/)

### A General Outline to Install Docker Desktop with WSL Integration:

*Please follow the guide above. The sequence below details the general steps needed.*

1. Download Docker Desktop for Windows

2. Open Docker Desktop -> Settings -> Resources -> WSL Integration

3. Check WSL version with:
```console
wsl.exe -l -v
```
You will want to have WSL 2 downloaded.

4. Update WSL 1 to WSL 2 with the link below. It may take a while.

    [https://docs.microsoft.com/en-us/windows/wsl/install](https://docs.microsoft.com/en-us/windows/wsl/install)
