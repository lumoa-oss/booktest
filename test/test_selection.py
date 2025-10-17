"""
Test for pytest-style test selection.
"""
import booktest as bt
from booktest.config.selection import is_selected


class TestSelection(bt.TestBook):

    def test_file_selection(self, t: bt.TestCaseRun):
        """
        Test that selecting a file path matches all tests in that file.
        """
        t.h1("File Path Selection")

        test_cases = [
            # (test_name, selection, should_match)
            ("test/foo_test.py::test_bar", ["test/foo_test.py"], True),
            ("test/foo_test.py::FooBook/test_bar", ["test/foo_test.py"], True),
            ("test/foo_test.py::FooBook/test_baz", ["test/foo_test.py"], True),
            ("test/other_test.py::test_other", ["test/foo_test.py"], False),
        ]

        t.tln("Testing file path selection:")
        for test_name, selection, should_match in test_cases:
            result = is_selected(test_name, selection)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {test_name} with selection {selection}: {result}")

            assert result == should_match, \
                f"Expected {should_match} but got {result} for {test_name} with {selection}"

        t.tln()
        t.tln("✓ All file selection tests passed!")

    def test_class_selection(self, t: bt.TestCaseRun):
        """
        Test that selecting a class matches all tests in that class.
        """
        t.h1("Class Selection")

        test_cases = [
            # (test_name, selection, should_match)
            ("test/foo_test.py::FooBook/test_bar", ["test/foo_test.py::FooBook"], True),
            ("test/foo_test.py::FooBook/test_baz", ["test/foo_test.py::FooBook"], True),
            ("test/foo_test.py::test_standalone", ["test/foo_test.py::FooBook"], False),
            ("test/foo_test.py::BarBook/test_other", ["test/foo_test.py::FooBook"], False),
        ]

        t.tln("Testing class selection:")
        for test_name, selection, should_match in test_cases:
            result = is_selected(test_name, selection)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {test_name} with selection {selection}: {result}")

            assert result == should_match, \
                f"Expected {should_match} but got {result} for {test_name} with {selection}"

        t.tln()
        t.tln("✓ All class selection tests passed!")

    def test_directory_selection(self, t: bt.TestCaseRun):
        """
        Test that selecting a directory matches all tests in that directory.
        """
        t.h1("Directory Selection")

        test_cases = [
            # (test_name, selection, should_match)
            ("test/examples/foo_test.py::test_bar", ["test/examples"], True),
            ("test/examples/subdir/bar_test.py::test_baz", ["test/examples"], True),
            ("test/other/foo_test.py::test_bar", ["test/examples"], False),
        ]

        t.tln("Testing directory selection:")
        for test_name, selection, should_match in test_cases:
            result = is_selected(test_name, selection)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {test_name} with selection {selection}: {result}")

            assert result == should_match, \
                f"Expected {should_match} but got {result} for {test_name} with {selection}"

        t.tln()
        t.tln("✓ All directory selection tests passed!")

    def test_exact_match(self, t: bt.TestCaseRun):
        """
        Test that exact test name matches.
        """
        t.h1("Exact Match Selection")

        test_cases = [
            # (test_name, selection, should_match)
            ("test/foo_test.py::test_bar", ["test/foo_test.py::test_bar"], True),
            ("test/foo_test.py::FooBook/test_bar", ["test/foo_test.py::FooBook/test_bar"], True),
            ("test/foo_test.py::test_bar", ["test/foo_test.py::test_baz"], False),
        ]

        t.tln("Testing exact match selection:")
        for test_name, selection, should_match in test_cases:
            result = is_selected(test_name, selection)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {test_name} with selection {selection}: {result}")

            assert result == should_match, \
                f"Expected {should_match} but got {result} for {test_name} with {selection}"

        t.tln()
        t.tln("✓ All exact match tests passed!")
