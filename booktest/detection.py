import os.path

import os
import importlib
import sys
from inspect import signature, Parameter
import types

import booktest as bt
from booktest.naming import clean_method_name, clean_test_postfix

from booktest.utils import SetupTeardown

BOOKTEST_SETUP_FILENAME = "__booktest__.py"

PROCESS_SETUP_TEARDOWN = "process_setup_teardown"


def empty_setup_teardown():
    # do nothing
    yield
    # do nothing


class BookTestSetup:

    def __init__(self, setup_teardown=None):
        if setup_teardown is None:
            setup_teardown = empty_setup_teardown
        self._setup_teardown = setup_teardown

    def setup_teardown(self):
        return SetupTeardown(self._setup_teardown)


def parse_booktest_setup(root, f, context=None):
    context = resolve_context(context)
    module_name = os.path.join(root, f[:len(f) - 3]).replace("/", ".")
    module = importlib.import_module(module_name, package=context)

    setup_teardown = None

    for name in dir(module):
        member = getattr(module, name)
        if name == PROCESS_SETUP_TEARDOWN and isinstance(member, types.FunctionType):
            method = member

            member_signature = signature(method)
            needed_arguments = 0
            for parameter in member_signature.parameters.values():
                if parameter.default == Parameter.empty:
                    needed_arguments += 1

            if needed_arguments != 0:
                raise Exception(f"booktest setup teardown method accepts 0 parameters, instead of {needed_arguments}")

            setup_teardown = member

    return BookTestSetup(setup_teardown)


def parse_test_file(root, f, context=None):
    context = resolve_context(context)

    rv = []
    test_suite_name = os.path.join(root, clean_test_postfix(f[:len(f) - 3]))
    module_name = os.path.join(root, f[:len(f) - 3]).replace("/", ".")
    module = importlib.import_module(module_name, package=context)
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
        elif isinstance(member, types.FunctionType) and name.startswith("test_"):
            member_signature = signature(member)
            needed_arguments = 0
            for parameter in member_signature.parameters.values():
                if parameter.default == Parameter.empty:
                    needed_arguments += 1
            test_cases.append((os.path.join(test_suite_name, clean_method_name(name)), member))

    if len(test_cases) > 0:
        rv.append(bt.Tests(test_cases))

    return rv

def get_context(config: dict):
    context_path = config.get("context", ".")

    if context_path is None or context_path == ".":
        context_path = os.path.curdir

    return context_path


def include_sys_path(root: str, python_path: str):
    for src_path in python_path.split(":"):
        if not os.path.isabs(src_path):
            src_path = os.path.join(root, src_path)
        if os.path.exists(src_path) and src_path not in sys.path:
            sys.path.insert(0, os.path.abspath(src_path))

def resolve_context(context):
    if context is None:
        context = os.path.curdir
    return context

def detect_setup(path, context=None):
    setup = None

    context = resolve_context(context)
    full_path = os.path.join(context, path)

    if os.path.exists(full_path):
        for root, dirs, files in os.walk(full_path):
            rel_path = os.path.relpath(root, context)
            for f in files:
                if f == BOOKTEST_SETUP_FILENAME:
                    setup = parse_booktest_setup(rel_path, f, context)

    return setup


def detect_tests(path, context=None):
    context = resolve_context(context)
    full_path = os.path.join(context, path)

    tests = []
    if os.path.exists(full_path):
        for root, dirs, files in os.walk(full_path):
            rel_path = os.path.relpath(root, context)
            for f in files:
                if f.endswith("_test.py") or f.endswith("_book.py") or f.endswith("_suite.py") or \
                   (f.startswith("test_") and f.endswith(".py")):
                    tests.extend(parse_test_file(rel_path, f, context))

    return tests


def detect_test_suite(path, context=None):
    tests = detect_tests(path, context)

    return bt.merge_tests(tests)
