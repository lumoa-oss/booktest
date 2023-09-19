from booktest.tests import Tests
from os import path


class TestSuite(Tests):
    def __init__(self, suite_name, cases):
        self.cases = []
        for c in cases:
            self.cases.append([path.join(suite_name, c[0]), c[1]])


#
# Test suite manipulation (renames, merges)
#


def drop_prefix(prefix: str, tests: Tests) -> Tests:
    """
    removes a prefix like 'test' from all test.
    this can be used, if the test name inference adds
    unnecessary decorations to test names.
    """
    cases = []
    full_prefix = prefix
    if not full_prefix.endswith("/"):
        full_prefix += "/"
    for case in tests.cases:
        if case[0].startswith(full_prefix):
            cases.append([case[0][len(full_prefix):], case[1]])

    return Tests(cases)


def merge_tests(suites: list) -> Tests:
    """
    Combines a list of Tests into a single Tests entity
    """
    cases = []
    for s in suites:
        for c in s.cases:
            cases.append([c[0], c[1]])

    return Tests(cases)
