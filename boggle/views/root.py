from starlette.authentication import requires
from starlette.responses import UJSONResponse
from starlette.routing import Route


async def root(request):
    return UJSONResponse({"hello": "world"})
