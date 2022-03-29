---
title: "Downloading the Tool"
nav_order: 33
keywords:
tags: [documentation, basics]
sidebar: index_sidebar
permalink: downloading_tool.html
summary: A short guide for downloading presto.
---

### Downloading tool

### Setting up the wheel

for the wheel:
wget https://github.com/FossilizedContainers/fossilized-controller/blob/tech-demo-updates/controller/dist/presto-0.0.1-py3-none-any.whl

cd  /controller

python setup.py bdist_wheel

pip install presto-0.0.1-py3-none-any.whl

### Notes from alpha demo

* For WSL, run "sudo apt-get install" if you're having issues installing pip
* For WSL, replace `python setup.py bdist_wheel` with
`python3 setup.py bdist_wheel`

### Energies to focus on

* edge cases, test accuracy + performance + usable (how draw user pool to test
  project w/o prior knowledge of project using documentation) Melissa suggests
  to use Nick's graduate students as well for tester in addition to Michael Erb
  + different CS students since a variety of user pool can make documentation
  clearer and more effective
