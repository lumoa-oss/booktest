

def process_setup_teardown():
    from test.global_value import set_global_value
    set_global_value("set")
    yield
    set_global_value("unset")

