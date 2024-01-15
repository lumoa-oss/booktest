import asyncio
import os
import time
from collections import defaultdict

from booktest.review import review, create_index, report_case_result, report_case, report_case_begin, start_report, \
    end_report
from booktest.testrun import TestRun
from booktest.reports import CaseReports, Metrics, test_result_to_exit_code, read_lines, write_lines, UserRequest, \
    TestResult


#
# Parallelization and test execution support:
#


class RunBatch:
    #
    # Tests are collected into suites, that are
    # treated as test batches run by process pools
    #

    def __init__(self,
                 exp_dir: str,
                 out_dir: str,
                 tests,
                 config: dict,
                 cache):
        self.exp_dir = exp_dir
        self.out_dir = out_dir
        self.tests = tests
        self.config = config
        self.cache = cache

    def __call__(self, case):
        path = case.split("/")
        batch_name = ".".join(path)
        batch_dir = \
            os.path.join(
                self.out_dir,
                ".batches",
                batch_name)

        output_file = \
            os.path.join(
                self.out_dir,
                ".batches",
                batch_name,
                "output.txt")

        output = open(output_file, "w")

        try:
            run = TestRun(
                self.exp_dir,
                self.out_dir,
                batch_dir,
                self.tests,
                [case],
                self.config,
                self.cache,
                output)

            rv = test_result_to_exit_code(run.run())
        finally:
            output.close()

        return rv


def case_batch_dir_and_report_file(batches_dir, name):
    path = ".".join(name.split("/"))
    batch_dir = os.path.join(batches_dir, path)
    return batch_dir, os.path.join(batch_dir, "cases.txt")


def parallel_run_tests(exp_dir,
                       out_dir,
                       tests,
                       cases: list,
                       config: dict,
                       cache):
    from multiprocessing import Pool

    begin = time.time()

    #
    # 1. load old report and prepare directories
    #
    report_file = os.path.join(out_dir, "cases.txt")
    case_reports = CaseReports.of_file(report_file)

    batches_dir = \
        os.path.join(
            out_dir,
            ".batches")

    os.makedirs(batches_dir, exist_ok=True)

    #
    # 2. prepare batch jobs for process pools
    #

    # 2.1 configuration. batches must not be interactive

    import copy
    job_config = copy.copy(config)
    job_config["interactive"] = False
    job_config["always_interactive"] = False

    run_batch = RunBatch(exp_dir, out_dir, tests, job_config, cache)

    # 2.2 split test cases into batches
    dependencies = defaultdict(set)
    todo = set()
    for name in cases:
        method = tests.get_case(name)
        for dependency in tests.method_dependencies(method, cases):
            dependencies[name].add(dependency)
        todo.add(name)

    todo = sorted(list(todo))
    done = set()

    def ready_cases():
        rv = []
        for name in todo:
            ready = True
            for dependency in dependencies[name]:
               if dependency not in done:
                   ready = False
            if ready:
                rv.append(name)
        return rv

    reports = case_reports.cases

    passed = case_reports.passed()

    cont = config.get("continue", False)
    fail_fast = config.get("fail_fast", False)

    reviews = []

    start_report(print)
    abort = False

    start_report(print)

    exit_code = 0

    batch_dirs = []

    import coverage
    try:
        with Pool(os.cpu_count(),
                  initializer=coverage.process_startup) as p:

            scheduled = dict()

            while len(done) < len(todo) and not abort:
                ready = ready_cases()

                # start async jobs
                for name in ready:
                    if name not in done and name not in scheduled:
                        batch_dir, batch_report_file = case_batch_dir_and_report_file(batches_dir, name)
                        batch_dirs.append(batch_dir)
                        os.makedirs(batch_dir, exist_ok=True)
                        batch_reports = list([i for i in reports if i[0] == name])[:1]
                        CaseReports(batch_reports)\
                            .to_file(batch_report_file)

                        scheduled[name] = p.apply_async(run_batch, args=[name])

                #
                # 3. run test in a process pool
                #
                done_tasks = set()
                while len(done_tasks) == 0:
                    for name, task in scheduled.items():
                        if task.ready():
                            done_tasks.add(name)
                    if len(done_tasks) == 0:
                        break
                    time.sleep(0.001)

                done |= done_tasks
                for i in done_tasks:
                    del scheduled[i]

                # 3.1 Run test in parallel processes
                #     initialize each process with coverage.process_startup
                #     method

                report_txt = os.path.join(out_dir, "cases.txt")

                for case_name in done_tasks:
                    batch_report_file = case_batch_dir_and_report_file(batches_dir, case_name)[1]
                    case_reports = CaseReports.of_file(batch_report_file)
                    if not abort and len(case_reports.cases) > 0:
                        if (cases is None or case_name in cases) and \
                            (not cont or case_name not in passed):
                            case_name, result, duration = case_reports.cases[0]
                            reviewed_result, request = \
                                report_case(print,
                                            exp_dir,
                                            out_dir,
                                            case_name,
                                            result,
                                            duration,
                                            config)

                            if request == UserRequest.ABORT or \
                                    (fail_fast and reviewed_result != TestResult.OK):
                                abort = True

                            if reviewed_result != TestResult.OK:
                                exit_code = -1

                            reviews.append((case_name,
                                            reviewed_result,
                                            duration))

        # it's important to wait the jobs for
        # the coverage measurement to succeed
        p.close()
        p.join()

    finally:
        #
        # 3.2 merge outputs from test. do this
        #     even on failures to allow continuing
        #     testing from CTRL-C
        #
        merged = {}
        for batch_dir in batch_dirs:
            if os.path.isdir(batch_dir):
                for j in os.listdir(batch_dir):
                    if j.endswith(".txt"):
                        lines = merged.get(j, [])
                        lines.extend(
                            read_lines(batch_dir, j))
                        merged[j] = lines

        for name, lines in merged.items():
            write_lines(out_dir, name, lines)

    #
    # 4. do test reporting & review
    #
    end = time.time()
    took_ms = int((end-begin)*1000)

    updated_case_reports = CaseReports(reviews)
    updated_case_reports.to_file(report_txt)

    end_report(print,
               updated_case_reports.failed(),
               len(updated_case_reports.cases),
               took_ms)

    create_index(exp_dir, tests.all_names())

    return exit_code

def run_tests(exp_dir,
              out_dir,
              tests,
              cases: list,
              config: dict,
              cache):
    run = TestRun(
        exp_dir,
        out_dir,
        out_dir,
        tests,
        cases,
        config,
        cache)

    rv = test_result_to_exit_code(run.run())

    return rv

