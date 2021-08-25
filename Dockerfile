# syntax=docker/dockerfile:1
FROM python:3-alpine
LABEL name nlp_project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly language processor designed for reconnaissance."


RUN apk add git && git clone https://github.com/cwirks01/NLP_Project.git
WORKDIR /NLP_Project

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /NLP_Project
CMD [ "python", "-m" , "main", "run", "--host=0.0.0.0"]