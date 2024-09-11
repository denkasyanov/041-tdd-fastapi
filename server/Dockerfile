FROM python:3.12.4-slim-bookworm

# Set up uv
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./uv.lock .
COPY ./pyproject.toml .
RUN uv sync --frozen


# CMD ["uv", "run", "my_app"]
