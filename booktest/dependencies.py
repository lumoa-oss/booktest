import functools
import inspect

from booktest.coroutines import maybe_async_call


class Resource:
    """
    Represents an exclusive resources, which must not be
    shared simultaneously by several parallel tests

    Such a resource can be a specific port, file system resource,
    some global state or excessive use of RAM or GPU, that prohibits parallel
    run.
    """

    def __init__(self, value, identifier=None):
        self.value = value
        if identifier is None:
            identifier = value
        self.identifier = identifier

    def __eq__(self, other):
        return isinstance(other, Resource) and self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)


def port(value: int):
    """
    Generates a resource for given port.
    A special identifier is generated in order to not mix the port
    with other resource integers
    """
    return Resource(value, f"port={value}")


def get_decorated_attr(method, attr):
    while True:
        if hasattr(method, attr):
            return getattr(method, attr)
        if hasattr(method, "_original_function"):
            method = method._original_function
        else:
            return None


def remove_decoration(method):
    while hasattr(method, "_original_function"):
        method = method._original_function
    return method


def bind_dependent_method_if_unbound(method, dependency):
    dependency_type = get_decorated_attr(dependency, "_self_type")
    self = get_decorated_attr(method, "__self__")

    if dependency_type is not None and self is not None and isinstance(self, dependency_type):
        return dependency.__get__(self, self.__class__)
    else:
        return dependency


async def call_class_method_test(dependencies, func, self, case, kwargs):

    args2 = []
    args2.append(self)
    args2.append(case)

    run = case.run
    for dependency in dependencies:
        if isinstance(dependency, Resource):
            args2.append(dependency.value)
        else:
            unbound_method = dependency
            # 1. Try first to find this method for this exact test instance.
            #    This covers cases, where a test class has been instantiated
            #    with several different parameters

            bound_method = unbound_method.__get__(self, self.__class__)
            found, result = \
                run.get_test_result(
                    case,
                    bound_method)

            # 2. If method is not exist for test instance, try to look elsewhere.
            #    This allows for tests to share same data or prepared model
            if not found:
                found, result = \
                    run.get_test_result(
                        case,
                        unbound_method)

            if not found:
                raise ValueError(f"could not find or make method {unbound_method} result")

            args2.append(result)

    return await maybe_async_call(func, args2, kwargs)

async def call_function_test(methods, func, case, kwargs):
    run = case.run

    args2 = []
    args2.append(case)

    for dependency in methods:
        if isinstance(dependency, Resource):
            args2.append(dependency.value)
        else:
            found, result = \
                run.get_test_result(
                    case,
                    dependency)

            if not found:
                raise ValueError(f"could not find or make method {dependency} result")

            args2.append(result)

    return await maybe_async_call(func, args2, kwargs)


def depends_on(*dependencies):
    """
    This method depends on a method on this object.
    """
    methods = []
    resources = []
    for i in dependencies:
        if isinstance(i, Resource):
            resources.append(i)
        else:
            methods.append(i)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook

            if isinstance(args[0], TestBook):
                return await call_class_method_test(dependencies, func, args[0], args[1], kwargs)
            else:
                return await call_function_test(dependencies, func, args[0], kwargs)

        wrapper._dependencies = methods
        wrapper._resources = resources
        wrapper._original_function = func
        return wrapper

    return decorator

