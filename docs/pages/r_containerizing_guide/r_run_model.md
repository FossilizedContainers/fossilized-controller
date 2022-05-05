---
title: "Run Container"
keywords: guide
tags: [guide]
sidebar: index_sidebar
permalink: r_run_model.html
summary: Running your newly build container
---


## 1. Verify files
When you are ready to run your container, navigate to your `Client` folder. It should still look like below.

```
├── Client
├── metadata.json
├── params.json
```

## 2. Run the model
We are now ready to run our container using our `presto run <image name>`
command. After the model finishes you should receive a zip file that has
the output files from the model.

**If you experience errors at this step and need to do presto run again, make sure you are doing [Step 5](https://fossilizedcontainers.github.io/fossilized-controller/clean_containers.html) at the same time**

In a separate terminal, you can run

```console
docker logs --follow $(docker ps -q)
```

after you run the below command to follow what is happening inside of the container in real time. This only works if you have one container active at the moment. Otherwise, run `docker ps` and copy the id of the most recent container.

```console
presto run model
```

```console
mumbi@WSL:~/.../client$ presto run demo
Running the container...
{'Status': 'running', 'Running': True, 'Paused': False, 'Restarting': False, 'OOMKilled': False, 'Dead': False,
'Pid': 86211, 'ExitCode': 0, 'Error': '', 'StartedAt': '2022-03-11T00:58:10.323020527Z', 'FinishedAt': '0001-01-01T00:00:00Z'}
Output files successfully saved at ./response_data.zip
```

## 3. Verify response data
When you check your files you should see a new zip archive `response_data.zip`.
You can then unzip the archive and view your output files.

## 4. Clean up the container
It is important that you **do not** skip this step. Click next to access the instructions.

## [Next](https://fossilizedcontainers.github.io/fossilized-controller/clean_containers.html)
