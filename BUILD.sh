#!/bin/bash

docker-compose down;

docker system prune -f -a
docker volume prune -f

docker network create nlp_project_default;

sudo git pull;

docker-compose build --no-cache;

docker-compose up -d; 

docker ps;
