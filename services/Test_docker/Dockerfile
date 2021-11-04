# syntax=docker/dockerfile:1
FROM ubuntu/nginx:1.18-21.04_beta

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get dist-upgrade
RUN apt-get install -y build-essential
RUN apt-get install -y snapd

# FROM certbot/certbot:latest

RUN apt remove certbot && \
    apt-get install -y certbot python3-certbot-nginx
    # snap install --classic certbot && \
    # ln -s /snap/bin/certbot /usr/bin/certbot

# RUN snap install core
# RUN snap refresh core

# FROM nginx:1.19-alpine

# RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available && \
    mkdir -pv /static && \
    mkdir -pv /etc/nginx/ssl/live/certs/


RUN certbot --nginx -m cwirks01@gmail.com
RUN certbot certonly --webroot --webroot-path /etc/nginx/ssl/live/certs/ -d testing-dev.dev -m cwirks01@gmail.com

WORKDIR /etc/nginx/html
# Remove default nginx static assets
RUN rm -rf ./*

RUN ln -s /etc/nginx/sites-available/regex.testing-dev.dev.conf /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/nlp.testing-dev.dev.conf /etc/nginx/sites-enabled/