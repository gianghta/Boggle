import uvicorn

from boggle import create_app
from boggle.config.app import UVICORN_RUN_CONFIG


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app:app", **UVICORN_RUN_CONFIG)
