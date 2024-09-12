import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api import ping


def create_app() -> FastAPI:
    app = FastAPI()

    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )

    app.include_router(ping.router)

    return app


app = create_app()
