from pydoc import resolve

from booktest.reporting.review import BOOK_TEST_PREFIX

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
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i]

            # Skip comments and empty lines
            if line.startswith(';') or line.startswith('#') or not line.strip():
                i += 1
                continue

            # Parse key=value
            if '=' in line:
                key, value = line.strip().split('=', 1)
                key = key.strip()
                value = value.strip()

                # Check if this is a multiline value (empty or whitespace after =)
                if not value:
                    # Collect subsequent indented lines
                    multiline_values = []
                    i += 1
                    while i < len(lines):
                        next_line = lines[i]
                        # Check if line is indented (starts with whitespace)
                        if next_line.strip() and (next_line.startswith(' ') or next_line.startswith('\t')):
                            multiline_values.append(next_line.strip())
                            i += 1
                        else:
                            break

                    # Join multiline values
                    if multiline_values:
                        config[key] = '\n'.join(multiline_values)
                else:
                    config[key] = parse_config_value(value)
                    i += 1
            else:
                i += 1


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


def update_config_value(config_file: str, key: str, value: str):
    """
    Update or add a configuration value in a config file.

    This preserves comments and formatting of the config file.
    """
    lines = []
    key_found = False

    if path.exists(config_file):
        with open(config_file, 'r') as f:
            lines = f.readlines()

    # Try to update existing key
    for i, line in enumerate(lines):
        if not line.startswith(';') and not line.startswith('#') and line.strip():
            if '=' in line:
                existing_key = line.split('=', 1)[0].strip()
                if existing_key == key:
                    lines[i] = f"{key}={value}\n"
                    key_found = True
                    break

    # If key not found, add it
    if not key_found:
        # Add newline before if file doesn't end with one
        if lines and not lines[-1].endswith('\n'):
            lines[-1] += '\n'
        lines.append(f"{key}={value}\n")

    # Write back
    with open(config_file, 'w') as f:
        f.writelines(lines)


def get_fs_version(config_file: str = PROJECT_CONFIG_FILE) -> str:
    """
    Get the filesystem version from config.

    Returns "v1" (legacy) if not found, "v2" for pytest-style naming.
    Reads from booktest.ini (project config) as this is project state.
    """
    config = {}
    parse_config_file(config_file, config)
    return config.get("fs_version", "v1")


def set_fs_version(version: str, config_file: str = PROJECT_CONFIG_FILE):
    """
    Set the filesystem version in config.

    Writes to booktest.ini (project config) as this should be in Git.
    """
    update_config_value(config_file, "fs_version", version)


def extract_env_vars(config: dict) -> dict:
    """
    Extract environment variables from config.

    Supports pytest-style format:
        env =
            FOO=bar
            BAZ=qux

    Also supports legacy env_ prefix format:
        env_FOO=bar

    Returns a dictionary of environment variable names to values.
    """
    env_vars = {}

    # Check for pytest-style 'env' key with multiline value
    if 'env' in config:
        env_value = config['env']
        if isinstance(env_value, str) and '\n' in env_value:
            # Parse multiline env value
            for line in env_value.split('\n'):
                line = line.strip()
                if line and '=' in line:
                    var_name, var_value = line.split('=', 1)
                    env_vars[var_name.strip()] = var_value.strip()

    # Also support legacy env_ prefix format for backward compatibility
    for key, value in config.items():
        if key.startswith("env_"):
            env_name = key[4:]  # Remove 'env_' prefix
            env_vars[env_name] = value

    return env_vars
