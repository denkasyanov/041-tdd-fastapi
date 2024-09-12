import logging
import os

from fastapi import FastAPI

from app.api import ping
from app.db import init_db


log = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(ping.router)
    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
