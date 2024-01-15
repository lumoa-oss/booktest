import functools
import inspect


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


def call_class_method_test(methods, func, self, case, kwargs):

    args2 = []
    args2.append(self)
    args2.append(case)

    run = case.run
    for unbound_method in methods:
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

    for unbound_method in methods:
        found, result = \
            run.get_test_result(
                case,
                unbound_method)

        if not found:
            raise ValueError(f"could not find or make method {unbound_method} result")

        args2.append(result)

    return func(*args2, **kwargs)


def depends_on(*methods):
    """
    This method depends on a method on this object.
    """
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from booktest import TestBook

            if isinstance(args[0], TestBook):
                return call_class_method_test(methods, func, args[0], args[1], kwargs)
            else:
                return call_function_test(methods, func, args[0], kwargs)

        wrapper._dependencies = methods
        wrapper._original_function = func
        return wrapper
    return decorator_depends

