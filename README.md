# NLP_Project

#### To run application in Docker with NGINX:


- Run NGINX in a docker container
    - [Link to NGINX installation](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-docker/)


 - Ensure GITHUB_TOKEN is saved in your Environmental Variables
```docker
sudo docker-compose build --build-arg NTC_TOKEN="$(echo $env:NTC_TOKEN)"; sudo docker-compose up -b
```

```Commandline
GITHUB_TOKEN expires every 90 days.
```

