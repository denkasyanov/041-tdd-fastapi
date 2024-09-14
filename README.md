# Text Summarization service

**TDD · FastAPI · Docker** course project

## Usage

This project assumes that [`uv`](https://docs.astral.sh/uv/) is installed.

### Local environment

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

#### Connect to production app and run migrations

```shell
fly postgres connect -a tdd-fastapi-db
```

On server:

```shell
uv run aerich upgrade
```

#### Connect to production database

```shell
fly postgres connect -a tdd-fastapi-db
```
