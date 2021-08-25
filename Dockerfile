# syntax=docker/dockerfile:1
FROM python:3-alpine
FROM ubuntu

ARG TOKEN
ARG ssh_prv_key
ARG ssh_pub_key

LABEL name nlp_project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly language processor designed for reconnaissance."

WORKDIR /NLP_Project

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git
RUN apt-get install -y pip

# Create known_hosts
# Add github key
# Authorize SSH Host
RUN mkdir -p /NLP_Project/ssh && \
    chmod 0700 /NLP_Project/ssh && \
    touch /NLP_Project/ssh/known_hosts && \
    touch /NLP_Project/ssh/config && \
    touch /NLP_Project/ssh/ssh_config && \
    ssh-keyscan -H github.com > /NLP_Project/ssh/known_hosts

# Add the keys and set permissions
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" > /NLP_Project/ssh/config && \
    echo "IdentityFile ~/.ssh/id_ed25519" > /etc/ssh/ssh_config && \
    echo "IdentityFile ~/.ssh/id_ed25519.pub" > /etc/ssh/ssh_config && \
    echo "$ssh_prv_key" > /NLP_Project/ssh/id_ed25519 && \
    echo "$ssh_pub_key" > /NLP_Project/ssh/id_ed25519.pub && \
    chmod 644 /NLP_Project/ssh/id_ed25519 && \
    chmod 644 /NLP_Project/ssh/id_ed25519.pub

RUN git clone https://${TOKEN}@github.com/cwirks01/NLP_Project.git

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /NLP_Project
CMD [ "python", "-m" , "main", "run", "--host=0.0.0.0"]