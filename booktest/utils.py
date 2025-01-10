import functools

from booktest.coroutines import maybe_async_call
import importlib.resources as rs
import os


def accept_all(_):
    return True


def path_to_module_resource(path: str):
    parts = path.split("/")
    return ".".join(parts[:len(parts)-1]), parts[len(parts)-1]


def open_file_or_resource(path: str, is_resource: bool):
    if is_resource:
        module, resource = path_to_module_resource(path)
        return rs.open_text(module, resource)
    else:
        return open(path, "r")

def file_or_resource_exists(path: str, is_resource: bool):
    if is_resource:
        module, resource = path_to_module_resource(path)
        try:
            return rs.is_resource(module, resource)
        except ModuleNotFoundError:
            return False
    else:
        return os.path.exists(path)


class SetupTeardown:

    def __init__(self, setup_teardown_generator):
        self.setup_teardown_generator = setup_teardown_generator

        self._generator = None

    def __enter__(self):
        self._generator = self.setup_teardown_generator()
        next(self._generator)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            next(self._generator)
        except StopIteration:
            pass

        self._generator = None


def setup_teardown(setup_teardown_generator):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            with SetupTeardown(setup_teardown_generator):
                return await maybe_async_call(func, args, kwargs)

        wrapper._original_function = func
        return wrapper

    return decorator


def combine_decorators(*decorators):
    def decorator(func):
        rv = func
        for i in decorators:
            rv = i(rv)

        return rv

    return decorator
