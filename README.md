# Text Summarization service

**TDD · FastAPI · Docker** course project

![Continuous Integration and Delivery](https://github.com/denkasyanov/041-tdd-fastapi/actions/workflows/main.yml/badge.svg?branch=main)

## Usage

All commands are run from the root of the project.

### Local environment

This project assumes that [`uv`](https://docs.astral.sh/uv/) is installed locally.

#### Start the server

```shell
docker compose up --build
```

#### Run migrations locally

```shell
docker compose exec server uv run aerich upgrade
```

#### Run tests

```shell
docker compose exec server uv run pytest
```

#### Organize imports with Ruff

```shell
uv run ruff check --select I --fix
```

#### Access postgres shell

```shell
docker compose exec server-db psql -U postgres -d server_dev
```

#### Access Tortoise shell

```shell
docker compose exec server uv run tortoise-cli shell
```

### Production environment

This projects assumes that project was deployed with Fly database app `tdd-fastapi-db`.

### Deploy

```shell
fly deploy server
```

> [!NOTE]
> `server` is the name of directory with the target `fly.toml`

#### Connect to production app and run migrations

```shell
fly ssh console -a tdd-fastapi -C "uv run aerich upgrade"
```

#### Connect to production database

```shell
fly postgres connect -a tdd-fastapi-db
```

## Stretch goals

- [ ] Add a system for tagging images
