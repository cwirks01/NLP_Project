#!/bin/bash

sudo docker image prune -f
sudo docker volume prune -f

sudo docker-compose down;

sudo docker network create nlp_project_default;

git pull;

sudo docker-compose build --no-cache;

sudo docker-compose up --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d; 

sudo docker ps;
