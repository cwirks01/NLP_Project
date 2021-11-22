# syntax=docker/dockerfile:1
FROM python:3.8-alpine
FROM ubuntu

WORKDIR /usr/nginx/html

RUN mkdir -pv /etc/nginx/sites-enabled/nlp_project

RUN mkdir -pv /usr/nginx/html/nlp_project

COPY /services/nginx/default.conf /etc/nginx/sites-enabled/nlp_project
COPY /services/nginx/default.conf /etc/nginx/sites-available/nlp_project
COPY /services/nginx/backend-not-found.html /var/www/html/backend-not-found.html

ARG TOKEN
ARG DEBIAN_FRONTEND=noninteractive
ARG ssh_prv_key
ARG ssh_pub_key
ARG passphrase
ARG git_username
ARG git_password

LABEL name nlp_project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly fast language processor designed for initial analysis."

ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0

# Update aptitude with new repo
RUN apt-get update

RUN mkdir -p /root/.ssh && \
    mkdir -p ~/logs 

RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub

# Create known_hosts
# Add github key
# Authorize SSH Host
RUN touch /root/.ssh/known_hosts && \
    touch /root/.ssh/config && \
    # Install software
    apt-get install -y git && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

# Add the keys and set permissions
RUN chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub && \
    echo "    IdentityFile /root/.ssh/id_rsa" >> /etc/ssh/ssh_config && \
    eval `ssh-agent`
    
# Add the keys and set permissions
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config


# variabels in Dockerfile and docker-compose.yml need to be escaped out with $$
RUN echo "########################### Cloning GITHUB Repo ###########################"

COPY . .

RUN apt-get install -y python3-pip && \
    apt-get install -y python3-tk && \
    apt-get install -y vim && \
    pip3 install -U pip setuptools wheel && \
    pip install blis

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN pip3 install -U pip setuptools wheel &&\
    pip3 install -U spacy && \
    python3 -m spacy download en_core_web_sm

EXPOSE 5000

RUN realpath ./ && ls ./ && ls -l ../
