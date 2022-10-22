HOSTNAME="aws-hostname"

default:
	@echo make "<config|start|logs|stop|restart|errors|warnings|reload_config|performance>"

sync:
	@rsync -e "ssh" -auvz . ec2-user@$(HOSTNAME):seas-8414/

config:
	@cd template && bash create-docker-compose.sh dev
	@cp template/docker-compose.yml .
	@echo "INFO: config is ready. Run 'make start' to run the bot"

reload_config:
	cd tools/ && python control-bots.py reload_config

pnl:
	cd tools/ && python control-bots.py profit

start:
	docker-compose up -d --remove-orphans

logs:
	docker-compose logs -f --tail 20

stop:
	docker-compose down 

errors:
	docker-compose logs | egrep error -i

warnings:
	docker-compose logs | egrep warning -i

warn: warnings
error: errors

restart:
	docker-compose restart

down: stop

