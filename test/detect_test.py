import booktest as bt
from booktest.core.testsuite import cases_of


def test_detect_tests(t: bt.TestCaseRun):
    """Test that filesystem and module detection find the same tests.

    This test verifies that both detection methods agree, rather than
    listing all tests (which would break every time a test is added).
    """
    t.h1("detecting tests:")

    fs_cases = cases_of(bt.detect_tests("test"))
    module_cases = cases_of(bt.detect_module_tests("test"))

    fs_set = set()
    module_set = set()

    for fs, module in zip(fs_cases, module_cases):
        fs_set.add(fs[0])
        module_set.add(module[0])

    # Check for mismatches between detection methods
    only_in_fs = fs_set - module_set
    only_in_module = module_set - fs_set

    t.h2("detection method agreement:")
    t.t(" * both methods detect some tests..").assertln(len(fs_set) > 0 and len(module_set) > 0)
    t.t(" * methods find same tests..").assertln(fs_set == module_set)

    if only_in_fs:
        t.tln()
        t.tln("tests only detected via filesystem:")
        for case in sorted(only_in_fs):
            t.fail().tln(f"   * {case}")

    if only_in_module:
        t.tln()
        t.tln("tests only detected via module:")
        for case in sorted(only_in_module):
            t.fail().tln(f"   * {case}")

    t.tln()
    t.t(" * detected test count is reasonable (> 100)..").assertln(len(fs_set) > 100)


def test_detect_setup(t: bt.TestCaseRun):
    t.h1("detecting setup:")

    fs_setup = bt.detect_setup("test")

    t.h2("fs setup:")

    t.t(" * asset fs setup was found..").assertln(fs_setup is not None)
    t.t(" * asset fs setup method was found..").assertln(fs_setup.setup_teardown is not None)

    t.h2("module setup:")

    module_setup = bt.detect_module_setup("test")

    t.t(" * asset module setup was found..").assertln(module_setup is not None)
    t.t(" * asset module setup method was found..").assertln(module_setup.setup_teardown is not None)

