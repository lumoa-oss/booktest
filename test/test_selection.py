"""
Test for pytest-style test selection.
"""
import booktest as bt
from booktest.config.selection import is_selected, match_selection_with_test_suite_name


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

    def test_match_selection_with_test_suite_name(self, t: bt.TestCaseRun):
        """
        Test match_selection_with_test_suite_name function.

        This function is used to determine if a CLI selection pattern matches
        a test suite name (file path with optional class).
        """
        t.h1("match_selection_with_test_suite_name Tests")

        t.h2("Basic Directory Matching")
        test_cases = [
            # (selection, test_suite_name, should_match, description)
            # Basic prefix matching
            ("test", "test/test_foo.py", True, "'test' matches 'test/test_foo.py'"),
            ("test", "test/subdir/test_bar.py", True, "'test' matches nested paths"),
            ("test/subdir", "test/subdir/test_bar.py", True, "exact directory prefix"),
            ("other", "test/test_foo.py", False, "'other' doesn't match 'test/*'"),

            # Wildcard matching
            ("*", "test/test_foo.py", True, "'*' matches everything"),
            ("*", "anywhere/test.py", True, "'*' matches any path"),
        ]

        t.tln("Testing basic directory matching:")
        for selection, test_suite_name, should_match, description in test_cases:
            result = match_selection_with_test_suite_name(selection, test_suite_name)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {description}")
            t.tln(f"    selection='{selection}', test_suite='{test_suite_name}' → {result}")

            assert result == should_match, \
                f"{description}: Expected {should_match} but got {result}"

        t.tln()

        t.h2("Pytest-Style Class Matching")
        test_cases = [
            # Selection patterns that include class names (::ClassName)
            ("test/test_foo.py::FooClass", "test/test_foo.py::FooClass", True,
             "exact class match"),
            ("test/test_foo.py::FooClass", "test/test_foo.py::BarClass", False,
             "different class names"),
            ("test/test_foo.py", "test/test_foo.py::FooClass", True,
             "file selection DOES match classes in that file"),

            # Testing the :: separator handling
            ("test/test_foo.py::FooClass/test_bar", "test/test_foo.py::FooClass", True,
             "method selection matches class (forward slash)"),
        ]

        t.tln("Testing pytest-style class matching:")
        for selection, test_suite_name, should_match, description in test_cases:
            result = match_selection_with_test_suite_name(selection, test_suite_name)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {description}")
            t.tln(f"    selection='{selection}', test_suite='{test_suite_name}' → {result}")

            assert result == should_match, \
                f"{description}: Expected {should_match} but got {result}"

        t.tln()

        t.h2("Edge Cases")
        test_cases = [
            # Empty strings and boundary conditions
            ("", "test/test_foo.py", True, "empty selection matches everything"),
            ("test/", "test/test_foo.py", False, "trailing slash doesn't match (exact path mismatch)"),

            # Partial path matching
            ("test/examples", "test/examples/foo_test.py", True,
             "directory prefix matches file in directory"),
            ("test/examples", "test/examples_other/foo_test.py", False,
             "partial directory name doesn't match (must have / boundary)"),
            ("test/exa", "test/examples/foo_test.py", False,
             "incomplete directory name doesn't match"),

            # Case sensitivity
            ("Test", "test/test_foo.py", False, "case sensitive - 'Test' != 'test'"),

            # Pytest :: separator - partial class names don't match
            ("test/foo_test.py::Bar", "test/foo_test.py::BarClass", False,
             "partial class name doesn't match (Bar != BarClass)"),
            ("test/foo_test.py::BarClass", "test/foo_test.py::BarClass", True,
             "exact class name matches"),
        ]

        t.tln("Testing edge cases:")
        for selection, test_suite_name, should_match, description in test_cases:
            result = match_selection_with_test_suite_name(selection, test_suite_name)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {description}")
            t.tln(f"    selection='{selection}', test_suite='{test_suite_name}' → {result}")

            assert result == should_match, \
                f"{description}: Expected {should_match} but got {result}"

        t.tln()

        t.h2("Real-World Selection Patterns")
        test_cases = [
            # Typical CLI usage patterns
            ("test", "test/datascience/test_gpt.py", True,
             "selecting 'test' includes datascience subdirectory"),
            ("test/datascience", "test/datascience/test_gpt.py", True,
             "selecting subdirectory includes files in it"),
            ("test/datascience", "test/datascience/agents/test_agent.py", True,
             "selecting subdirectory includes nested files"),
            ("test/datascience/test_gpt.py", "test/datascience/test_gpt.py::TestGPT", True,
             "selecting file DOES match classes in that file"),
            ("test/datascience/test_gpt.py::TestGPT", "test/datascience/test_gpt.py::TestGPT", True,
             "selecting class with :: matches exactly"),

            # Multiple levels of nesting
            ("test/examples", "test/examples/example_suite/simple", True,
             "directory selection matches nested suite"),
            ("test/examples/example_suite", "test/examples/example_suite/simple", True,
             "nested directory selection"),
        ]

        t.tln("Testing real-world selection patterns:")
        for selection, test_suite_name, should_match, description in test_cases:
            result = match_selection_with_test_suite_name(selection, test_suite_name)
            status = "✓" if result == should_match else "✗"
            t.tln(f" {status} {description}")
            t.tln(f"    selection='{selection}', test_suite='{test_suite_name}' → {result}")

            assert result == should_match, \
                f"{description}: Expected {should_match} but got {result}"

        t.tln()
        t.tln("✓ All match_selection_with_test_suite_name tests passed!")
