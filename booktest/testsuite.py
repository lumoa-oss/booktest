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


def cases_of(tests_or_suites) -> list:
    if isinstance(tests_or_suites, list):
        rv = []
        for s in tests_or_suites:
            rv.extend(cases_of(s))
        return rv
    else:
        return tests_or_suites.cases


def merge_tests(tests_or_suites) -> Tests:
    """
    Combines a list of Tests into a single Tests entity
    """
    cases = []
    for c in cases_of(tests_or_suites):
        cases.append([c[0], c[1]])

    return Tests(cases)


def decorate_tests(decorator, tests_or_suites) -> Tests:
    cases = []
    for c in cases_of(tests_or_suites):
        cases.append([c[0], decorator(c[1])])

    return Tests(cases)
