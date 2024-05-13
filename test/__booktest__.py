import booktest as bt


GLOBAL_VALUE = "unset"


def get_global_value():
    global GLOBAL_VALUE
    return GLOBAL_VALUE


@bt.setup_teardown
def default_decorator():
    global GLOBAL_VALUE
    GLOBAL_VALUE = "set"
    yield
    GLOBAL_VALUE = "unset"
