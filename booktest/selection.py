def is_selected(test_name, selection):
    """
    checks whether the test name is selected
    based on the selection
    """
    if selection is None:
        return True

    # filter negatives
    negatives = 0
    skip_key = "skip:"
    for s in selection:
        if s.startswith(skip_key):
            s = s[len(skip_key):]
            if (test_name.startswith(s) and
                    (len(s) == 0
                     or len(test_name) == len(s)
                     or test_name[len(s)] == '/')):
                return False
            negatives += 1

    if negatives == len(selection):
        return True
    else:
        for s in selection:
            if s == '*' or \
                    (test_name.startswith(s) and
                     (len(s) == 0
                      or len(test_name) == len(s)
                      or test_name[len(s)] == '/')):
                return True
        return False


def is_selected_test_suite(test_suite_name, selection):
    """
    checks whether the test suiite is selected
    based on the selection
    """
    if selection is None:
        return True

    # filter negatives
    negatives = 0
    skip_key = "skip:"
    for s in selection:
        if s.startswith(skip_key):
            s = s[len(skip_key):]
            if (test_suite_name.startswith(s) and
                    (len(s) == 0
                     or len(test_suite_name) == len(s)
                     or test_suite_name[len(s)] == '/')):
                return False
            negatives += 1

    if negatives == len(selection):
        return True
    else:
        for s in selection:
            if (s == '*' or
                s.startswith(test_suite_name + "/") or
                (test_suite_name.startswith(s) and
                 (len(s) == 0
                  or len(test_suite_name) == len(s)
                  or test_suite_name[len(s)] == '/'))):
                return True
        return False
