import inspect

from booktest.config.naming import (
    class_to_test_path,
    clean_method_name,
    class_to_pytest_name,
    method_to_pytest_name
)
from booktest.core.testsuite import TestSuite


#
# Utilities related to use of reflection
# when inferring test cases for a test class
#


# The custom dictionary
class member_table(dict):
    def __init__(self):
        self.member_names = []

    def __setitem__(self, key, value):
        # if the key is not already defined, add to the
        # list of keys.
        if key not in self:
            self.member_names.append(key)

        # Call superclass
        dict.__setitem__(self, key, value)


# The metaclass
class OrderedClass(type):

    # The prepare function
    @classmethod
    def __prepare__(metacls, name, bases):  # No keywords in this case
        return member_table()

    # The metaclass invocation
    def __new__(cls, name, bases, classdict):
        # Note that we replace the classdict with a regular
        # dict before passing it to the superclass, so that we
        # don't continue to record member names after the class
        # has been created.
        result = type.__new__(cls, name, bases, dict(classdict))
        result.member_names = classdict.member_names
        return result


#
# Base class for test book instances
#


class TestBook(metaclass=OrderedClass):
    """
    Base class for test book instances
    """

    def __init__(self, full_path=None, name=None):
        """
        if path is None, a default path is generated. If name is not None,
        the name is used as a part of the default path name.

        The full_path parameter is aimed for e.g. generating different test
        cases from the same class, while name is aimed for fixing badly
        generated names (e.g. caused by all caps abbreviations).
        """
        if full_path is None:
            # Generate pytest-style name for the class
            full_path = class_to_pytest_name(type(self))
            if name is not None:
                # For custom name, replace the last part (class name)
                # e.g. "test/foo_test.py::FooTestBook" -> "test/foo_test.py::CustomName"
                parts = full_path.split("::")
                parts[-1] = name
                full_path = "::".join(parts)
        cases = []

        for name in self.member_names:
            if name.startswith("test_"):
                for m in inspect.getmembers(self):
                    if m[0] == name:
                        unbound = m[1].__func__
                        if not hasattr(unbound, "_self_type"):
                            unbound._self_type = type(self)
                        # Just use method name - TestSuite will prepend class path
                        # Method name in pytest format: "test_bar" (not cleaned)
                        cases.append([name, m[1]])

        self.test_suite = TestSuite(full_path, cases)
        self.cases = self.test_suite.cases

        self.__test_book_path = full_path

    def test_book_path(self):
        return self.__test_book_path

    def __repr__(self):
        return self.__test_book_path

