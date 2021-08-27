# NLP_Project

#### To run Docker with ssh-keys:


```commandline
docker build -t nlp_project --build-arg TOKEN="$(echo $env:GITHUB_TOKEN)" .
```

```
Will need to update GITHUB_TOKEN when it expires
```

