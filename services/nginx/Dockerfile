FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available && \
    mkdir -pv /static

WORKDIR /usr/share/nginx/html
# Remove default nginx static assets
RUN rm -rf ./*

COPY ./NLP_Project/services/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./NLP_Project/services/nginx/regex.conf /etc/nginx/sites-available/regex.testing-dev.dev.conf
COPY ./NLP_Project/services/nginx/nlp.conf /etc/nginx/sites-available/nlp.testing-dev.dev.conf
COPY ./NLP_Project/services/nginx/drop.conf /etc/nginx/drop.conf
COPY ./NLP_Project/static ./static/
COPY ./regex/static ./static/

RUN ln -s /etc/nginx/sites-available/regex.testing-dev.dev.conf /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/nlp.testing-dev.dev.conf /etc/nginx/sites-enabled/