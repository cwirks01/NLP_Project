# syntax=docker/dockerfile:1
FROM nginx:1.19-alpine

ARG DEBIAN_FRONTEND=noninteractive

RUN rm /etc/nginx/conf.d/default.conf 

COPY /NLP_Project/services/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available && \
    mkdir -pv /static 

WORKDIR /etc/nginx/html
# Remove default nginx static assets
RUN rm -rf ./*

RUN ln -s /etc/nginx/sites-available/regex.testing-dev.dev.conf /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/nlp.testing-dev.dev.conf /etc/nginx/sites-enabled/