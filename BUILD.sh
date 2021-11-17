#!/bin/bash

sudo docker-compose down;

sudo docker system prune -f
sudo docker volume prune -f

sudo docker network create nlp_project_default;

sudo git pull;

sudo docker-compose build --no-cache;

sudo docker-compose up -d; 

sudo docker ps;
