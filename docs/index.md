---
title: "Fossilized Controller"
keywords: quickstart
tags: [getting_started]
sidebar: index_sidebar
permalink: index.html
summary: A quick installation guide for the Fossilized Controller
---

*This was tested on a Mint Linux distribution and Windows WSL 2.*

## Download Dependencies

### Download the latest versions of the following software:
* Python 3
* Pip
  - wheel
  - Flask
  - requests
  - LMRt
  - urllib3
* [Docker](/docker_install.html)

## Installing the Fossilized Controller

Follow the instructions below for a quick introduction of our tool.

### 1. Download our tool
We currently do not have a pip distribution so it needs to be created and installed manually. The following instructions are based on [this](https://realpython.com/python-wheels/) article.

Start by cloning our tool and moving into the controller directory
```console
git clone https://github.com/FossilizedContainers/fossilized-controller.git

cd controller
```

### 2. Set up the wheel
```console
python setup.py bdist_wheel
```

#### 2.2 Check the name of the wheel
```console
user@VM:~/.../controller$ ls dist/
presto-0.0.1-py3-none-any.whl
```

### 3. Install the tool through pip
```console
pip install dist/presto-0.0.1-py3-none-any.whl
```

### 4. Test the tool
Run the following command to make sure that the tool is properly installed
```console
presto guide
```

### 5. Start containerizing!
You can view our [LMRT Example](https://fossilizedcontainers.github.io/fossilized-controller/gathering_files.html) tab to see an example of containerizing LMRt.

You can also view our other tabs if you would like to start containerizing your model from scratch, with LMRt as the guiding example.

Email er883@nau.edu for any questions regarding the setup
