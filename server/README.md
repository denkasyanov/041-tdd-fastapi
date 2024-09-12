# Text Summarization service

**TDD · FastAPI · Docker** course project

## Usage

This project assumes that [`uv`](https://docs.astral.sh/uv/) is installed.

### Local development

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
