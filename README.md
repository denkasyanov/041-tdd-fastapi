# Text Summarization service

**TDD · FastAPI · Docker** course project

![Continuous Integration and Delivery](https://github.com/denkasyanov/041-tdd-fastapi/actions/workflows/main.yml/badge.svg?branch=main)

## Usage

All commands are run from the root of the project.

### Local environment

This project assumes that [`uv`](https://docs.astral.sh/uv/) is installed locally.

#### Start the server

```shell
make dev
```

#### Run migrations locally

```shell
docker compose exec server uv run aerich upgrade
```

#### Run tests

Basic run

```shell
make test
```

Test run with **verbose** output and disabled output capture

```shell
make testv
```

#### Run all checks and formatting

```shell
make check
```

#### Run individual checks/formatting

Format with Ruff

```shell
make format
```

Lint with Ruff

```shell
make lint
```

Sort imports

```shell
make sort
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

- [X] Use `uv` instead of `pip`
- [X] Don't pin dependencies
- [X] Use `lifespan` in Tortoise ORM instead of lifecycle event handlers
- [X] Replace long commands with `make` shortcuts
- [ ] Make multistage Docker build (ideas: <https://hynek.me/articles/docker-uv/>)
- [ ] Make use of Docker caching (ideas: <https://testdriven.io/blog/faster-ci-builds-with-docker-cache/>)
- [ ] Make table with shortcut and full command in README
- [ ] Add a system for tagging images
- [ ] Test CD from a private registry
- [ ] Clear test database after each test run
