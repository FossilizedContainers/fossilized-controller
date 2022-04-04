---
title: "Fossilized Controller"
keywords: quickstart
tags: [getting_started]
sidebar: index_sidebar
permalink: index.html
summary: A quick installation guide for the Fossilized Controller
---

## Dependencies
* Python3
  - wheel
* Pip
* Docker

Make sure you have the latest versions of each installed before using our tool.

This was tested on a Mint Linux distribution.

## Installing the Fossilized Controller

Follow the instructions below for a quick introduction of our tool.

### 1. Download our tool
We currently do not have a pip distribution so it needs to be created and installed manually. The following instructions are based on [this](https://realpython.com/python-wheels/) article.

Start by cloning our tool and moving into the controller directory
```bash
git clone https://github.com/FossilizedContainers/fossilized-controller.git

cd controller
```

### 2. Set up the wheel
```bash
python setup.py bdist_wheel
```

#### 2.2 Check the name of the wheel
```bash
user@VM:~/.../controller$ ls dist/
presto-0.0.1-py3-none-any.whl
```

### 3. Install the tool through pip
```bash
pip install dist/presto-0.0.1-py3-none-any.whl
```

### 3. Test the tool
Run the following command to make sure that the tool is properly installed
```bash
presto guide
```

### 4. Start containerizing!
You can view our [Alpha Demo](http://localhost:4000/alpha_uc1.html) tab to see an example of containerizing LMRt.

You can also view our other tabs if you would like to start containerizing your model from scratch, with LMRt as the guiding example.

Email er883@nau.edu for any questions regarding the setup
