# Took credit from @tomchristie
# https://github.com/encode/hostedapi/blob/master/tests/conftest.py

from alembic import command
from alembic.config import Config
from starlette.config import environ
from gino.ext.starlette import Gino
from sqlalchemy_utils import database_exists, create_database
import pytest
import uvloop


from boggle import create_app, db
from boggle.config import DATABASE_URL
from boggle.config.db import DB_CONFIG
from boggle.tests.client import TestClient

app = create_app()


@pytest.fixture(scope="session")
def event_loop():
    _loop = uvloop.new_event_loop()
    yield _loop
    _loop.close()


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    """
    Create a clean database on every test case.
    """
    url = DATABASE_URL
    if not database_exists(url):
        create_database(url)

    # Set up the tables in DB
    await db.set_bind(url)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


@pytest.fixture()
async def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    @pytest.mark.asyncio
    async def test_homepage(client):
        url = app.url_path_for('homepage')
        response = async client.get(url)
        assert response.status_code == 200
    """
    yield TestClient(app)
