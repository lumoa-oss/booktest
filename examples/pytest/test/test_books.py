import argparse

import booktest as bt
from booktest.testsuite import cases_of

import pytest


BOOK_SRC_DIR = "book"
BOOK_MODULE = BOOK_SRC_DIR

TEST_SUITES = bt.detect_test_suite(BOOK_SRC_DIR)
MODULE_TEST_SUITES = bt.detect_module_test_suite(BOOK_MODULE)

BOOK_SETUP = bt.detect_setup("book")
MODULE_BOOK_SETUP = bt.detect_module_setup("book")

BOOKS_ROOT_DIR = "books"


def get_module_test_suite():
    return bt.detect_module_test_suite(BOOK_MODULE)


def get_test_suite():
    return bt.detect_test_suite(BOOK_SRC_DIR)


def get_book_setup():
    return bt.detect_setup("book")


def get_module_book_setup():
    return bt.detect_module_setup("book")


def discover_tests_in_fs(prefix=""):
    test_names = []
    for name, _ in cases_of(get_test_suite()):
        if name.startswith(prefix):
            test_names.append(name)
    return test_names


def discover_tests_in_module(prefix=""):
    """ NOTE: e.g. in pants, you cannot easiy access the test FS, so you need to use this function """
    test_names = []
    for name, _ in cases_of(get_module_test_suite()):
        if name.startswith(prefix):
            test_names.append(name)
    return test_names


@pytest.mark.parametrize("test_case", discover_tests_in_fs(BOOK_SRC_DIR))
def test_fs_detect(test_case):
    tests = get_test_suite()
    setup = get_book_setup()

    assert tests.exec(BOOKS_ROOT_DIR, ["-v", "-L", test_case], setup=setup) == 0


@pytest.mark.parametrize("test_case", discover_tests_in_module(BOOK_MODULE))
def test_module_detect(test_case):
    tests = get_module_test_suite()
    setup = get_module_book_setup()

    assert tests.exec(BOOKS_ROOT_DIR, ["-v", "-L", test_case], setup=setup) == 0