---
title: "Alpha Demo Use Case 1"
nav_order: 4
keywords: demo
tags: [demo]
sidebar: index_sidebar
permalink: alpha_uc1.html
summary: A page on the first use case of the Alpha Demo
---

For our first alpha demo use case, we will focus on container creation. This shows how a scientist would take their model and containerize it for others to access


### 1. Going to the folder where the construction is located
verify that all files needed for the container are present
```console
alpha@demo:~/.../alpha-demo$ cd LMRt-container/
alpha@demo:~/.../LMRt-container$ ls
data  main.py
```

### 2. Modify the project to make a presto ready container

#### 2.1 Adding the adapter library
Download the adapter library to the same directory as your main file
```bash
wget https://raw.githubusercontent.com/FossilizedContainers/fossilized-controller/trunk/python-adapter/adapter.py
```
An example of a main file modified for adapter libraries can be found [here](https://github.com/FossilizedContainers/fossilized-controller/blob/trunk/LMRt-example/LMRt-container/main.py)

Your folder should now look like this.
```console
alpha@demo:~/.../alpha-demo$ cd LMRt-container/
alpha@demo:~/.../LMRt-container$ ls
adapter.py  data  main.py
```

#### 2.2 Adding environment file to model
In order for the container to create the specific anaconda enviornment to you, a file is needed that lists every pip and anaconda dependency. An example file looks like this.

Make sure you name the file `presto_environment.yml`
```yaml
name: presto_container
channels:
  - defaults
  - conda-forge
dependencies:
  - r-base=4.1
  - pip=21.2.4
  - python=3.9.7
  - cartopy
  - pyspharm
  - jupyterlab
  - pip:
    - requests==2.27.1
    - urllib3==1.26.8
    - LMRt
    - Flask
```

Your folder should now look like this.
```console
alpha@demo:~/.../alpha-demo$ cd LMRt-container/
alpha@demo:~/.../LMRt-container$ ls
adapter.py  data  main.py  presto_environment.yml
```

After this you are ready to start creating your container

### 3. Call presto create
Stay in the folder your reconstruction is in and call `presto create` and answer the prompted questions
```
presto create
```

```console
alpha@demo:~/.../LMRt-container$ presto create
What is the command to run your main file?
Here are some examples:
- python3 main.py
- r main.R
- sh main.sh

> : python3 main.py
Dockerfile created!
```

You should now see a Dockerfile in your directory that looks like the following
```console
alpha@demo:~/.../LMRt-container$ ls
adapter.py  data  Dockerfile  main.py  presto_environment.yml
alpha@demo:~/.../LMRt-container$
```
```Dockerfile
FROM continuumio/anaconda3

RUN conda update -n base -c defaults conda

# setup conda environment
COPY presto_environment.yml .
RUN conda env create -f presto_environment.yml
RUN echo "conda activate presto_container" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
RUN conda activate presto_container

# copy all files to the root directory of the container
COPY . /

# run the command in the context of the environment we made
CMD conda run --no-capture-output -n presto_container python3 main.py
```

### 4. Build the image
More information about what images are can be found [here](). Images are essentially what your container uses to run so they need to be built first. Run `presto build <name of your container>` to start building the image. This process can take a while. You should get a message when the image is done building
```
presto build alpha-demo
```
```console
LMRt-container$ presto build alpha-demo
Building the image.... This might take a while
alpha-demo has been successfully built
```

### 5. Uploading an image to Dockerhub
`presto upload <image-name>`

### 6. Prepare files for the container

#### 6.1 Make a new folder
For this part of the demo I suggest going into a seperate folder outside of your model
```console
alpha@demo:~/.../alpha-demo$ mkdir client
alpha@demo:~/.../alpha-demo$ cd client
```
#### 6.2 Make sure you have the files you want to send to the container
In the case for our model, we only are sending the `configs.yml` file
```console
alpha@demo:~/.../client$ ls
configs.yml
```

#### 6.3 Create our metadata file
In order for our controller to communicate properly with the container, you need to create a metadta file. This is in JSON format and gives the model your parameters as well as input files. Below is an example of our `metadata.json` file.

Our first parameter is `recon_iterations` which determines how many times we iterate through an algorithm the model depends on.

Our second parameter is `figure_type` here we can specify if we want a `graph` or `map` to be produced.

Our final parameter is the directory where we want our output files to be saved in `./recon`

For the inputs, we are only sending our `config.yml` file found [here](https://github.com/FossilizedContainers/fossilized-controller/blob/trunk/LMRt-example/configs.yml)
```JSON
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

Your directory should now look like
```console
alpha@demo:~/.../client$ ls
configs.yml  metadata.json
```
### 7. Run the model
We are now ready to run our container using our `presto run <image name>` command. After the model finishes you should receive a zip file `` that has the output files from the model.

In a seperate terminal you can run `docker logs --follow $(docker ps -q)` after you run the below command to follow what is happening inside of the container in real time.
```
presto run alpha-demo
```
```console
alpha@demo:~/.../client$ presto run alpha-demo
Running the container...
{'Status': 'running', 'Running': True, 'Paused': False, 'Restarting': False, 'OOMKilled': False, 'Dead': False, 'Pid': 86211, 'ExitCode': 0, 'Error': '', 'StartedAt': '2022-03-11T00:58:10.323020527Z', 'FinishedAt': '0001-01-01T00:00:00Z'}
Output files successfully saved at ./response_data.zip
```

### 8. View reconstruction files
When you check your files you should see a new zip archive `response_data.zip`. You can then unzip the archive and view your output files

### 9. Clean up the container
Run `presto display` to get the name of your container
```console
alpha@demo:~/.../client$ presto display
List of containers:
Container Name:/interesting_tereshkova       Container Image:['alpha-demo:latest']
```

Copy the name (without the `/`) and run `presto stop`
```console
alpha@demo:~/.../client$ presto stop interesting_tereshkova
The container was successfully stopped
```

Now clean up any stopped container using `presto clean`
```console
alpha@demo:~/.../client$ presto clean
All stopped containers have been deleted!
RESULT:
{'ContainersDeleted': ['a81ccead7aca5be0b961a69a9154c0d748ddf228808136e9a89d3f951ba8fac2', 'aaa7cf38c9142af216a5bb39f50fa9398e65df1f96e6a96b25d92121d3195cbf', 'efb7f7cdc63371c71fe967f60821b3353705e0535dc1aaf07a8b76e4a3ea6bd6', '6161f111c4509aa6eaf63d1b814b28690b7e7c9cd0ee24b227c975c6c4920f5a', '57aa0c510fb93583f1436845c00ccaffe57d2889db095dc48a9a069b04379818', '7b4dbfea4f7ce5d0218884e50b32123e4a1b75fbbcae4604e453ffdc8565701d'], 'SpaceReclaimed': 3122163131}
```
