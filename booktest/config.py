from booktest.review import BOOK_TEST_PREFIX

import os
from os import path


DEFAULT_CONFIG_FILE = ".booktest"
DEFAULT_CONFIG = None


def parse_config_value(value):
    if value == "1":
        return True
    elif value == "0":
        return False
    else:
        return value


def resolve_default_config(config_file):
    rv = {}
    # let config_file defaults have lower priority
    if path.exists(config_file):
        with open(config_file) as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=', 1)
                rv[key] = parse_config_value(value)

    # environment defaults have higher priority
    for key, value in os.environ.items():
        if key.startswith(BOOK_TEST_PREFIX):
            book_key = key[len(BOOK_TEST_PREFIX):].lower()
            rv[book_key] = parse_config_value(value)

    return rv


def get_default_config():
    global DEFAULT_CONFIG
    if DEFAULT_CONFIG is None:
        DEFAULT_CONFIG = resolve_default_config(DEFAULT_CONFIG_FILE)
    return DEFAULT_CONFIG
