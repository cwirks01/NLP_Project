# NLP_Project

## To run Docker with ssh-keys


```commandline
docker build -t nlp_project --build-arg ssh_prv_key="$(cat ~/.ssh/id_ed25519)" --build-arg ssh_pub_key="$(cat ~/.ssh/id_ed25519.pub)" .
```

```

```

