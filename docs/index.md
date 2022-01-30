---
title: "Fossilized Controller"
keywords: quickstart
tags: [getting_started]
sidebar: index_sidebar
permalink: index.html
summary: We are creating a tool to help scientists containerize their code.
---

## Dependencies
* Python
* Pip
* Docker

Make sure you have the latest versions of each installed before using our tool

## Creating a Container

Follow the instructions below for a quick introduction of our tool.

### 1. Download our tool
The direct link for the tool can be found [here](https://github.com/FossilizedContainers/tech-demo/raw/master/presto/dist/presto-0.0.1-py3-none-any.whl). If you
are using a Linux distribution then you can run the following command
```bash
wget https://github.com/FossilizedContainers/tech-demo/raw/master/presto/dist/presto-0.0.1-py3-none-any.whl
```

### 2. Install the tool through pip
```bash
pip install presto-0.0.1-py3-none-any.whl
```

### 3. Run the tool's Dockerfile creation
```bash
presto create
```

From there you will be prompted for the OS you would like to use. For this example you can use `alpine`
Afterwards will be a prompt asking for what message you would like to display. For this example you can use `Hello World!`

This will show the Dockerfile
```Dockerfile
FROM alpine
CMD ["echo", "Hello World!"]
```

### 4. Download or create the Dockerfile
You can either copy and paste the example Dockerfile from above into a new file named `Dockerfile` or you can download it from our Github
```bash
wget https://raw.githubusercontent.com/FossilizedContainers/tech-demo/master/C4/Dockerfile
```

### 5. Run the presto run command
```bash
presto run
```

You should see the following output of your container running
```
Building image from Dockerfile...

Finished building image...

Running the container...

Hello World!
```

### 6. Clean up your containers
You can run the following command to stop and delete the container you just built.
{% include note.html content="Be careful when running this command as it will stop and delete **ALL** containers" %}
```bash
presto clean
```
