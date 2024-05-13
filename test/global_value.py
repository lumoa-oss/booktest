import booktest as bt


GLOBAL_VALUE = "unset"


def get_global_value():
    global GLOBAL_VALUE
    return GLOBAL_VALUE


def set_global_value(global_value):
    global GLOBAL_VALUE
    GLOBAL_VALUE = global_value
