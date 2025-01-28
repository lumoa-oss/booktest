import os.path

import os
import importlib
import pkgutil
import sys
from inspect import signature, Parameter
import types

import booktest as bt
from booktest.naming import clean_method_name, clean_test_postfix
from booktest.selection import is_selected_test_suite

from booktest.utils import SetupTeardown

BOOKTEST_SETUP_MODULE = "__booktest__"

BOOKTEST_SETUP_FILENAME = f"{BOOKTEST_SETUP_MODULE}.py"

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


def parse_booktest_setup_module(module):
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


def parse_booktest_setup(root, f):
    module_name = os.path.join(root, f[:len(f) - 3]).replace("/", ".")
    module = importlib.import_module(module_name)

    return parse_booktest_setup_module(module)


def get_module_tests(test_suite_name, module_name):
    rv = []

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


def get_file_tests(root, f, selection):
    test_suite_name = os.path.join(root, clean_test_postfix(f[:len(f) - 3]))
    if is_selected_test_suite(test_suite_name, selection):
        module_name = os.path.join(root, f[:len(f) - 3]).replace("/", ".")
        return get_module_tests(test_suite_name, module_name)
    else:
        return []


def include_sys_path(python_path: str):
    for src_path in python_path.split(":"):
        if os.path.exists(src_path) and src_path not in sys.path:
            sys.path.insert(0, os.path.abspath(src_path))


def detect_setup(path):
    setup = None

    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if f == BOOKTEST_SETUP_FILENAME:
                    setup = parse_booktest_setup(root, f)

    return setup


def detect_module_setup(module_name):
    setup = None

    module = importlib.import_module(module_name)
    module_dir = os.path.dirname(module.__file__)

    for _, submodule_path, is_pkg in pkgutil.walk_packages([module_dir], module_name + "."):
        submodule_parts = submodule_path.split(".")
        submodule_name = submodule_parts[len(submodule_parts) - 1]
        if submodule_name == BOOKTEST_SETUP_MODULE:
            submodule = importlib.import_module(submodule_path)
            setup = parse_booktest_setup_module(submodule)

    return setup


def detect_tests(path, selection=None):
    """ Detects tests in a file system path"""
    tests = []
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith("_test.py") or f.endswith("_book.py") or f.endswith("_suite.py") or \
                   (f.startswith("test_") and f.endswith(".py")):
                    tests.extend(get_file_tests(root, f, selection))

    return tests


def detect_test_suite(path):
    tests = detect_tests(path)

    return bt.merge_tests(tests)


def detect_module_tests(module_name, selection=None):
    """ Detects tests in a module. This is needed e.g. in pants, where original FS is not easily accessible """
    tests = []

    module = importlib.import_module(module_name)
    module_dir = os.path.dirname(module.__file__)

    for _, submodule_name, is_pkg in pkgutil.walk_packages([module_dir], module_name + "."):
        submodule_path = str(submodule_name).split(".")
        test_name = submodule_path[len(submodule_path) - 1]
        if test_name.endswith("_test") or test_name.endswith("_book") or test_name.endswith("_suite") or\
           test_name.startswith("test_"):
            submodule_path[len(submodule_path) - 1] = clean_test_postfix(test_name)
            test_suite_name = os.path.join(*submodule_path)
            if is_selected_test_suite(test_suite_name, selection):
                tests.extend(get_module_tests(test_suite_name, submodule_name))

    return tests


def detect_module_test_suite(path, selection=None):
    tests = detect_module_tests(path, selection)

    return bt.merge_tests(tests)

