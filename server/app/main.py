import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.types import Lifespan
from tortoise.contrib.fastapi import RegisterTortoise

from app.api import ping, summaries
from app.db import TORTOISE_ORM


log = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app=app,
        # db_url=os.environ.get("DATABASE_URL"),
        # modules={"models": ["app.models.tortoise"]},
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        yield


def create_app(lifespan: Lifespan = lifespan) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(ping.router)
    app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
    return app


app = create_app(lifespan)
