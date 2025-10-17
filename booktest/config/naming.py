import inspect


#
# Utilities related to test naming
#


def camel_case_to_snake_case(name):
    rv = ""
    is_prev_lower_case = False
    for i in name:
        is_upper_case = i.isupper()
        if is_prev_lower_case and is_upper_case:
            rv += "_"
        rv += i.lower()
        is_prev_lower_case = not is_upper_case

    return rv


def clean_test_postfix(name):
    name = name.lower()
    if name.endswith("_testbook"):
        name = name[0:(len(name) - len("_testbook"))]
    elif name.endswith("testbook"):
        name = name[0:(len(name) - len("testbook"))]
    elif name.endswith("_test_book"):
        name = name[0:(len(name) - len("_test_book"))]
    elif name.endswith("test_book"):
        name = name[0:(len(name) - len("test_book"))]
    elif name.endswith("_book"):
        name = name[0:(len(name) - len("_book"))]
    elif name.endswith("book"):
        name = name[0:(len(name) - len("book"))]
    elif name.endswith("_test"):
        name = name[0:(len(name) - len("_test"))]
    elif name.endswith("test"):
        name = name[0:(len(name) - len("test"))]
    return name


def clean_class_name(name: str):
    return clean_test_postfix(camel_case_to_snake_case(name))


def clean_method_name(name: str):
    if name.startswith("test_"):
        return name[len("test_"):]
    else:
        return None


def class_to_test_path(clazz):
    path_and_file = inspect.getmodule(clazz).__name__.split(".")
    path = path_and_file[:len(path_and_file)-1]
    file_name = path_and_file[len(path_and_file)-1]
    test_name_path = []
    test_name_path.extend(path)

    cleaned_file_name = clean_test_postfix(file_name)
    cleaned_class_name = clean_class_name(clazz.__name__)
    test_name_path.append(cleaned_file_name)
    if cleaned_file_name.replace("_", "") != \
       cleaned_class_name.replace("_", ""):
        # be lenient with underscores for backward compatibility
        test_name_path.append(cleaned_class_name)

    return "/".join(test_name_path)


#
# Pytest-style naming (new format)
#


def class_to_pytest_name(clazz):
    """
    Convert a test class to pytest-style name.

    Example:
        Module: test.examples.foo_test
        Class: FooTestBook
        Result: test/examples/foo_test.py::FooTestBook
    """
    module = inspect.getmodule(clazz)
    module_path = module.__name__.replace(".", "/") + ".py"
    class_name = clazz.__name__

    return f"{module_path}::{class_name}"


def method_to_pytest_name(clazz, method_name: str):
    """
    Convert a test method to pytest-style name.

    Example:
        Module: test.examples.foo_test
        Class: FooTestBook
        Method: test_bar
        Result: test/examples/foo_test.py::FooTestBook::test_bar
    """
    class_path = class_to_pytest_name(clazz)
    return f"{class_path}::{method_name}"


def function_to_pytest_name(module_name: str, function_name: str):
    """
    Convert a standalone test function to pytest-style name.

    Example:
        Module: test.examples.simple_test
        Function: test_example
        Result: test/examples/simple_test.py::test_example
    """
    module_path = module_name.replace(".", "/") + ".py"
    return f"{module_path}::{function_name}"


def to_filesystem_path(pytest_name: str) -> str:
    """
    Convert pytest-style name to safe filesystem path.

    This is the internal representation used for file operations.
    Replaces :: with / to create a valid filesystem path.

    Example:
        Input:  test/foo_test.py::FooTestBook::test_bar
        Output: test/foo_test.py/FooTestBook/test_bar

        Input:  test/simple_test.py::test_example
        Output: test/simple_test.py/test_example
    """
    return pytest_name.replace("::", "/")


def from_filesystem_path(fs_path: str) -> str:
    """
    Convert filesystem path back to pytest-style name.

    Uses heuristic: if path contains '.py/', convert to '.py::'
    Otherwise returns as-is for backwards compatibility with old format.

    Example:
        Input:  test/foo_test.py/FooTestBook/test_bar
        Output: test/foo_test.py::FooTestBook::test_bar

        Input:  test/foo/bar (old format)
        Output: test/foo/bar (unchanged)
    """
    import re
    # Match pattern: {anything}.py/{rest}
    match = re.match(r'(.*?\.py)/(.*)', fs_path)
    if match:
        file_part = match.group(1)
        rest_part = match.group(2)
        # Convert remaining / to ::
        pytest_rest = rest_part.replace("/", "::")
        return f"{file_part}::{pytest_rest}"
    else:
        # Legacy format - return as-is
        return fs_path


def is_pytest_name(name: str) -> bool:
    """
    Check if a name is in pytest format (contains ::).

    Example:
        is_pytest_name("test/foo_test.py::test_bar") → True
        is_pytest_name("test/foo/bar") → False
    """
    return "::" in name


def normalize_test_name(name: str) -> str:
    """
    Normalize test name to internal filesystem format.

    Accepts both pytest format and legacy format.
    Returns filesystem-safe path for internal use.

    Example:
        Input:  test/foo_test.py::test_bar (pytest format)
        Output: test/foo_test.py/test_bar (filesystem)

        Input:  test/foo/bar (legacy format)
        Output: test/foo/bar (unchanged)
    """
    if is_pytest_name(name):
        return to_filesystem_path(name)
    else:
        return name

