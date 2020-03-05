from functools import partial, wraps
from starlette.responses import UJSONResponse

import boggle.schemas as schemas


def serialize_response(func=None, *, model, type="json", status_code=200):
    """Serialize the output using '<model>Out' schema in boggle/schemas.py"""
    response_types = {
        "json": UJSONResponse,
    }
    if func is None:
        return partial(
            serialize_response, model=model, type=type, status_code=status_code,
        )

    @wraps(func)
    async def inner(*args, **kwargs):
        result = await func(*args, **kwargs)

        # Serialize output
        _schema = getattr(schemas, model + "Out")()
        seriliazed_data = _schema.dump(result)
        return response_types[type](seriliazed_data, status_code=status_code)

    return inner
