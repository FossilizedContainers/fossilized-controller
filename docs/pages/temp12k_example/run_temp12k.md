---
title: "Containerizing LMRt"
keywords: temp12k
tags: [temp12k]
sidebar: index_sidebar
permalink: run_temp12k.html
summary: A page on containerizing Temp12k
---

Now that we have containerized LMRt, we can start communicating with it. For this step we will want to leave the current directory we're in and make a new folder named `client`. This can be anywhere.


## 1. Prepare files for the container
For LMRt we are only going to send one file which is our `configs.yml` file. Sending it into the container, rather than building the container with the file present, will allow us to make changes to our configuration without having to completely rebuild the container.

You can directly download the file from [here](https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/configs.yml)

---

Your directory should now look like below
```console
emily@VM:~/.../client$ ls
configs.yml
```

## 2. Create our metadata file
In order for our controller to communicate properly with the container, you need
to create a metadata file. This is in JSON format and gives the model your
parameters as well as input files. Below is an example of our `metadata.json`
file:

  1. Our first parameter is `recon_iterations` which determines how many times
  we iterate through an algorithm the model depends on.

  2. Our second parameter is `figure_type`; here we can specify if we want a
  `graph` or `map` to be produced.

  3. Our final parameter is the directory where we want our output files to be
  saved in `./recon`.

For the inputs, we are only sending our `config.yml` file found
[here](https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/configs.yml)
```json
{
    "parameters": {
        "recon_iterations": 1,
        "figure_type": "graph",
        "job_dirpath": "./recon"
    },
    "inputs": {
        "configs": "configs.yml"
    }
}
```

---

Your directory should now look like
```console
emily@VM:~/.../client$ ls
configs.yml  metadata.json
```

## 3. Run the model
We are now ready to run our container using our `presto run <image name>`
command. After the model finishes you should receive a zip file that has
the output files from the model.

**If you experience errors at this step and need to do presto run again, make sure you are doing [Step 5](https://fossilizedcontainers.github.io/fossilized-controller/clean_containers.html) at the same time**

In a separate terminal, you can run `docker logs --follow $(docker ps -q)` after
you run the below command to follow what is happening inside of the container in real time.

```console
presto run lmrt
```

```console
emily@VM:~/.../client$ presto run demo
Running the container...
{'Status': 'running', 'Running': True, 'Paused': False, 'Restarting': False, 'OOMKilled': False, 'Dead': False,
'Pid': 86211, 'ExitCode': 0, 'Error': '', 'StartedAt': '2022-03-11T00:58:10.323020527Z', 'FinishedAt': '0001-01-01T00:00:00Z'}
Output files successfully saved at ./response_data.zip
```

## 4. View reconstruction files
When you check your files you should see a new zip archive `response_data.zip`.
You can then unzip the archive and view your output files. This should be an image of a figure and the recon folder.

## 5. Clean up the container
It is important that you **do not** skip this step. Click next to access the instructions.


## [Next](https://fossilizedcontainers.github.io/fossilized-controller/clean_containers.html)
