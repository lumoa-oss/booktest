import os
import argparse

from booktest import detect_module_test_suite, detect_module_setup
from booktest.testsuite import cases_of


class Books:
    """ This is a for helping run books locally e.g. inside pytest or inside a script"""

    def __init__(self, book_src_module_or_path, books_module_or_path, selection=None):
        if isinstance(book_src_module_or_path, str):
            self.book_src_dir = book_src_module_or_path
        else:
            self.book_src_dir = book_src_module_or_path.__name__
        if isinstance(books_module_or_path, str):
            self.books_dir = books_module_or_path
        else:
            self.books_dir = os.path.abspath(books_module_or_path.__path__[0])

        self.test_suites = detect_module_test_suite(self.book_src_dir, selection)
        self.book_setup = detect_module_setup("book")
        self.parser = argparse.ArgumentParser(description='run book test operations')
        self.test_suites.setup_parser(self.parser)

    def list_tests(self, prefix=""):
        test_names = []
        for name, _ in cases_of(self.test_suites):
            if name.startswith(prefix):
                test_names.append(name)
        return test_names

    def run_test(self, test_case, cache={}):
        return self.test_suites.exec(self.books_dir,
                                     ["-v", "-L", test_case],
                                     cache=cache,
                                     extra_default_config={
                                         "books_path": self.books_dir
                                     },
                                     setup=self.book_setup)

    def assert_test(self, test_case):
        assert self.run_test(test_case) == 0