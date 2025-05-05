import traceback
import multiprocessing
import os
import threading
import time
from collections import defaultdict
from copy import copy

from booktest.cache import LruCache
from booktest.config import DEFAULT_TIMEOUT
from booktest.detection import BookTestSetup
from booktest.review import create_index, report_case, start_report, \
    end_report, report_case_begin, report_case_result
from booktest.testrun import TestRun
from booktest.reports import CaseReports, Metrics, test_result_to_exit_code, read_lines, write_lines, UserRequest, \
    TestResult

#
# Parallelization and test execution support:
#


PROCESS_LOCAL_CACHE = LruCache(8)


def batch_dir(out_dir: str):
    return \
        os.path.join(
            out_dir,
            ".batches")


def prepare_batch_dir(out_dir: str):
    if len(out_dir) < len(".out"):
        raise ValueError(f"dangerous looking {out_dir}!")

    _batch_dir = batch_dir(out_dir)

    if os.path.exists(_batch_dir):
        os.system(f"rm -rf {_batch_dir}")
        os.makedirs(_batch_dir, exist_ok=True)


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
                 setup: BookTestSetup):
        self.exp_dir = exp_dir
        self.out_dir = out_dir
        self.tests = tests
        self.config = config
        self.setup = setup

    def __call__(self, case, preallocations={}):
        output = None
        try:
            allocations = set()  # everything should be handled by preallocations
            path = case.split("/")
            batch_name = ".".join(path)
            batch_dir = \
                os.path.join(
                    self.out_dir,
                    ".batches",
                    batch_name)

            os.makedirs(batch_dir, exist_ok=True)

            output_file = \
                os.path.join(
                    batch_dir,
                    "output.txt")

            output = open(output_file, "w")

            run = TestRun(
                self.exp_dir,
                self.out_dir,
                batch_dir,
                self.tests,
                [case],
                self.config,
                PROCESS_LOCAL_CACHE,
                output,
                allocations,
                preallocations)

            with self.setup.setup_teardown():
                rv = test_result_to_exit_code(run.run())

        except Exception as e:
            print(f"{case} failed with {e}")
            if output:
                output.write(f"{case} failed with {e}\n")
            traceback.print_exc()
            rv = test_result_to_exit_code(TestResult.FAIL)
        finally:
            if output:
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
                 setup,
                 reports: CaseReports):
        self.cases = cases
        process_count = config.get("parallel", True)
        if process_count is True or process_count == "True":
            process_count = os.cpu_count()
        else:
            process_count = int(process_count)

        self.process_count = process_count
        self.pool = None
        self.done = set()
        self.case_durations = {}
        for name, result, duration in reports.cases:
            self.case_durations[name] = duration

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
        self.run_batch = RunBatch(exp_dir, out_dir, tests, job_config, setup)
        self.timeout = int(config.get("timeout", DEFAULT_TIMEOUT))

        self.log_path = os.path.join(out_dir, "log.txt")

        dependencies = defaultdict(set)
        resources = defaultdict(set)
        todo = set()
        for name in cases:
            method = tests.get_case(name)
            for dependency in tests.method_dependencies(method, cases):
                dependencies[name].add(dependency)
            resources[name] = list(tests.method_resources(method))
            todo.add(name)

            batch_dir, batch_report_file = case_batch_dir_and_report_file(self.batches_dir, name)
            os.makedirs(batch_dir, exist_ok=True)

        # prioritize each task based on the heaviest chain of tasks depending on it
        priorities = defaultdict(lambda: 0)

        def assign_priority(name, dependent_duration):
            duration = self.case_durations.get(name, 1) # assume task to take 1s by default
            total_duration = duration + dependent_duration
            priorities[name] = max(priorities[name], total_duration)
            for dependent in dependencies[name]:
                assign_priority(dependent, total_duration)

        for name in todo:
            assign_priority(name, 0)

        self.priorities = priorities

        self._log = None
        self.todo = todo
        self.dependencies = dependencies
        self.resources = resources
        self.scheduled = {}
        self._abort = False
        self.thread = None
        self.lock = threading.Lock()

        self.reports = []
        self.left = len(todo)
        self.allocated_resources = set()

    def plan(self, todo, plan_target):
        rv = []
        allocated_resources = copy(self.allocated_resources)

        # run slowest jobs first
        todo = list(todo)
        todo.sort(key=lambda name: (-self.priorities[name], name))

        for name in todo:
            if len(rv) >= plan_target:
                break
            runnable = True
            for dependency in self.dependencies[name]:
                if dependency in self.todo and dependency not in self.done:
                    runnable = False

            allocated_resources2 = copy(allocated_resources)
            preallocations = {}

            for pos, resource in enumerate(self.resources[name]):
                resource_allocations_preallocations = resource.allocate((name, pos), allocated_resources2, preallocations)
                if resource_allocations_preallocations is not None:
                    _, new_allocations, new_preallocations = resource_allocations_preallocations
                    allocated_resources2 = new_allocations
                    preallocations = new_preallocations
                else:
                    runnable = False
                    break

            if runnable:
                rv.append((name, preallocations))
                allocated_resources = allocated_resources2

        return rv, allocated_resources

    def abort(self):
        with self.lock:
            self._abort = True

    def log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self._log.write(f"{timestamp}: {message}\n")
        self._log.flush()

    def thread_function(self):
        self.log(f"parallel run started for {len(self.todo)} prioritized tasks:")
        for name in sorted(list([(self.priorities[i], i) for i in self.todo]), key=lambda x: (-x[0], x[1])):
            self.log(f" - {name[0]} {name[1]}")

        scheduled = dict()

        while len(self.done) < len(self.todo) and not self._abort:
            plan_target = (self.process_count - len(scheduled))
            planned_tasks, planned_allocated_resources = self.plan(self.todo - self.done - scheduled.keys(), plan_target)

            #
            # 1. start async jobs
            #
            self.log(f"planned {len(planned_tasks)} / {len(self.todo) - len(self.done)} tasks")
            self.log(f"{len(self.allocated_resources)} resources reserved")

            for name, preallocations in planned_tasks:
                self.log(f"scheduling {name} with resources:")
                for allocation_id, resource_identity_allocation in preallocations.items():
                    self.log(f" - {allocation_id}={resource_identity_allocation[0]}:{resource_identity_allocation[1]}")

                scheduled[name] = (self.pool.apply_async(self.run_batch, args=[name, preallocations]), time.time(), preallocations)

            self.allocated_resources = planned_allocated_resources

            scheduled_example = ", ".join(list(scheduled)[:3] + ["..."] if len(scheduled) > 3 else list(scheduled))
            self.log(f"{len(scheduled)} / {len(self.todo) - len(self.done)} tasks are scheduled: {scheduled_example}")
            self.log(f"{len(self.allocated_resources)} resources reserved")

            if len(scheduled) == 0:
                self.log(f"no tasks to run, while only {len(self.done)}/{self.todo} done. todo: {', '.join(planned_tasks)}")
                break

            #
            # 2. collect done tasks
            #
            done_tasks = list()
            while len(done_tasks) == 0 and not self._abort:
                for name, task_begin_preallocation in scheduled.items():
                    task, begin, preallocation = task_begin_preallocation
                    if task in done_tasks:
                        pass # already added
                    elif task.ready():
                        done_tasks.append((name, preallocation))
                        self.log(f"{name} ready.")
                    elif time.time() - begin > self.timeout:
                        done_tasks.append((name, preallocation))
                        self.log(f"{name} timeouted after {time.time() - begin}.")
                if len(done_tasks) == 0:
                    time.sleep(0.001)

            #
            # 3. remove done tasks and collect their reports
            #
            self.done |= {i[0] for i in done_tasks}
            reports = []
            for name, preallocations in done_tasks:
                begin = scheduled[name][1]
                del scheduled[name]
                report_file = case_batch_dir_and_report_file(self.batches_dir, name)[1]
                i_case_report = None
                if os.path.exists(report_file):
                    i_report = CaseReports.of_file(report_file)
                    if len(i_report.cases) > 0:
                        i_case_report = i_report.cases[0]
                if i_case_report is None:
                    i_case_report = CaseReports.make_case(name, TestResult.FAIL, 1000*(time.time() - begin))
                reports.append(i_case_report)
                self.log(f"{name} reported as {i_case_report[1]} after {i_case_report[2]}.")
                self.log("freeing resources:")

                for pos, resource in enumerate(self.resources[name]):
                    allocation_id = (name, pos)
                    if allocation_id not in preallocations:
                        raise ValueError(f"missing {allocation_id} in {preallocations}")
                    resource_identity_allocation = preallocations[allocation_id]
                    self.log(f" - {allocation_id}={resource_identity_allocation[0]}:{resource_identity_allocation[1]}")
                    self.allocated_resources = resource.deallocate(self.allocated_resources, resource_identity_allocation[1])

            self.log(f"done {len(self.done)}/{len(self.todo)} tasks.")

            #
            # 4. make reports visible to the interactive thread vis shared list
            #
            with self.lock:
                self.log(f"reporting {len(reports)}.")
                self.left -= len(reports)
                self.reports.extend(reports)

        self.log("parallel run ended.")

    def batch_dirs(self):
        rv = []
        for i in self.cases:
            rv.append(case_batch_dir_and_report_file(self.batches_dir, i)[0])
        return rv

    def has_next(self):
        with self.lock:
            return (self.left > 0 or len(self.reports) > 0) and not self._abort

    def done_reports(self):
        with self.lock:
            return self.reports

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
        self._log = open(self.log_path, "w")

        self.pool = multiprocessing.get_context('spawn').Pool(self.process_count, initializer=coverage.process_startup)
        self.pool.__enter__()

        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # it's important to wait the jobs for
        # the coverage measurement to succeed
        self._abort = True
        self.thread.join()
        self.pool.close()

        # for some reason, this will get stuck on keyboard interruptions
        # yet, it is necessary for getting the coverage correctly
        self.pool.join()
        self._log.close()


