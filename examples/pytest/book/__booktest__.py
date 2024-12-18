
def process_setup_teardown():
    from book.global_value import set_global_value
    set_global_value("set")
    yield
    set_global_value("unset")

