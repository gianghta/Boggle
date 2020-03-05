import platform
from sys import implementation

from boggle.config import MODE


# The uvloop implementation provides greater performance,
# but is not compatible with Windows or PyPy
EVENT_LOOP = (
    "uvloop"
    if implementation.name != "pypy" and platform.system() != "Windows"
    else "asyncio"
)

DEBUG = MODE != "production"

BASE_UVICORN_RUN_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "loop": EVENT_LOOP,
    "lifespan": "on",
}

if MODE == "production":
    UVICORN_RUN_CONFIG = {
        **BASE_UVICORN_RUN_CONFIG,
        "access_log": False,
        "workers": 2,
    }

else:  # MODE == "development" or MODE == "testing":
    UVICORN_RUN_CONFIG = {
        **BASE_UVICORN_RUN_CONFIG,
        "reload": True,  # Enable auto-reload
    }
