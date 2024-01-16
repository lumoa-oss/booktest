import functools
import inspect


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


def bind_dependent_method_if_unbound(method, dependency):
    non_annotated = dependency
    while hasattr(non_annotated, "_original_function"):
        non_annotated = non_annotated._original_function

    if (hasattr(method, "__self__") and
        "self" in inspect.getfullargspec(non_annotated).args):
        self = method.__self__
        return dependency.__get__(self, self.__class__)
    else:
        return dependency


def call_class_method_test(dependencies, func, self, case, kwargs):

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

    return func(*args2, **kwargs)


def call_function_test(methods, func, case, kwargs):
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

    return func(*args2, **kwargs)


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

    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from booktest import TestBook

            if isinstance(args[0], TestBook):
                return call_class_method_test(dependencies, func, args[0], args[1], kwargs)
            else:
                return call_function_test(dependencies, func, args[0], kwargs)

        wrapper._dependencies = methods
        wrapper._resources = resources
        wrapper._original_function = func
        return wrapper
    return decorator_depends

