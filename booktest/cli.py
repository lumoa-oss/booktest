"""
This package introduces the lumoa-rl cli interface.
It can be used for creating insights or for creating topics.
"""

import argparse
import argcomplete

import sys

import booktest as bt
from booktest.config import get_default_config
from booktest.detection import detect_tests


def add_exec(parser, method):
    parser.set_defaults(
        exec=method)


def setup_test_suite(parser):
    config = get_default_config()

    default_paths = config.get("test_paths", "test,book,run").split(",")

    tests = []
    for path in default_paths:
        tests.extend(detect_tests(path, include_in_sys_path=True))

    test_suite = bt.merge_tests(tests)
    test_suite.setup_parser(parser)
    books_dir = config.get("books_path", "books")
    parser.set_defaults(
        exec=lambda args: test_suite.exec_parsed(books_dir, args))


def exec_parsed(parsed):
    return parsed.exec(parsed)


def main(arguments=None):
    parser = argparse.ArgumentParser(description='booktest - review driven test tool')

    setup_test_suite(parser)
    argcomplete.autocomplete(parser)

    args = parser.parse_args(args=arguments)

    if "exec" in args:
        exec_parsed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main(sys.argv)
