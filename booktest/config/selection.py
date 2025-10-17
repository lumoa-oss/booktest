def is_selected(test_name, selection):
    """
    checks whether the test name is selected
    based on the selection

    Supports both pytest format (test/foo_test.py::test_bar)
    and legacy format (test/foo/bar).
    """
    from booktest.config.naming import normalize_test_name

    if selection is None:
        return True

    # Normalize test name to filesystem format for comparison
    # This handles both pytest format (with ::) and legacy format
    test_name_fs = normalize_test_name(test_name)

    # filter negatives
    negatives = 0
    skip_key = "skip:"
    for s in selection:
        if s.startswith(skip_key):
            s = s[len(skip_key):]
            # Normalize selection pattern
            s_fs = normalize_test_name(s)
            if (test_name_fs.startswith(s_fs) and
                    (len(s_fs) == 0
                     or len(test_name_fs) == len(s_fs)
                     or test_name_fs[len(s_fs)] == '/')):
                return False
            negatives += 1

    if negatives == len(selection):
        return True
    else:
        for s in selection:
            # Normalize selection pattern
            s_fs = normalize_test_name(s)
            if s == '*' or \
                    (test_name_fs.startswith(s_fs) and
                     (len(s_fs) == 0
                      or len(test_name_fs) == len(s_fs)
                      or test_name_fs[len(s_fs)] == '/')):
                return True
        return False

def match_selection_with_test_suite_name(s, test_suite_name):
    from booktest.config.naming import normalize_test_name

    test_suite_name_fs = normalize_test_name(test_suite_name)
    s_fs = normalize_test_name(s)

    return (s == '*' or
            s_fs.startswith(test_suite_name_fs + "/") or
            s_fs.startswith(test_suite_name_fs + "::") or
            (test_suite_name_fs.startswith(s_fs) and
             (len(s_fs) == 0
              or len(test_suite_name_fs) == len(s_fs)
              or test_suite_name_fs[len(s_fs)] == '/')))


def is_selected_test_suite(test_suite_name, selection):
    """
    checks whether the test suiite is selected
    based on the selection

    Supports both pytest format (test/foo_test.py::TestClass)
    and legacy format (test/foo).
    """
    from booktest.config.naming import normalize_test_name

    if selection is None:
        return True

    # filter negatives
    negatives = 0
    skip_key = "skip:"
    for s in selection:
        if s.startswith(skip_key):
            s = s[len(skip_key):]

            if match_selection_with_test_suite_name(s, test_suite_name):
                return False

            negatives += 1

    if negatives == len(selection):
        return True
    else:
        for s in selection:
            if match_selection_with_test_suite_name(s, test_suite_name):
                return True
        return False
