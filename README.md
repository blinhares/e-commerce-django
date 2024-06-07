# titulo

## Apaga tudo

```bash
docker rm -vf $(docker ps -aq) ; docker rmi -f $(docker images -aq)
```

## build

Execute:

```bash
sudo docker compose up --build --force-recreate
```

## Para Rodar o Contêiner

```bash
sudo docker compose up
```
