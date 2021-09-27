#!/bin/bash

sudo docker image prune -f
sudo docker volume prune -f

sudo docker-compose down;

sudo docker network create nlp_project_default;

git pull;

sudo docker-compose build --no-cache --build-arg GIT_TOKEN="$$GIT_TOKEN";

sudo docker-compose up -d; 
