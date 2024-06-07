all:
	@sudo docker compose up
ch_permi:
	@ls | xargs sudo chown -R bruno:bruno
build:
	@sudo docker compose up --build --force-recreate
apagar_dockers:
	@docker rm -vf $(docker ps -aq) ; docker rmi -f $(docker images -aq)