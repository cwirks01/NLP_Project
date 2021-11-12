# syntax=docker/dockerfile:1
FROM nginx:1.19-alpine

ARG DEBIAN_FRONTEND=noninteractive

RUN rm /etc/nginx/conf.d/default.conf 

COPY /NLP_Project/services/nginx/nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available && \
    mkdir -pv /static && \
    mkdir -pv /etc/nginx/ssl/live/certs && \
    chown -R root:root /etc/nginx/ssl/live/certs && \
    chmod -R 600 /etc/nginx/ssl/live/certs

WORKDIR /etc/nginx/html
# Remove default nginx static assets


RUN ln -s /etc/nginx/sites-available/regex.testing-dev.dev.conf /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/nlp.testing-dev.dev.conf /etc/nginx/sites-enabled/