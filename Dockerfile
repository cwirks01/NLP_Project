# syntax=docker/dockerfile:1
FROM python:3-alpine
LABEL name NLP_Project
LABEL src "https://github.com/cwirks01/NLP_Project"
LABEL desc "Incredibly fast crawler designed for reconnaissance."

RUN apk add git && git clone https://github.com/cwirks01/NLP_Project.git NLP_Project
WORKDIR /NLP_Project

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]