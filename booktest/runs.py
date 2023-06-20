import os
import time

from booktest.review import review, create_index
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

    def __call__(self, cases):

        path = cases[0].split("/")
        path = path[:len(path)-1]
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
                cases,
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
    """
    Runs test in parallel processes
    """
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

    f = RunBatch(exp_dir, out_dir, tests, job_config, cache)

    # 2.2 split test cases into batches
    batches = []
    batch = []
    batch_paths = []
    prev_path = None
    for i in cases:
        parts = i.split("/")
        path = parts[:len(parts)-1]
        if prev_path is None or path == prev_path:
            batch.append(i)
        else:
            batch_paths.append(prev_path)
            batches.append(batch)
            batch = [i]
        prev_path = path

    if prev_path is not None:
        batches.append(batch)
        batch_paths.append(prev_path)

    reports = case_reports.cases
    batch_dirs = []

    # 2.3 split the case reports for each parallel job
    for i in range(len(batches)):
        path = ".".join(batch_paths[i])
        batch = batches[i]

        batch_reports = [i for i in reports if i[0] in batch]

        batch_dir = os.path.join(batches_dir, path)
        batch_dirs.append(batch_dir)
        os.makedirs(batch_dir, exist_ok=True)

        batch_report_file = os.path.join(batch_dir, "cases.txt")
        CaseReports(batch_reports)\
            .to_file(batch_report_file)

    #
    # 3. run test in a process pool
    #

    # 3.1 Run test in parallel processes
    #     initialize each process with coverage.process_startup
    #     method
    import coverage
    try:
        with Pool(min(os.cpu_count(), len(batches)),
                  initializer=coverage.process_startup) as p:
            exit_codes = list(p.map(f, batches))
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
    exit_code = 0
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

