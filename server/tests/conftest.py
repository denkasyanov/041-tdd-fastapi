import os
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import RegisterTortoise

from app.config import Settings, get_settings
from app.main import create_app


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    # set up

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with RegisterTortoise(
            app=app,
            db_url=os.environ.get("DATABASE_TEST_URL"),
            modules={"models": ["app.models.tortoise"]},
            generate_schemas=True,
            add_exception_handlers=True,
        ):
            yield

    app = create_app(lifespan)
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:
        # testing
        yield test_client


# Courtesy of https://github.com/pytest-dev/pytest/issues/7568#issuecomment-1217328487
def dict_parametrize(data, **kwargs):
    args = list(list(data.values())[0].keys())
    formatted_data = [[item[a] for a in args] for item in data.values()]
    ids = list(data.keys())
    return pytest.mark.parametrize(args, formatted_data, ids=ids, **kwargs)
