from functools import partial, wraps
from json.decoder import JSONDecodeError
from marshmallow import ValidationError

from boggle.exceptions import InvalidUsage
import boggle.schemas as schemas
from boggle.utils.request import get_request_obj_from_args


def validate(data, schema):
    """Validate/Deserialize data input using schemas from boggle/schemas.py"""
    if not data:
        return data

    _schema = getattr(schemas, schema)()
    try:
        res = _schema.load(data)
    except ValidationError as err:
        raise InvalidUsage(err.messages)
    return res


def validate_request(func=None, *, model=None, method):
    """
    Unpack the body, path params and query params from the request
    to the kwargs of the wrapped function.
    """
    if func is None:
        return partial(validate_request, model=model, method=method)

    @wraps(func)
    async def inner(*args, **kwargs):
        if method not in ("Read", "Write"):
            raise ValueError("The method must be either 'Read' or 'Write'.")

        request = get_request_obj_from_args(*args)

        # There are 3 types of schemas: Read, Write and Out
        # 1. Read is for GET requests
        # 2. Write is for POST request
        # 3. Out is for the output of ALL requests
        #   (This is handled in boggle/utils/serialization/serialize_response)
        schema = model + method
        path_params = validate(request.path_params, schema)
        query_params = validate(request.query_params, schema)
        body = dict()
        try:
            raw_body = await request.body()
            # Only parse JSON for request body if it is not empty/None
            if raw_body:
                body = await request.json()
        except JSONDecodeError:
            raise InvalidUsage("Missing or invalid JSON format for request body.")

        if method == "Write":
            body = validate(body, schema)

        return await func(
            *args,
            path_params=path_params,
            body=body,
            query_params=query_params,
            **kwargs
        )

    return inner