def parallel_run_tests(exp_dir,
                       out_dir,
                       tests,
                       cases: list,
                       config: dict,
                       setup: BookTestSetup):
    begin = time.time()

    reports = CaseReports.of_dir(out_dir)

    done, todo = reports.cases_to_done_and_todo(cases, config)

    prepare_batch_dir(out_dir)

    runner = ParallelRunner(exp_dir,
                            out_dir,
                            tests,
                            todo,
                            config,
                            setup,
                            reports)

    fail_fast = config.get("fail_fast", False)

    start_report(print)

    exit_code = 0

    os.system(f"mkdir -p {out_dir}")
    report_file = os.path.join(out_dir, "cases.txt")

    with open(report_file, "w") as report_f:
        # add previously passed items to test
        for i in reports.cases:
            if i[0] not in todo:
                CaseReports.write_case(
                    report_f, i[0], i[1], i[2])

        reviewed = []

        def record_case(case_name, result, duration):
            CaseReports.write_case(
                report_f,
                case_name,
                result,
                duration)
            reviewed.append((case_name, result, duration))

        with runner:
            try:
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

                    record_case(
                        case_name,
                        reviewed_result,
                        duration)

            except KeyboardInterrupt as e:
                runner.abort()
                for i in runner.todo - runner.done:
                    print(f"  {i}..interrupted")

            finally:
                #
                # 3.2 merge outputs from test. do this
                #     even on failures to allow continuing
                #     testing from CTRL-C
                #

                # add already processed, but not interacted reports
                for case_name, result, duration in runner.done_reports():
                    report_case_begin(print,
                                      case_name,
                                      None,
                                      False)
                    report_case_result(print,
                                       case_name,
                                       result,
                                       duration,
                                       False)
                    record_case(
                        case_name,
                        result,
                        duration)

                merged = {}
                for batch_dir in runner.batch_dirs():
                    if os.path.isdir(batch_dir):
                        for j in os.listdir(batch_dir):
                            if j.endswith(".txt"):
                                lines = merged.get(j, [])
                                lines.extend(
                                    read_lines(batch_dir, j))
                                merged[j] = lines

                for name, lines in merged.items():
                    if name != "cases.txt":
                        write_lines(out_dir, name, lines)

                #
                # 4. do test reporting & review
                #
                end = time.time()
                took_ms = int((end-begin)*1000)
                Metrics(took_ms).to_dir(out_dir)

                updated_case_reports = CaseReports(reviewed)

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
              cache,
              setup: BookTestSetup):

    run = TestRun(
        exp_dir,
        out_dir,
        out_dir,
        tests,
        cases,
        config,
        cache)

    with setup.setup_teardown():
        rv = test_result_to_exit_code(run.run())

    return rv

async def run_tests_async(exp_dir,
                          out_dir,
                          tests,
                          cases: list,
                          config: dict,
                          cache,
                          setup: BookTestSetup):

    run = TestRun(
        exp_dir,
        out_dir,
        out_dir,
        tests,
        cases,
        config,
        cache)

    with setup.setup_teardown():
        rv = await test_result_to_exit_code(run.run())

    return rv

