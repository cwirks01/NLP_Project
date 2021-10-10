FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -pv /etc/nginx/sites-enabled && \
    mkdir -pv /etc/nginx/sites-available

COPY nginx.conf /etc/nginx/conf.d/nginx.conf
COPY regex.conf /etc/nginx/sites-available/regex.testing-dev.dev.conf
COPY nlp.conf /etc/nginx/sites-available/nlp.testing-dev.dev.conf
COPY drop.conf /etc/nginx/drop.conf

RUN ln -s /etc/nginx/sites-available/regex.testing-dev.dev.conf /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/nlp.testing-dev.dev.conf /etc/nginx/sites-enabled/