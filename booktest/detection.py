import os.path

import os
import importlib
import sys
from inspect import signature, Parameter
import types

import booktest as bt
from booktest.naming import clean_method_name, clean_test_postfix

from booktest.testsuite import decorate_tests

BOOKTEST_SETUP_FILENAME = "__booktest__.py"

DEFAULT_DECORATOR_NAME = "default_decorator"


class BookTestSetup:

    def __init__(self, booktest_decorator=None):
        self.booktest_decorator = booktest_decorator

    def decorate_test(self, test):
        if self.booktest_decorator is None:
            return test
        else:
            return decorate_tests(self.booktest_decorator, test)

    def decorate_tests(self, tests):
        return list([self.decorate_test(i) for i in tests])


def parse_booktest_setup(root, f):
    module_name = os.path.join(root, f[:len(f) - 3]).replace("/", ".")
    module = importlib.import_module(module_name)

    process_fixture = None

    for name in dir(module):
        member = getattr(module, name)
        if isinstance(member, types.FunctionType) and name == DEFAULT_DECORATOR_NAME:
            member_signature = signature(member)
            needed_arguments = 0
            for parameter in member_signature.parameters.values():
                if parameter.default == Parameter.empty:
                    needed_arguments += 1

            if needed_arguments != 1:
                raise Exception("booktest decorators accepts only one parameter")

            process_fixture = member

    return BookTestSetup(process_fixture)


def parse_test_file(root, f):
    rv = []
    setup = BookTestSetup()
    test_suite_name = os.path.join(root, clean_test_postfix(f[:len(f) - 3]))
    module_name = os.path.join(root, f[:len(f) - 3]).replace("/", ".")
    module = importlib.import_module(module_name)
    test_cases = []
    for name in dir(module):
        member = getattr(module, name)
        if isinstance(member, type) and \
                issubclass(member, bt.TestBook):
            member_signature = signature(member)
            needed_arguments = 0
            for parameter in member_signature.parameters.values():
                if parameter.default == Parameter.empty:
                    needed_arguments += 1
            if needed_arguments == 0:
                rv.append(member())
        elif isinstance(member, bt.TestBook) or \
                isinstance(member, bt.Tests):
            rv.append(member)
        elif isinstance(member, types.FunctionType) and name == DEFAULT_DECORATOR_NAME:
            setup = BookTestSetup(member)
        elif isinstance(member, types.FunctionType) and name.startswith("test_"):
            member_signature = signature(member)
            needed_arguments = 0
            for parameter in member_signature.parameters.values():
                if parameter.default == Parameter.empty:
                    needed_arguments += 1
            test_cases.append((os.path.join(test_suite_name, clean_method_name(name)), member))

    if len(test_cases) > 0:
        rv.append(bt.Tests(test_cases))

    return setup.decorate_tests(rv)


def detect_setup(path, include_in_sys_path=False):
    setup = None
    if os.path.exists(path):
        if include_in_sys_path:
            sys.path.insert(0, os.path.curdir)

        for root, dirs, files in os.walk(path):
            for f in files:
                if f == BOOKTEST_SETUP_FILENAME:
                    setup = parse_booktest_setup(root, f)

    return setup


def detect_tests(path, include_in_sys_path=False):
    tests = []
    if os.path.exists(path):
        if include_in_sys_path:
            sys.path.insert(0, os.path.curdir)

        for root, dirs, files in os.walk(path):
            module_tests = []
            module_setup = BookTestSetup(None)
            for f in files:
                if f == BOOKTEST_SETUP_FILENAME:
                    module_setup = parse_booktest_setup(root, f)
                elif f.endswith("_test.py") or f.endswith("_book.py") or f.endswith("_suite.py") or \
                        (f.startswith("test_") and f.endswith(".py")):
                    module_tests.extend(parse_test_file(root, f))

            tests.extend(module_setup.decorate_tests(module_tests))

    return tests


def detect_test_suite(path, include_in_sys_path=False):
    tests = detect_tests(path, include_in_sys_path)

    return bt.merge_tests(tests)
