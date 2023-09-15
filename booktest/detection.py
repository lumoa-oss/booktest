import os.path

import os
import importlib
import sys
from inspect import signature, Parameter

import booktest as bt


def detect_tests(path, include_in_sys_path=False):
    tests = []
    if os.path.exists(path):
        if include_in_sys_path:
            sys.path.insert(0, os.path.curdir)

        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith("_test.py") or f.endswith("_book.py") or f.endswith("_suite.py") or \
                        (f.startswith("test_") and f.endswith(".py")):
                    module_name = os.path.join(root, f[:len(f) - 3]).replace("/", ".")
                    module = importlib.import_module(module_name)
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
                                tests.append(member())
                        elif isinstance(member, bt.TestBook) or \
                                isinstance(member, bt.Tests):
                            tests.append(member)

    return tests


def detect_test_suite(path, include_in_sys_path=False):
    tests = detect_tests(path, include_in_sys_path)

    return bt.merge_tests(tests)
