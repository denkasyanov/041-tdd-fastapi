FROM python:3.12.4-slim-bookworm

# Set up uv
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get -y install netcat-traditional gcc postgresql \
  && apt-get clean

COPY ./uv.lock ./pyproject.toml ./
RUN uv sync --frozen

COPY . . 

COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
