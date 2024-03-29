#!/bin/sh

docker-compose down
docker-compose build
docker-compose up -d

echo "+++++ CLEAN UP +++++"
docker rmi -f $(docker images -f "dangling=true" -q)