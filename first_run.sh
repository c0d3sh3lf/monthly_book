#!/bin/sh
docker-compose build
docker-compose up -d
sleep 2s
docker-compose run web python manage.py migrate