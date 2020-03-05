from starlette.responses import UJSONResponse


async def http_exception(request, exc):
    return UJSONResponse({"message": exc.detail}, status_code=exc.status_code)
