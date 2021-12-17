# syntax=docker/dockerfile:1
FROM ubuntu

WORKDIR /usr/nginx/html

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install nginx -y
RUN apt-get install vim -y

RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available && \
    mkdir -pv /static && \
    mkdir -pv /etc/nginx/conf.d && \
    mkdir -pv /etc/nginx/ssl/live/certs && \
    mkdir -pv /var/www/html/ && \
    mkdir -pv /usr/nginx/html/static && \
    chown -R root:root /etc/nginx/ssl/live/certs && \
    chmod -R 755 /etc/nginx/ssl/live/certs

# RUN rm /etc/nginx/conf.d/*
RUN rm /etc/nginx/sites-available/*

COPY /NLP_Project/services/nginx/nginx.conf /etc/nginx/sites-enabled/default
COPY /NLP_Project/services/nginx/index.html /var/www/html/
COPY /NLP_Project/static/* /usr/nginx/html/static/ 
COPY /NLP_Project/templates/NOT_FOUND.html /var/www/html/NOT_FOUND.html

# Remove default nginx static assets
EXPOSE 80
EXPOSE 443

# RUN rm /etc/nginx/sites-enabled/*
# RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf

CMD ["nginx", "-g", "daemon off;"]