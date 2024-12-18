import booktest as bt
from booktest.testsuite import cases_of


def test_detect_tests(t: bt.TestCaseRun):
    t.h1("detecting tests:")

    fs_cases = cases_of(bt.detect_tests("test"))
    module_cases = cases_of(bt.detect_module_tests("test"))

    cases = set()
    fs_set = set()
    module_set = set()

    for fs, module in zip(fs_cases, module_cases):
        cases.add(fs[0])
        fs_set.add(fs[0])
        cases.add(module[0])
        module_set.add(module[0])

    for case in list(sorted(cases)):
        t.t(f" * {case}..").assertln(case in fs_set and case in module_set)
        if case not in fs_set:
            t.fail().tln("   * not detected via fs")
        if case not in module_set:
            t.fail().tln("   * not detected via module")

    t.tln()
    t.keyvalueln("count:", len(cases))


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

