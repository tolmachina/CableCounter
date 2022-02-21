#!bin/sh
docker build --tag pyja .
docker images
docker run --rm --publish 8000:5000 pyja 