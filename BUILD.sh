#!/bin/bash

docker-compose down;

sudo docker network create nlp_project_default;

git pull;

sudo docker-compose build --build-arg NTC_TOKEN="$(echo $NTC_TOKEN)";

sudo docker-compose up -b; 
