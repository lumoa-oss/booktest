import functools


def depends_on(*methods):
    """
    This method depends on a method on this object.
    """
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            case = args[1]
            run = args[1].run

            args2 = []
            args2.extend(args)
            for unbound_method in methods:
                # 1. Try first to find this method for this exact test instance.
                #    This covers cases, where a test class has bee instantiated
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
        wrapper._dependencies = methods
        return wrapper
    return decorator_depends

