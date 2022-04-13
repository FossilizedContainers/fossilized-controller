---
title: "Containerizing LMRt"
keywords: lmrt
tags: [lmrt]
sidebar: index_sidebar
permalink: run_lmrt.html
summary: A page on containerizing LMRt
---

Now that we have containerized LMRt, we can start communicating with it. For this step we will want to leave the current directory we're in and make a new folder named `client`. This can be anywhere.


### 1. Prepare files for the container
For LMRt we are only going to send one file which is our `configs.yml` file. Sending it into the container, rather than building the container with the file present, will allow us to make changes to our configuration without having to completely rebuild the container.

You can directly download the file from [here](https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/LMRt-example/configs.yml)

---

Your directory should now look like below
```bash
emily@VM:~/.../client$ ls
configs.yml
```

### 2 Create our metadata file
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
[here](https://github.com/FossilizedContainers/fossilized-controller/blob/trunk/LMRt-example/configs.yml)
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
```bash
emily@VM:~/.../client$ ls
configs.yml  metadata.json
```

### 3. Run the model
We are now ready to run our container using our `presto run <image name>`
command. After the model finishes you should receive a zip file that has
the output files from the model.

**If you experience errors at this step and need to do presto run again, make sure you are doing [Step 5](https://fossilizedcontainers.github.io/fossilized-controller/run_lmrt.html#5-clean-up-the-container) at the same time**

In a separate terminal, you can run `docker logs --follow $(docker ps -q)` after
you run the below command to follow what is happening inside of the container in real time.

```console
presto run lmrt
```

```bash
emily@VM:~/.../client$ presto run demo
Running the container...
{'Status': 'running', 'Running': True, 'Paused': False, 'Restarting': False, 'OOMKilled': False, 'Dead': False,
'Pid': 86211, 'ExitCode': 0, 'Error': '', 'StartedAt': '2022-03-11T00:58:10.323020527Z', 'FinishedAt': '0001-01-01T00:00:00Z'}
Output files successfully saved at ./response_data.zip
```

### 4. View reconstruction files
When you check your files you should see a new zip archive `response_data.zip`.
You can then unzip the archive and view your output files. This should be an image of a figure and the recon folder.

### 5. Clean up the container
If you have noticed your computer has slowed down, you are not alone. The containers take up a good amount of computing resources so we want to make sure that everytime we use `presto run` that we clean up the containers.

#### 5.1 Display all containers
Run `presto display` to get the name of your container:
```bash
emily@VM:~/.../client$ presto display
List of containers:
Container Name:/interesting_tereshkova       Container Image:['alpha-demo:latest']
```

#### 5.2 Stop a container
Copy the name (without the `/`) and run `presto stop`:
```bash
emily@VM:~/.../client$ presto stop interesting_tereshkova
The container was successfully stopped
```

#### 5.3 Delete stopped containers
Now clean up any stopped container using `presto clean`:
```bash
emily@VM:~/.../client$ presto clean
All stopped containers have been deleted!
RESULT:
{'ContainersDeleted':
    ['a81ccead7aca5be0b961a69a9154c0d748ddf228808136e9a89d3f951ba8fac2',
    'aaa7cf38c9142af216a5bb39f50fa9398e65df1f96e6a96b25d92121d3195cbf',
    'efb7f7cdc63371c71fe967f60821b3353705e0535dc1aaf07a8b76e4a3ea6bd6',
    '6161f111c4509aa6eaf63d1b814b28690b7e7c9cd0ee24b227c975c6c4920f5a',
    '57aa0c510fb93583f1436845c00ccaffe57d2889db095dc48a9a069b04375818',
    '7b4dbfea4f7ce5d0218884e50b32123e4a1b75fbbcae4604e453ffdc8565701d'],
'SpaceReclaimed': 3122163131}
```

You have no successfully containerized and run LMRt!
