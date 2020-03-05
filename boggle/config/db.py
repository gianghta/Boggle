from boggle.config import (
    MODE,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PORT,
    TEST_POSTGRES_USER,
    TEST_POSTGRES_HOST,
    TEST_POSTGRES_PORT,
    TEST_POSTGRES_DATABASE,
)


if MODE in ("production", "development"):
    DB_CONFIG = {
        "host": POSTGRES_HOST,
        "port": POSTGRES_PORT,
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "database": POSTGRES_DB,
        "pool_min_size": 10,
        "pool_max_size": 20,
        "kwargs": {"command_timeout": 60 * 2},
    }
elif MODE == "testing":
    DB_CONFIG = {
        "host": TEST_POSTGRES_HOST,
        "port": TEST_POSTGRES_PORT,
        "user": TEST_POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "database": TEST_POSTGRES_DATABASE,
        "pool_min_size": 5,
        "pool_max_size": 10,
    }
