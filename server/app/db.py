import logging
import os

from tortoise import Tortoise, run_async


log = logging.getLogger("uvicorn")


TORTOISE_ORM = {
    "connections": {
        "default": os.environ.get("DATABASE_URL"),
    },
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        }
    },
}


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")
    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={
            "models": ["models.tortoise"]
        },  # without `app` because we run it from the file inside the `app` directory
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
