# NLP_Project

#### To run application in Docker with NGINX:


- Run NGINX in a docker container
    - [Link to NGINX installation](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-docker/)


 - Ensure GITHUB_TOKEN is saved in your Environmental Variables
```docker
docker build -t nlp_project --build-arg TOKEN="$(echo $env:GITHUB_TOKEN)" .
```

```Commandline
GITHUB_TOKEN expires every 90 days.
```

