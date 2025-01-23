from pydoc import resolve

from booktest.review import BOOK_TEST_PREFIX

import os
from os import path


# project config, should be put in git
PROJECT_CONFIG_FILE = "booktest.ini"

# personal config, should not be put in git
DOT_CONFIG_FILE = ".booktest"

DEFAULT_CONFIG = None

DEFAULT_PYTHON_PATH = "src:."

# let's have moderately long timeout, as the tool is aimed for data science projects, where individual tests
# can be slow
DEFAULT_TIMEOUT = "1800"


def parse_config_value(value):
    if value == "1":
        return True
    elif value == "0":
        return False
    else:
        return value


def parse_config_file(config_file, config):
    if path.exists(config_file):
        with open(config_file) as f:
            for line in f:
                if line.startswith(';') or line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=', 1)
                config[key] = parse_config_value(value)


def resolve_default_config():

    project_config_file = PROJECT_CONFIG_FILE
    dot_config_file = DOT_CONFIG_FILE

    rv = {}
    # let personal .booktest file has lowest priority
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, ".booktest")

    parse_config_file(file_path, rv)
    # let project config booktest.ini file
    parse_config_file(project_config_file, rv)
    # let config_file defaults have lower priority
    parse_config_file(dot_config_file, rv)

    # environment defaults have higher priority
    for key, value in os.environ.items():
        if key.startswith(BOOK_TEST_PREFIX):
            book_key = key[len(BOOK_TEST_PREFIX):].lower()
            rv[book_key] = parse_config_value(value)

    return rv


def get_default_config():
    global DEFAULT_CONFIG
    if DEFAULT_CONFIG is None:
        DEFAULT_CONFIG = resolve_default_config()

    return DEFAULT_CONFIG
