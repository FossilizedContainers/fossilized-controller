---
title: "Clean your containers"
keywords: guide
tags: [guide]
sidebar: index_sidebar
permalink: r_clean_containers.html
summary: Cleaning up after yourself
---

If you have noticed your computer has slowed down, you are not alone. The containers take up a good amount of computing resources so we want to make sure that everytime we use `presto run` that we clean up the containers.

## 1. Display all containers
Run `presto display` to get the name of your container:
```console
mumbi@WSL:~/.../client$ presto display
List of containers:
Container Name:/interesting_tereshkova       Container Image:['alpha-demo:latest']
```

## 2. Stop a container
Copy the name (without the `/`) and run `presto stop`:
```console
mumbi@WSL:~/.../client$ presto stop interesting_tereshkova
The container was successfully stopped
```

## 3. Delete stopped containers
Now clean up any stopped container using `presto clean`:
```console
mumbi@WSL:~/.../client$ presto clean
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
