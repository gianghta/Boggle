from starlette.routing import Mount, Route

from boggle.views.root import root
from boggle.views.game import routes as game_routes
from boggle.views.openapi import openapi_schema


routes = [
    Route("/", root),
    Route("/docs", endpoint=openapi_schema, include_in_schema=False),
    *game_routes,
]
