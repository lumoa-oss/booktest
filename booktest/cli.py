"""
This package introduces the lumoa-rl cli interface.
It can be used for creating insights or for creating topics.
"""

import argparse
import os.path

import time
import sys
import os
import importlib
import types
import sys
import inspect
from inspect import signature, Parameter

import booktest as bt
from booktest.config import get_default_config


def add_exec(parser, method):
    parser.set_defaults(
        exec=method)


def setup_test_suite(parser):
    config = get_default_config()

    default_paths = config.get("test_paths", "test,book,run").split(",")

    tests = []
    for path in default_paths:
        if os.path.exists(path):
            sys.path.insert(0, os.path.curdir)

            for f in os.listdir(path):
                if f.endswith("_test.py") or f.endswith("_book.py") or f.endswith("_suite.py") or \
                   (f.startswith("test_") and f.endswith(".py")):
                    module_name = os.path.join(path, f[:len(f)-3]).replace("/", ".")
                    module = importlib.import_module(module_name)
                    for name in dir(module):
                        member = getattr(module, name)
                        if isinstance(member, type) and\
                           issubclass(member, bt.TestBook):
                            member_signature = signature(member)
                            needed_arguments = 0
                            for parameter in member_signature.parameters.values():
                                if parameter.default == Parameter.empty:
                                    needed_arguments += 1
                            if needed_arguments == 0:
                                tests.append(member())
                        elif isinstance(member, bt.TestBook) or\
                             isinstance(member, bt.Tests):
                            tests.append(member)

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

    args = parser.parse_args(args=arguments)

    if "exec" in args:
        exec_parsed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main(sys.argv)
