"""
This package introduces the lumoa-rl cli interface.
It can be used for creating insights or for creating topics.
"""

import argparse
import argcomplete

import sys

import booktest as bt
from booktest.config import get_default_config
from booktest.detection import detect_tests, detect_setup, include_sys_path
import os


def add_exec(parser, method):
    parser.set_defaults(
        exec=method)


def setup_test_suite(parser, context=None):
    if context is None:
        context = os.path.curdir

    config = get_default_config(context)

    default_paths = config.get("test_paths", "test,book,run").split(",")

    include_sys_path(context, config)

    tests = []
    setup = None
    for path in default_paths:
        tests.extend(detect_tests(context, path))
        path_setup = detect_setup(context, path)
        if path_setup is not None:
            setup = path_setup

    test_suite = bt.merge_tests(tests)
    test_suite.setup_parser(parser)
    books_dir = os.path.join(context, config.get("books_path", "books"))

    parser.set_defaults(
        exec=lambda args: test_suite.exec_parsed(books_dir,
                                                 args,
                                                 setup=setup))


def exec_parsed(parsed):
    return parsed.exec(parsed)


def main(arguments=None):
    parser = argparse.ArgumentParser(description='booktest - review driven test tool')

    context = os.environ.get("BOOKTEST_CONTEXT", None)
    if arguments and "--context" in arguments:
        context_pos = arguments.index("--context")
        context = arguments(context_pos+1)

    setup_test_suite(parser, context)
    argcomplete.autocomplete(parser)

    args = parser.parse_args(args=arguments)

    if "exec" in args:
        return exec_parsed(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    main(sys.argv)
