import asyncio
import os
import threading
import time
from collections import defaultdict
from multiprocessing import Pool

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


class ParallelRunner:

    def __init__(self,
                 exp_dir,
                 out_dir,
                 tests,
                 cases: list,
                 config: dict,
                 cache):
        self.cases = cases
        self.pool = None
        self.done = set()

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
        job_config["continue"] = False
        job_config["interactive"] = False
        job_config["always_interactive"] = False

        self.batches_dir = batches_dir
        self.run_batch = RunBatch(exp_dir, out_dir, tests, job_config, cache)

        dependencies = defaultdict(set)
        todo = set()
        for name in cases:
            method = tests.get_case(name)
            for dependency in tests.method_dependencies(method, cases):
                dependencies[name].add(dependency)
            todo.add(name)

            batch_dir, batch_report_file = case_batch_dir_and_report_file(self.batches_dir, name)
            os.makedirs(batch_dir, exist_ok=True)

        self.todo = todo
        self.dependencies = dependencies
        self.scheduled = {}
        self.abort = False
        self.thread = None
        self.lock = threading.Lock()

        self.reports = []
        self.left = len(todo)

    def runnable_cases(self):
        rv = []
        for name in self.todo:
            ready = True
            for dependency in self.dependencies[name]:
                if dependency not in self.done:
                    ready = False
            if ready:
                rv.append(name)
        return rv

    def abort(self):
        with self.lock:
            self.abort = True

    def thread_function(self):
        scheduled = dict()

        while len(self.done) < len(self.todo) and not self.abort:
            ready = self.runnable_cases()

            # start async jobs
            for name in ready:
                if name not in self.done and name not in scheduled:
                    scheduled[name] = self.pool.apply_async(self.run_batch, args=[name])

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

            self.done |= done_tasks
            reports = []
            for i in done_tasks:
                del scheduled[i]
                report_file = case_batch_dir_and_report_file(self.batches_dir, i)[1]
                reports.append(CaseReports.of_file(report_file).cases[0])

            with self.lock:
                self.left -= len(reports)
                self.reports.extend(reports)

    def has_next(self):
        with self.lock:
            return (self.left > 0 or len(self.reports) > 0) and not self.abort

    def next_report(self):
        while True:
            with self.lock:
                if len(self.reports) > 0:
                    rv = self.reports[0]
                    self.reports = self.reports[1:]
                    return rv
            # todo, use semaphore instead of polling
            time.sleep(0.01)

    def __enter__(self):
        import coverage
        self.finished = False
        self.pool = Pool(os.cpu_count(), initializer=coverage.process_startup)
        self.pool.__enter__()

        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # it's important to wait the jobs for
        # the coverage measurement to succeed
        self.abort = True
        self.thread.join()

        self.pool.close()
        self.pool.join()



def parallel_run_tests(exp_dir,
                       out_dir,
                       tests,
                       cases: list,
                       config: dict,
                       cache):
    begin = time.time()

    report_file = os.path.join(out_dir, "cases.txt")
    reviews, todo = CaseReports.of_file(report_file).cases_to_done_and_todo(cases, config)

    runner = ParallelRunner(exp_dir,
                            out_dir,
                            tests,
                            todo,
                            config,
                            cache)

    fail_fast = config.get("fail_fast", False)

    start_report(print)

    exit_code = 0

    batch_dirs = []

    try:
        with runner:
            while runner.has_next():
                case_name, result, duration = runner.next_report()

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
                    runner.abort()

                if reviewed_result != TestResult.OK:
                    exit_code = -1

                reviews.append((case_name,
                                reviewed_result,
                                duration))
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
    updated_case_reports.to_file(report_file)

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

