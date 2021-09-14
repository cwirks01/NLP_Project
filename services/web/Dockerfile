# syntax=docker/dockerfile:1
FROM python:3.8-alpine
FROM ubuntu
FROM nginx

COPY ./services/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./services/nginx/default.conf /etc/nginx/sites-enabled/nlp_project
COPY ./services/nginx/default.conf /etc/nginx/sites-available/nlp_project
COPY ./services/nginx/backend-not-found.html /var/www/html/backend-not-found.html

ARG TOKEN
ARG DEBIAN_FRONTEND=noninteractive
ARG NTC_TOKEN

LABEL name nlp_project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly fast language processor designed for initial analysis."

WORKDIR /usr/nginx/html

ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-tk && \
    pip3 install -U pip setuptools wheel && \
    pip install blis

# Create known_hosts
# Add github key
# Authorize SSH Host
RUN mkdir -p /NLP_Project/ssh && \
    mkdir -p /NLP_Project/logs && \
    chmod 0700 /NLP_Project/ssh && \
    touch /NLP_Project/ssh/known_hosts && \
    touch /NLP_Project/ssh/config && \
    touch /.bashrc && \
    touch /etc/ssh/sshd_config && \
    ssh-keyscan -H github.com > /NLP_Project/ssh/known_hosts

# ERROR: _tkinter.TclError: couldn't connect to display "unix" (SOLVED)
# RUN echo "export DISPLAY='localhost:0.0'" >> /.bashrc && \
#     echo "export DISPLAY=':0'" >> /.bashrc && \
#     echo "export MPLBACKEND='Agg'" >> /.bashrc && \
#     echo "s/^.*X11Forwarding.*$/X11Forwarding yes/" >> /etc/ssh/sshd_config && \
#     echo "s/^.*X11UseLocalhost.*$/X11UseLocalhost no/" >> /etc/ssh/sshd_config

CMD echo "127.0.0.1 testing-dev.dev www.testing-dev.dev" >> /etc/hosts 

# Add the keys and set permissions
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /NLP_Project/ssh/config

CMD git clone https://${NTC_TOKEN}@github.com/cwirks01/NLP_Project.git

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN pip3 install -U pip setuptools wheel &&\
    pip3 install -U spacy && \
    python3 -m spacy download en_core_web_sm

COPY . .

CMD python3 -m main
