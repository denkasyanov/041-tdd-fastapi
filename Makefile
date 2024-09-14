DOCKER_COMPOSE = docker compose

COMPOSE_FILE = compose.yaml
COMPOSE_PROD_FILE = compose.prod.yaml


# Dev 
## dev - Starts the development environment in attached mode
dev:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up --build

## devd - Starts the development environment in detached mode
devd:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d --build

## stop
stop:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) stop

## logs - View logs
logs:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f


## lint - Run linting
lint:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run ruff check .

## format - Run formatting
format:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run ruff format .

## sort - Run sorting imports
sort:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run ruff check --select I --fix

## check - Run linting, formatting and sorting imports
check: lint format sort


## test - Run tests
test:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run pytest


# Prod

## prod - Starts the production environment in attached mode
prod:
	$(DOCKER_COMPOSE) -f $(COMPOSE_PROD_FILE) up --build

## prodd - Starts the production environment in detached mode
prodd:
	$(DOCKER_COMPOSE) -f $(COMPOSE_PROD_FILE) up -d --build


.PHONY: help
help: Makefile
	@sed -n 's/^##//p' $<

.PHONY: dev devd stop logs lint format sort check test prod prodd help
