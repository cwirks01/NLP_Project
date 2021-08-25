# syntax=docker/dockerfile:1
FROM python:3-alpine
FROM ubuntu

LABEL name nlp_project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly language processor designed for reconnaissance."

WORKDIR /NLP_Project

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git

RUN mkdir /root/.ssh/
# Copy over private key, and set permissions
# Warning! Anyone who gets their hands on this image will be able
# to retrieve this private key file from the corresponding image layer
ADD id_ed25519.pub /root/.ssh/id_ed25519.pub

# Create known_hosts
RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN git clone git@github.com:cwirks01/NLP_Project.git

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /NLP_Project
CMD [ "python", "-m" , "main", "run", "--host=0.0.0.0"]