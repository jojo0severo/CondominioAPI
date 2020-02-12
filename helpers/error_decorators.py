from functools import wraps


def permission_error_decorator(func):
    @wraps(func)
    def handle_permission_error(*args):
        try:
            return func(*args)
        except PermissionError:
            return 401, {'result': False, 'event': 'Invalid key received'}

    return handle_permission_error


def key_error_decorator(func):
    @wraps(func)
    def handle_key_error(*args):
        try:
            return func(*args)
        except KeyError:
            return 400, {'result': False, 'event': 'Missing information', 'data': {}}

    return handle_key_error
