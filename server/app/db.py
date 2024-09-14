import logging
import os
from urllib.parse import parse_qs, urlparse


log = logging.getLogger("uvicorn")


# Fly uses sslmode=disable which Tortoise doesn't like
# So we'll parse the DATABASE_URL and process sslmode manually


def get_db_config() -> dict:
    database_url = os.environ.get("DATABASE_URL")

    parsed_url = urlparse(database_url)

    result = {
        "engine": "tortoise.backends.asyncpg",  # TODO assume postgres
        "credentials": {
            "user": parsed_url.username,
            "password": parsed_url.password,
            "host": parsed_url.hostname,
            "port": parsed_url.port,
            "database": parsed_url.path.lstrip("/"),
        },
    }

    query_params = parse_qs(parsed_url.query)
    for key, value in query_params.items():
        if key == "sslmode" and value[0] == "disable":
            result["credentials"]["ssl"] = False

    return result


TORTOISE_ORM = {
    "connections": {
        "default": get_db_config(),
    },
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        }
    },
}
