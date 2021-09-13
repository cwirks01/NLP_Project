#!/bin/bash

sudo docker-compose build --build-arg NTC_TOKEN="$(echo $NTC_TOKEN)"
sudo docker-compose up -b
