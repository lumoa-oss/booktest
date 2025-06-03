import asyncio
import inspect
import os.path as path
import os
import time
import traceback
import pickle

from booktest.coroutines import maybe_async_call
from booktest.dependencies import remove_decoration, get_decorated_attr
from booktest.testcaserun import TestCaseRun
from booktest.reports import TestResult, CaseReports, UserRequest, Metrics
from booktest.review import end_report, create_index, start_report


#
# Test running
#

def method_identity(method):
    self = get_decorated_attr(method, "__self__")
    func = get_decorated_attr(method, "__func__")

    if func is None:
        func = method

    return self, func


def match_method(matcher, method):
    matcher_self, matcher_func = method_identity(matcher)
    method_self, method_func = method_identity(method)
    return matcher_func == method_func and (matcher_self == method_self or matcher_self is None)


class TestRun:
    """
    Runs a selection of test cases from the test-object
    """
    def __init__(self,
                 exp_dir,
                 out_dir,
                 report_dir,
                 tests,
                 selected_cases,
                 config,
                 cache,
                 output=None,
                 allocations=None,
                 preallocations=None):
        self.exp_dir = exp_dir
        self.report_dir = report_dir
        self.out_dir = out_dir
        self.tests = tests
        self.selected_cases = selected_cases
        self.config = config
        self.verbose = config.get("verbose", False)
        self.fail_fast = config.get("fail_fast", False)
        self.continue_test = config.get("continue", False)
        self.cache = cache
        self.output = output
        if allocations is None:
            allocations = set()
        self.allocations = allocations
        if preallocations is None:
            preallocations = {}
        self.preallocations = preallocations

    def get_test_result(self, case, method):
        for t in self.tests.cases:
            # a bit hacky way for figuring out the dependencies
            if match_method(method, t[1]):
                bin_path = self.tests.test_result_path(self.out_dir, t[0])
                if bin_path not in self.cache:
                    if path.exists(bin_path):
                        with open(bin_path, 'rb') as file:
                            rv = pickle.load(file)
                            self.cache[bin_path] = rv
                    else:
                        raise Exception(
                            f"case {case.name} dependency {t[0]}" +
                            f" missing in '{bin_path}'")

                return True, self.cache[bin_path]

        return False, None

    def save_test_result(self, case_path, result):
        bin_path = self.tests.test_result_path(self.out_dir, case_path)
        self.cache[bin_path] = result
        if result is None:
            if path.exists(bin_path):
                os.remove(bin_path)
        else:
            with open(bin_path, 'wb') as file:
                pickle.dump(result, file)

    async def run_case(self, case_path, case, title=None) \
            -> (TestResult, UserRequest, float):
        t = TestCaseRun(self, case_path, self.config, self.output)
        t.start(title)
        try:
            rv = await maybe_async_call(case, [t], {})
        except Exception as e:
            t.iln().fail().iln(f"test raised exception {e}:")
            t.iln(traceback.format_exc())
            rv = None

        result, interaction = t.end()
        if result is TestResult.OK or result is TestResult.DIFF:
            # if the test case return a value, store it in a cache
            self.save_test_result(case_path, rv)

        return result, interaction, t.took_ms

    def print(self, *args, sep=' ', end='\n'):
        print(*args, sep=sep, end=end, file=self.output)

    async def run_async(self):
        #
        # 1. prepare variables and state
        #

        # 1.1 initialize basic variables
        before = time.time()
        rv = TestResult.OK
        failed = []
        passed = []
        oks = 0
        fails = 0
        tests = 0
        os.system(f"mkdir -p {self.report_dir}")
        report_file = path.join(self.report_dir, "cases.txt")

        # 1.2. To continue testing, we need to read
        #      the old case report so that we continue from there
        old_report = CaseReports.of_file(report_file)

        done, todo = old_report.cases_to_done_and_todo(self.selected_cases, self.config)

        #
        # 2. Test
        #

        # 2.1 inform user that the testing has started
        start_report(self.print)

        # 2.2. run test.
        #      update the report as we test to allow hitting
        #      CTRL-C and continuing from the last succesful test
        with open(report_file, "w") as report_f:

            # 2.2.1 add previously passed items to test
            if old_report is not None:
                for i in old_report.cases:
                    if i[0] not in todo:
                        CaseReports.write_case(
                            report_f, i[0], i[1], i[2])

            # 2.2.2 run cases
            for case_name in todo:
                case = self.tests.get_case(case_name)
                res, request, duration = \
                    await self.run_case(case_name, case)

                if res == TestResult.DIFF \
                   or res == TestResult.FAIL:
                    if rv != TestResult.FAIL:
                        rv = res
                    # treat both FAIL and DIFF as failures
                    failed.append(case_name)
                    fails += 1
                    tests += 1
                else:
                    passed.append(case_name)
                    oks += 1
                    tests += 1

                CaseReports.write_case(
                    report_f, case_name, res, duration)

                # manage situations, where testing should
                # be aborted
                if request == UserRequest.ABORT or \
                   (self.fail_fast and fails > 0):
                    break

        took = int((time.time() - before) * 1000)

        Metrics(took).to_file(
            os.path.join(
                self.out_dir, "metrics.json"))

        end_report(self.print, failed, tests, took)

        create_index(self.exp_dir, self.tests.all_names())

        return rv

    def run(self):
        return asyncio.run(self.run_async())
