DOCKER_COMPOSE = docker compose

COMPOSE_FILE = compose.yaml
COMPOSE_PROD_FILE = compose.prod.yaml


# Docker in development environment

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

.PHONY: dev devd stop logs


# Docker for testing "production" environment

## prod - Starts the production environment in attached mode
prod:
	$(DOCKER_COMPOSE) -f $(COMPOSE_PROD_FILE) up --build

## prodd - Starts the production environment in detached mode
prodd:
	$(DOCKER_COMPOSE) -f $(COMPOSE_PROD_FILE) up -d --build

.PHONY: prod prodd


# Checks

## format - Run formatting
format:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run ruff format .

## lint - Run linting
lint:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run ruff check . --fix

## sort - Run sorting imports
sort:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run ruff check --select I --fix

## check - Run formatting, linting and sorting imports
check: lint format sort

.PHONY: format lint sort check


# Tests

## test - Run tests
test:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run pytest

## testv - Run tests with verbose output and disabled ouptutcapture
testv:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec server uv run pytest -s -vv

.PHONY: test testv


.PHONY: help
help: Makefile
	@sed -n 's/^##//p' $<
