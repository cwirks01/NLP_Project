# syntax=docker/dockerfile:1
FROM python:3.8
FROM ubuntu

ARG TOKEN
ARG DEBIAN_FRONTEND=noninteractive

LABEL name nlp_project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly fast language processor designed for initial analysis."

WORKDIR /NLP_Project

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git && \
    apt-get install -y python3-pip && \
    apt-get install -y python3.8 python3-tk && \
    apt-get install -y xvfb

# Create known_hosts
# Add github key
# Authorize SSH Host
RUN mkdir -p /NLP_Project/ssh && \
    chmod 0700 /NLP_Project/ssh && \
    touch /NLP_Project/ssh/known_hosts && \
    touch /NLP_Project/ssh/config && \
    ssh-keyscan -H github.com > /NLP_Project/ssh/known_hosts

# ERROR: _tkinter.TclError: couldn't connect to display "unix" (SOLVED)
RUN echo "export DISPLAY='localhost:0.0'" >> .bashrc && \
    echo "export DISPLAY=':0'" >> .bashrc && \
    echo "export MPLBACKEND='Agg'" >> .bashrc && \
    echo "s/^.*X11Forwarding.*$/X11Forwarding yes/" >> /etc/ssh/sshd_config && \
    echo "s/^.*X11UseLocalhost.*$/X11UseLocalhost no/" >> /etc/ssh/sshd_config

# Add the keys and set permissions
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /NLP_Project/ssh/config

RUN git clone https://$NTC_TOKEN@github.com/cwirks01/NLP_Project.git

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["python3", "main.py"]
