# docker-movie-cache-server

動画をキャッシュするサーバ

===

## Build

```
$ docker build --rm -t hideyuki/movie-cache-server:0.1 ./
``` 
## Run

Interactive

```
$ docker run -i -t --name daily -p 10022:22 hideyuki/movie-cache-server:0.1 /bin/bash
root@289241d88367:/# 
```

Daemon

```
$ docker run -d --name daily -p 10022:22 hideyuki/movie-cache-server:0.1
```

## Push to Docker Hub

```
$ docker login    # if you need
$ docker push hideyuki/movie-cache-server:0.1
```