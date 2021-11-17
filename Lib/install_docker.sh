#!/bin/bash

sudo yum update -y

sudo yum install docker -y

sudo service docker start

sudo usermod -a -G docker $USER;

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose;

sudo chmod +x /usr/local/bin/docker-compose;

docker-compose version;