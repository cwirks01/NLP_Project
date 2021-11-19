# syntax=docker/dockerfile:1
FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install nginx -y



RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available && \
    mkdir -pv /static && \
    mkdir -pv /etc/nginx/conf.d && \
    mkdir -pv /etc/nginx/ssl/live/certs && \
    mkdir -pv /var/www/html/ && \
    chown -R root:root /etc/nginx/ssl/live/certs && \
    chmod -R 600 /etc/nginx/ssl/live/certs

COPY /NLP_Project/services/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY /NLP_Project/services/nginx/nginx.conf /etc/nginx/sites-available/nginx.conf
COPY /NLP_Project/services/nginx/index.html /var/www/html/

# Remove default nginx static assets
EXPOSE 80
EXPOSE 443

RUN rm /etc/nginx/sites-enabled/*
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/ 


CMD ["nginx"]