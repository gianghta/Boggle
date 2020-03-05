from starlette.schemas import SchemaGenerator
from starlette.responses import HTMLResponse

from boggle.templates.openapi import OPENAPI_TEMPLATE


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Boggle API", "version": "1.0"}}
)


def openapi_schema(request):
    schema = schemas.get_schema(routes=request.app.routes)
    return HTMLResponse(OPENAPI_TEMPLATE % schema)
