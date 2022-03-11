---
title: "Alpha Demo Use Case 2"
nav_order: 52
keywords: demo
tags: [demo]
sidebar: index_sidebar
permalink: alpha_uc2.html
summary: A page on the second use case of the Alpha Demo
---

For our second alpha demo use case, we will focus on accessing an already made
container. This shows how a scientist would find a model someone else made and
view it themselves and avoid having to install many dependencies.

### 1. Find an existing model they would like to access on Docker Hub

For this demo we are going to access the LMRt model that we created in the
previous use case. The link can be found
[here](https://hub.docker.com/r/fossilizedcontainers/lmrt-demo)

### 2. Download the model
Use the `presto download` command to download the LMRt container.
```console
presto download fossilizedcontainers/lmrt-demo
```

### 3 + 4. Run the model

#### 3 + 4.1 Prerequisites
Download the following metadata and input files before running the container:
```bash
alpha@demo:~$ wget https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/configs.yml
```
```bash
alpha@demo:~$ wget https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/metadata.json
```

We are now ready to run our container using our `presto run <image name>`
command. After the model finishes you should receive a zip file that has the
output files from the model.

In a separate terminal you can run `docker logs --follow $(docker ps -q)` after
you run the below command to follow what is happening inside of the container in
real time.
```console
presto run lmrt-demo
```
```bash
alpha@demo:~/.../client$ presto run lmrt-demo
Running the container...
{'Status': 'running', 'Running': True, 'Paused': False, 'Restarting': False, 'OOMKilled': False, 'Dead': False, 'Pid': 86211,
'ExitCode': 0, 'Error': '', 'StartedAt': '2022-03-11T00:58:10.323020527Z', 'FinishedAt': '0001-01-01T00:00:00Z'}
Output files successfully saved at ./response_data.zip
```

### 5. Receive and view output files
When you check your files you should see a new zip archive `response_data.zip`.
You can then unzip the archive and view your output files.

### 6. Stop and clean out the resulting container

#### 6.1 Display all containers
Run `presto display` to get the name of your container:
```bash
alpha@demo:~/.../client$ presto display
List of containers:
Container Name:/interesting_tereshkova       Container Image:['alpha-demo:latest']
```
#### 6.2 Stop a container
Copy the name (without the `/`) and run `presto stop`
```bash
alpha@demo:~/.../client$ presto stop interesting_tereshkova
The container was successfully stopped
```

#### 6.3 Delete stopped containers
Now clean up any stopped container using `presto clean`
```bash
alpha@demo:~/.../client$ presto clean
All stopped containers have been deleted!
RESULT:
{'ContainersDeleted': ['a81ccead7aca5be0b961a69a9154c0d748ddf228808136e9a89d3f951ba8fac2', 'aaa7cf38c9142af216a5bb39f50fa9398e65df1f96e6a96b25d92121d3195cbf', 'efb7f7cdc63371c71fe967f60821b3353705e0535dc1aaf07a8b76e4a3ea6bd6', '6161f111c4509aa6eaf63d1b814b28690b7e7c9cd0ee24b227c975c6c4920f5a', '57aa0c510fb93583f1436845c00ccaffe57d2889db095dc48a9a069b04379818', '7b4dbfea4f7ce5d0218884e50b32123e4a1b75fbbcae4604e453ffdc8565701d'], 'SpaceReclaimed': 3122163131}
```
