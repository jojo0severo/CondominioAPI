from functools import wraps


def key_error_decorator(func):
    @wraps(func)
    def handle_key_error(*args):
        try:
            return func(*args)
        except KeyError as e:
            return 400, {'status': 400, 'result': False, 'event': f'Missing information: {e}', 'data': {}}

    return handle_key_error


def runtime_error_decorator(func):
    @wraps(func)
    def handle_runtime_error(*args):
        try:
            return func(*args)
        except RuntimeError as e:
            return 500, {'status': 500, 'result': False, 'event': f'Something went wrong with the application: {e}', 'data': {}}

    return handle_runtime_error


def value_error_decorator(func):
    @wraps(func)
    def handle_value_error(*args):
        try:
            return func(*args)
        except ValueError as e:
            return 400, {'status': 400, 'result': False, 'event': f'Unknown option passed: {e}', 'data': {}}

    return handle_value_error
