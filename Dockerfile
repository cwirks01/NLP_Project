# syntax=docker/dockerfile:1
FROM python:3.9.6-alpine
FROM ubuntu

ARG TOKEN
ARG DEBIAN_FRONTEND=noninteractive

LABEL name nlp_project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly language processor designed for reconnaissance."

WORKDIR /NLP_Project

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git && \
    apt-get install -y pip && \
    apt-get install -y tk-dev && \
    apt-get install python-tk

# Create known_hosts
# Add github key
# Authorize SSH Host
RUN mkdir -p /NLP_Project/ssh && \
    chmod 0700 /NLP_Project/ssh && \
    touch /NLP_Project/ssh/known_hosts && \
    touch /NLP_Project/ssh/config && \
    ssh-keyscan -H github.com > /NLP_Project/ssh/known_hosts

# Add the keys and set permissions
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" > /NLP_Project/ssh/config

RUN git clone https://${TOKEN}@github.com/cwirks01/NLP_Project.git

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /NLP_Project
CMD [ "python3", "-m" , "main.py"]