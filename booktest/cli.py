"""
This package introduces the lumoa-rl cli interface.
It can be used for creating insights or for creating topics.
"""

import argparse
from os import chdir

import argcomplete

import sys

import booktest as bt
from booktest.config.config import get_default_config, DEFAULT_PYTHON_PATH, extract_env_vars
from booktest.config.detection import detect_tests, detect_setup, include_sys_path
from booktest.migration.migrate import check_and_migrate
from booktest.snapshots.env import MockEnv
import os


def add_exec(parser, method):
    parser.set_defaults(
        exec=method)


def setup_test_suite(parser, python_path=None, detect_selection=None):
    config = get_default_config()

    default_paths = config.get("test_paths", "test,book,run").split(",")

    if python_path is None:
        python_path = config.get("python_path", DEFAULT_PYTHON_PATH)

    include_sys_path(python_path)

    tests = []
    setup = None
    for path in default_paths:
        tests.extend(detect_tests(path, detect_selection))
        path_setup = detect_setup(path)
        if path_setup is not None:
            setup = path_setup

    test_suite = bt.merge_tests(tests)

    # Check and perform automatic migration AFTER test discovery
    # This ensures we have the test structure needed to migrate legacy paths
    books_dir = config.get("books_path", "books")
    check_and_migrate(base_dir=books_dir, tests=test_suite)

    test_suite.setup_parser(parser)

    parser.set_defaults(
        exec=lambda args: test_suite.exec_parsed(books_dir,
                                                 args,
                                                 setup=setup))


def exec_parsed(parsed):
    return parsed.exec(parsed)


def main(arguments=None):
    if arguments is None:
        arguments = sys.argv[1:]

    parser = argparse.ArgumentParser(description='booktest - review driven test tool')

    context = os.environ.get("BOOKTEST_CONTEXT", None)
    python_path = os.environ.get("PYTHON_PATH", None)
    detect_selection = None

    if arguments and "--context" in arguments:
        context_pos = arguments.index("--context")
        context = arguments[context_pos+1]

    if arguments and "--python-path" in arguments:
        python_path_pos = arguments.index("---python-path")
        python_path = arguments[python_path_pos+1]

    if arguments and "--narrow-detection" in arguments:
        detect_selection = []
        for i in arguments:
            if not i.startswith("-"):
                detect_selection.append(i)
        if len(detect_selection) == 0:
            detect_selection = None

    if context is not None:
        os.chdir(context)

    # Load config and extract environment variables
    config = get_default_config()
    env_vars = extract_env_vars(config)

    # Apply environment variables before test discovery
    # This allows tests to read env vars during module import
    mock_env = None
    if env_vars:
        mock_env = MockEnv(env_vars)
        mock_env.start()

    try:
        setup_test_suite(parser, python_path, detect_selection)
        argcomplete.autocomplete(parser)

        args = parser.parse_args(args=arguments)

        if "exec" in args:
            return exec_parsed(args)
        else:
            parser.print_help()
            return 1
    finally:
        # Clean up environment variables after execution
        if mock_env is not None:
            mock_env.stop()


if __name__ == "__main__":
    main(sys.argv)
