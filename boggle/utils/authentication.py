from functools import wraps

from boggle.exceptions import InvalidUsage, Unauthorized
from boggle.models import Board


def authenticate(func=None):
    @wraps(func)
    async def inner(*args, **kwargs):
        path_params = kwargs.get("path_params", {})
        body = kwargs.get("body", {})

        if "id" not in path_params:
            raise InvalidUsage("Missing ID in path params")

        board_id = path_params["id"]
        board = await Board.get(id=board_id)

        if "token" not in body or board["token"] != body["token"]:
            raise Unauthorized("Missing or invalid token")

        return await func(*args, **kwargs)

    return inner
