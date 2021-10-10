FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available && \
    mkdir -pv /static

COPY ./services/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./services/nginx/regex.conf /etc/nginx/sites-available/regex.testing-dev.dev.conf
COPY ./services/nginx/nlp.conf /etc/nginx/sites-available/nlp.testing-dev.dev.conf
COPY ./services/nginx/drop.conf /etc/nginx/drop.conf
COPY ./static/ ./static/
COPY ../regex/static/ ./static/

RUN ln -s /etc/nginx/sites-available/regex.testing-dev.dev.conf /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/nlp.testing-dev.dev.conf /etc/nginx/sites-enabled/