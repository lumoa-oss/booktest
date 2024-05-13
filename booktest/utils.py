import functools


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
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with SetupTeardown(setup_teardown_generator):
                return func(*args, **kwargs)

        wrapper._original_function = func
        return wrapper

    return decorator_depends


def combine_decorators(*decorators):
    def decorator(func):
        rv = func
        for i in decorators:
            rv = i(rv)

        return rv

    return decorator
