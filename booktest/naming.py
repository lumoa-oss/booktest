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

