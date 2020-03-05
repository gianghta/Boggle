from gino.ext.starlette import Gino
from starlette.applications import Starlette
from starlette.authentication import AuthCredentials
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from boggle.config import DATABASE_URL, MODE
from boggle.config.db import DB_CONFIG


# Set up DB before connecting with app
db = Gino(**DB_CONFIG)


async def setup_db():
    # Only automatically create new tables
    # For changes in existing tables, please run migration manually with alembic
    # to avoid collision for the DB
    if MODE == "development":
        # Create new tables
        from boggle.models import db as _db

        await _db.gino.create_all()


def create_app():
    from boggle.config.app import DEBUG
    from boggle.views.urls import routes
    from boggle.utils.exception import http_exception

    exception_handlers = {HTTPException: http_exception}
    app = Starlette(
        routes=routes,
        debug=DEBUG,
        exception_handlers=exception_handlers,
        on_startup=[setup_db],
    )

    db.init_app(app)
    return app
