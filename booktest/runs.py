import asyncio
import os
import time
from collections import defaultdict

from booktest.review import review, create_index, report_case_result, report_case, report_case_begin
from booktest.testrun import TestRun
from booktest.reports import CaseReports, Metrics, test_result_to_exit_code, read_lines, write_lines


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

    print()
    print("# parallel run:")
    print()

    exit_code = 0
    exit_codes = []

    batch_dirs = []

    import coverage
    try:
        with Pool(os.cpu_count(),
                  initializer=coverage.process_startup) as p:

            scheduled = dict()

            while len(done) < len(todo):
                ready = ready_cases()

                # start async jobs
                for name in ready:
                    if name not in done and name not in scheduled:
                        path = ".".join(name.split("/"))

                        batch_reports = list([i for i in reports if i[0] == name])[:1]

                        batch_dir = os.path.join(batches_dir, path)
                        batch_dirs.append(batch_dir)
                        os.makedirs(batch_dir, exist_ok=True)

                        batch_report_file = os.path.join(batch_dir, "cases.txt")
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
                            exit_codes.append(task.get())
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
                case_reports = CaseReports.of_file(report_txt)

                for (case_name, result, duration) in case_reports.cases:
                    if case_name in done_tasks:
                        report_case_begin(print, case_name, None, False)
                        report_case_result(print,
                                           case_name,
                                           result,
                                           duration,
                                           False)

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

    # 3.3 resolve the test result as unix exit code
    for i in exit_codes:
        exit_code = i
        if exit_code != 0:
            break

    #
    # 4. do test reporting & review
    #

    end = time.time()
    took_ms = int((end-begin)*1000)

    Metrics(took_ms).to_file(
        os.path.join(
            out_dir, "metrics.json"))

    review(exp_dir,
           out_dir,
           config,
           case_reports.passed(),
           cases)

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

