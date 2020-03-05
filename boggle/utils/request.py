from starlette.requests import Request


def get_request_obj_from_args(*args):
    """
    In order to make the `authentication` function usable by both HTTPEndpoint class and functions,
    when the wrapper function is a class method, there would be an extra 'self' argument.
    This function is used to extract the <Request> from the HTTPEndpoint.
    """
    for arg in args:
        if isinstance(arg, Request):
            return arg
    raise ValueError("Missing 'request' object in function arguments")
