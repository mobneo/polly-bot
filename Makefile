.PHONY: start build up down shell

start:
	docker-compose up -d --build

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

shell:
	docker-compose exec polymarket-cli polymarket shell

# Wallet management
wallet-create:
	docker-compose exec polymarket-cli polymarket wallet create

wallet-show:
	docker-compose exec polymarket-cli polymarket wallet show

# Quick commands
markets-list:
	docker-compose exec polymarket-cli polymarket markets list --limit 10

my-balance:
	docker-compose exec polymarket-cli polymarket clob balance --asset-type collateral

bash:
	docker-compose exec polymarket-cli bash

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
