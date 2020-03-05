from os import environ

from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings


MODE = environ.get("MODE", "development").lower()

# Configuration from .env file
config = Config(".env")

POSTGRES_USER = config("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default=None)
POSTGRES_DB = config("POSTGRES_DB", default="postgres")
POSTGRES_HOST = config("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = config("POSTGRES_PORT", default=5432)
TEST_POSTGRES_USER = environ.get("TEST_POSTGRES_USER", "postgres")
TEST_POSTGRES_HOST = environ.get("TEST_POSTGRES_HOST", "localhost")
TEST_POSTGRES_PORT = int(environ.get("TEST_POSTGRES_PORT", 54321))
TEST_POSTGRES_DATABASE = environ.get("TEST_POSTGRES_DATABASE", "postgres")

if MODE == "testing":
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{TEST_POSTGRES_HOST}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DATABASE}"
else:
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)
