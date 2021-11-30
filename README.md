# NLP Project

#### To run application in Docker with NGINX:


- Run NGINX in a docker container
    - [NGINX installation guide](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-docker/)

 - Prior to building docker ensure you took the previous container down and create a network
```docker
docker-compose down
THEN
docker network create nlp_project_default
```

 - Ensure GITHUB_TOKEN is saved in your Environmental Variables
```docker
sudo docker-compose build --build-arg NTC_TOKEN="$(echo $env:NTC_TOKEN)"; sudo docker-compose up -b
```

 - Confirm docker is running properly
```docker
docker logs --tail 50 --follow --timestamps <CONTAINER ID>
```


```Commandline
GITHUB_TOKEN expires every 90 days.
```

# CERTBOT

#### Steps to establishing a secure Connection HTTPS with Docker compose

- Ensure your nginx container name is "nginx"
- Ensure volumes are mounted between nginx and certbot in docker-compose.yml file

~~~Docker
volume:
  - ./data/certbot/conf:/etc/letsencrypt
  - ./data/certbot/www:/var/www/certbot
~~~

#### Create and save file in root directory

~~~Commandline
touch ./init-letsencrypt.sh 

curl -L https://github.com/cwirks01/NLP_Project/blob/dev/init-letsencrypt.sh > init-letsencrypt.sh
~~~
Set the path relative to the file. Then set the Domain (i.e., example.com), path, email, and whether it is staging or not.

- Staging=0 is used for testing & Staging=1 for production
- Ensure files are

You are giving a limit on how many times you can requests certs. After you set your options, then run.

#### Run linux file
~~~Bash
chmod +x init-letsencrypt.sh && \
sudo ./init-letsencrypt.sh
~~~

- You will see a directory named "live" with certs needed.

#### Renew Certificates

- Add to docker-compose.yml under Certbot This will check certbot if certs need updating every 12 hours
~~~Docker
entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
~~~

- Add to docker-compose.yml under Nginx. This will reload nginx to load certs
~~~Docker
command: "/bin/sh -c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'"
~~~