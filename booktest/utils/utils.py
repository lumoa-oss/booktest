import functools

from booktest.utils.coroutines import maybe_async_call
import importlib.resources as rs
import os


def accept_all(_):
    return True


def path_to_module_resource(path: str):
    """
    DEPRECATED: Old API that doesn't handle dots in filenames.
    Use open_file_or_resource() with files() API instead.
    """
    parts = path.split("/")
    return ".".join(parts[:len(parts)-1]), parts[len(parts)-1]


def open_file_or_resource(path: str, is_resource: bool):
    """
    Open a file or resource for reading.

    Uses modern importlib.resources.files() API which handles paths with dots correctly.
    Assumes first path component is the root Python package (e.g., 'books').

    Args:
        path: Path like 'books/test/test_hello.py/test_hello.md'
        is_resource: Whether to use Pants resource system

    Returns:
        File-like object opened for text reading
    """
    if not path.startswith("/") and is_resource:
        # Split path into root module and relative path
        parts = path.split('/')
        if len(parts) < 2:
            raise ValueError(f"Resource path must have at least 2 components: {path}")

        root_module = parts[0]  # e.g., 'books'
        relative_parts = parts[1:]  # e.g., ['test', 'test_hello.py', 'test_hello.md']

        # Use files() API to navigate to the resource
        traversable = rs.files(root_module)
        for part in relative_parts:
            traversable = traversable / part

        # Open the resource for reading
        return traversable.open('r')
    else:
        return open(path, "r")

def file_or_resource_exists(path: str, is_resource: bool):
    """
    Check if a file or resource exists.

    Uses modern importlib.resources.files() API which handles paths with dots correctly.
    Assumes first path component is the root Python package (e.g., 'books').

    Args:
        path: Path like 'books/test/test_hello.py/test_hello.md'
        is_resource: Whether to use Pants resource system

    Returns:
        True if the file/resource exists
    """
    # there seems to be a special case, where absolutely paths are provided
    # in is_resource mode, so we need to handle that as well
    if not path.startswith("/") and is_resource:
        # Split path into root module and relative path
        parts = path.split('/')
        if len(parts) < 2:
            return False

        root_module = parts[0]  # e.g., 'books'
        relative_parts = parts[1:]  # e.g., ['test', 'test_hello.py', 'test_hello.md']

        if not root_module:
            return False
        try:
            # Use files() API to navigate to the resource
            traversable = rs.files(root_module)
            for part in relative_parts:
                traversable = traversable / part

            # Check if it exists and is a file (not a directory)
            return traversable.is_file()
        except (ModuleNotFoundError, FileNotFoundError, AttributeError):
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
