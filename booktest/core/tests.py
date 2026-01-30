import os.path as path
import os
import argparse

from coverage import Coverage

from booktest.dependencies.cache import LruCache
from booktest.dependencies.dependencies import bind_dependent_method_if_unbound
from booktest.config.detection import BookTestSetup
from booktest.reporting.reports import CaseReports
from booktest.reporting.review import run_tool, review
from booktest.core.runs import parallel_run_tests, run_tests
from booktest.config.config import get_default_config
import booktest.utils.setup
from booktest.core.testrun import method_identity, match_method

from booktest.config.selection import is_selected
from booktest.config.naming import to_filesystem_path


class Tests:
    def __init__(self, cases):
        self.cases = cases

    def test_result_path(self, out_dir, case_path):
        # Convert pytest-style names to filesystem paths (:: → /)
        case_path_fs = to_filesystem_path(case_path)
        return path.join(out_dir, case_path_fs + ".bin")

    def test_result_exists(self, out_dir, case_path):
        return path.exists(self.test_result_path(out_dir, case_path))

    def get_case(self, case_name):
        for s in self.cases:
            if s[0] == case_name:
                return s[1]
        return None

    def case_by_method(self, method):
        for t in self.cases:
            if match_method(method, t[1]):
                return t[0]
        return None

    def method_dependencies(self,
                            method,
                            selection,
                            cache_out_dir=None):
        rv = []
        if hasattr(method, "_dependencies"):
            for dependency in method._dependencies:
                bound_method = bind_dependent_method_if_unbound(method, dependency)
                case = self.case_by_method(bound_method)
                if case is not None:
                    if is_selected(case, selection) or \
                       cache_out_dir is None or \
                       not self.test_result_exists(cache_out_dir, case):
                        rv.append(case)

        return rv

    def method_resources(self,
                         method):
        rv = []
        if hasattr(method, "_resources"):
            rv.extend(method._resources)

        return rv

    def all_method_dependencies(self,
                                method,
                                selection,
                                cache_out_dir=None):
        rv = []
        for dependency in self.method_dependencies(method, selection, cache_out_dir):
            m = self.get_case(dependency)
            rv.extend(self.all_method_dependencies(m, selection, cache_out_dir))
            rv.append(dependency)

        return rv

    def all_names(self):
        return list(map(lambda x: x[0], self.cases))

    def selected_names(self, selection, cache_out_dir=None):
        selected = []
        for c in self.cases:
            if is_selected(c[0], selection):
                dependencies = \
                    self.all_method_dependencies(c[1],
                                                 selection,
                                                 cache_out_dir)
                for dependency in dependencies:
                    if dependency not in selected:
                        selected.append(dependency)
                if c[0] not in selected:
                    selected.append(c[0])
        return selected

    def _print_failure_report_if_needed(self, exit_code, exp_dir, out_dir, config, cases):
        """
        Automatically print failure report when tests fail.
        Replaces the need for 'booktest -v -L -w -c' fallback.
        """
        # Don't print report if:
        # - All tests passed (exit code 0)
        # - Already in interactive mode (user is actively reviewing)
        # - User disabled auto-report
        if exit_code == 0:
            return

        if config.get("interactive", False):
            return

        if not config.get("auto_report", True):
            return

        # Print the report (equivalent to -v -L -w -c logic)
        print()
        print("━" * 70)
        print("FAILURE REPORT")
        print("━" * 70)
        print()

        # Call the review function with non-interactive flag and continue mode
        # This ensures only failed/diffed tests are shown, not all tests
        review_config = config.copy()
        review_config["verbose"] = True
        review_config["print_logs"] = True
        review_config["interactive"] = False
        review_config["continue"] = True  # Only show failed/diffed tests

        review(exp_dir, out_dir, review_config, None, cases)

        # Show helpful tips at the end
        print()
        print("💡 To review (-w) failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -w -c -v -i")
        print("💡 To rerun failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -c -v -i")
        print("💡 To update failed tests's (-c) missing snapshots (-s), run: booktest -c -s")
        print()

    def setup_parser(self, parser):
        parser.add_argument(
            "-i",
            action='store_true',
            help="interactive mode"
        )
        parser.add_argument(
            "-I",
            action='store_true',
            help="always interactive, even on success"
        )
        parser.add_argument(
            "-v",
            action='store_true',
            help="verbose"
        )
        parser.add_argument(
            "-L",
            action='store_true',
            help="prints logs"
        )
        parser.add_argument(
            "-f",
            action='store_true',
            help="fails fast"
        )
        parser.add_argument(
            "-c",
            action='store_true',
            help="continue, skip succesful test"
        )
        parser.add_argument(
            "-r",
            action='store_true',
            help="refresh test dependencies"
        )
        parser.add_argument(
            "-u",
            action='store_true',
            help="update test on success"
        )
        parser.add_argument(
            "-a",
            action='store_true',
            help="automatically accept differing tests"
        )
        parser.add_argument(
            "-R",
            action='store_true',
            help="use AI to review test differences (requires LLM configuration)"
        )
        parser.add_argument(
            "-p",
            action='store_true',
            help="run test on N parallel processes, where is N relative to CPU count"
        )
        parser.add_argument(
            "-p1",
            dest='p',
            action='store_const',
            const=1,
            help="run test on 1 parallel processes"
        )
        parser.add_argument(
            "-p2",
            dest='p',
            action='store_const',
            const=2,
            help="run test on 2 parallel processes"
        )
        parser.add_argument(
            "-p3",
            dest='p',
            action='store_const',
            const=3,
            help="run test on 3 parallel processes"
        )
        parser.add_argument(
            "-p4",
            dest='p',
            action='store_const',
            const=4,
            help="run test on 4 parallel processes"
        )
        parser.add_argument(
            "-p6",
            dest='p',
            action='store_const',
            const=6,
            help="run test on 6 parallel processes"
        )
        parser.add_argument(
            "-p8",
            dest='p',
            action='store_const',
            const=8,
            help="run test on 8 parallel processes"
        )
        parser.add_argument(
            "-p16",
            dest='p',
            action='store_const',
            const='16',
            help="run test on 16 parallel processes"
        )
        parser.add_argument(
            "--parallel-count",
            dest='p',
            type=int,
            help="run test on N parallel processes"
        )
        parser.add_argument(
            "-s",
            action='store_true',
            help="complete snapshots. this captures snapshots that are missing"
        )
        parser.add_argument(
            "-S",
            action='store_true',
            help="refresh snapshots and discard old snapshots"
        )
        parser.add_argument(
            "--cov",
            action='store_true',
            help="store coverage information"
        )
        parser.add_argument(
            "--md-viewer",
            help="set the used mark down viewer"
        )
        parser.add_argument(
            "--diff-tool",
            help="set the used diff tool"
        )
        parser.add_argument(
            '--context',
            type=str,
            help="context, where the tests are detected and run. default is local directory.")
        parser.add_argument(
            '--python-path',
            type=str,
            help="python path for detecting source files. values should separated by ':'. default is 'src:.'")
        parser.add_argument(
            '--resource-snapshots',
            dest="resource_snapshots",
            action='store_true',
            help="use this flag, if snapshot files are stored as packaged resources (e.g. in PEX file)")
        parser.add_argument(
            "--timeout",
            dest='timeout',
            type=int,
            help="fail tests on a timeout. works only with parallel runs"
        )
        parser.add_argument(
            "--narrow-detection",
            dest='narrow_detection',
            action='store_true',
            help="only detect tests within the related files / modules. E.g. hello-selection opens only hello_book.py."
        )

        parser.add_argument(
            '-l',
            action='store_const',
            dest='cmd',
            const="-l",
            help="lists the selected test cases")
        parser.add_argument(
            "--setup",
            action='store_const',
            dest='cmd',
            const="--setup",
            help="setups booktest"
        )
        parser.add_argument(
            '--garbage',
            action='store_const',
            dest='cmd',
            const="--garbage",
            help="prints the garbage files")

        parser.add_argument(
            '--clean',
            action='store_const',
            dest='cmd',
            const="--clean",
            help="cleans the garbage files")

        parser.add_argument(
            '--config',
            action='store_const',
            dest='cmd',
            const="--config",
            help="Prints the configuration")

        parser.add_argument(
            '--print',
            action='store_const',
            dest='cmd',
            const="--print",
            help="Prints the selected test cases expected output")

        parser.add_argument(
            '--view',
            action='store_const',
            dest='cmd',
            const="--view",
            help="Opens the selected test cases in markdown viewere")

        parser.add_argument(
            '--path',
            action='store_const',
            dest='cmd',
            const="--path",
            help="Prints the selected test cases expected output paths")

        parser.add_argument(
            '--review',
            action='store_const',
            dest='cmd',
            const="--review",
            help="Prints interactive report of previous run for review.")
        parser.add_argument(
            '-w',
            action='store_const',
            dest='cmd',
            const="--review",
            help="Short hand for --review.")
        parser.add_argument(
            '--forget',
            action='store_const',
            dest='cmd',
            const="--forget",
            help="Removes reviews from test cases. This stages them for rerun even with -c flag.")

        test_choices = ["*"]
        from booktest.config.naming import normalize_test_name

        for name in self.all_names():
            # Add the full pytest-style name
            if name not in test_choices:
                test_choices.append(name)
                test_choices.append("skip:" + name)

            # Normalize to filesystem format for prefix extraction
            name_fs = normalize_test_name(name)
            parts = name_fs.split('/')

            # Build all prefixes from filesystem path
            prefix_fs = ""
            for p in parts:
                if len(prefix_fs) > 0:
                    prefix_fs += "/"
                prefix_fs += p
                if prefix_fs not in test_choices:
                    test_choices.append(prefix_fs)
                    test_choices.append("skip:" + prefix_fs)

            # Also extract pytest-style prefixes (file path and class path)
            # For test/foo_test.py::ClassName/test_method:
            # - Add test/foo_test.py
            # - Add test/foo_test.py::ClassName
            if "::" in name:
                parts_pytest = name.split("::")
                if len(parts_pytest) >= 2:
                    # File path (test/foo_test.py)
                    file_path = parts_pytest[0]
                    if file_path not in test_choices:
                        test_choices.append(file_path)
                        test_choices.append("skip:" + file_path)

                    # Class path (test/foo_test.py::ClassName)
                    # Handle both :: and / separators in test part
                    test_part = parts_pytest[1]
                    if "/" in test_part:
                        # Has class, extract just class name
                        class_name = test_part.split("/")[0]
                        class_path = f"{file_path}::{class_name}"
                        if class_path not in test_choices:
                            test_choices.append(class_path)
                            test_choices.append("skip:" + class_path)

        parser.add_argument('test_cases',
                            nargs='*',
                            default='*',
                            choices=test_choices)

    def exec_parsed(self,
                    root_dir,
                    parsed,
                    cache=None,
                    extra_default_config: dict = {},
                    setup = None) -> int:
        """
        :param root_dir:  the directory containing books and .out directory
        :param parsed: the object containing argparse parsed arguments
        :param cache: in-memory cache. Can be e.g. dictionary {},
                      LruCache or NoCache.
        :return: returns an exit value. 0 for success, 1 for error
        """

        out_dir = os.path.join(root_dir, ".out")
        exp_dir = root_dir

        if cache is None:
            cache = LruCache(8)

        if setup is None:
            setup = BookTestSetup()

        config = get_default_config()
        # extra default configuration parameters get layered
        # on top of normal default configuration
        for key, value in extra_default_config.items():
            config[key] = value

        if parsed.i:
            config["interactive"] = True
        if parsed.I:
            config["always_interactive"] = True
        if parsed.v:
            config["verbose"] = True
        if parsed.L:
            config["print_logs"] = True
        if parsed.f:
            config["fail_fast"] = True
        if parsed.c:
            config["continue"] = True
        if parsed.r:
            config["refresh_sources"] = True
        if parsed.u:
            config["update"] = True
        if parsed.a:
            config["accept"] = True
        if parsed.R:
            config["ai_review"] = True
        if parsed.p:
            config["parallel"] = parsed.p
        if parsed.s:
            config["complete_snapshots"] = True
        if parsed.S:
            config["refresh_snapshots"] = True
        if parsed.cov:
            config["coverage"] = True
        if parsed.resource_snapshots:
            config["resource_snapshots"] = True
        if parsed.timeout:
            config["timeout"] = parsed.timeout
            if config.get("parallel") is None:
                raise ValueError("timeout requires parallel run")
        if parsed.md_viewer:
            config["md_viewer"] = parsed.md_viewer
        if parsed.diff_tool:
            config["diff_tool"] = parsed.diff_tool
        if parsed.context:
            config["context"] = parsed.context
        if parsed.diff_tool:
            config["python_path"] = parsed.python_path

        def is_garbage(not_garbage, file):
            for ng in not_garbage:
                if ng == file:
                    return False
                # Protect subdirectories
                if ng.endswith("/") and file.startswith(ng):
                    return False
                # Protect files with same basename (test_name.txt, test_name.log, etc.)
                if ng.endswith(".") and file.startswith(ng):
                    return False
            return True

        def garbage():
            rv = []
            names = set()
            for name in self.all_names():
                # Convert pytest-style name (::) to filesystem path (/)
                filesystem_name = name.replace("::", "/")
                # Only check files in books/ directory (exp_dir)
                # .out/ directory is excluded from garbage collection entirely
                names.add(path.join(exp_dir, filesystem_name + ".md"))
                names.add(path.join(exp_dir, filesystem_name + "/"))
                # Also protect files with same basename (e.g., .txt, .log files)
                names.add(path.join(exp_dir, filesystem_name + "."))
            names.add(path.join(exp_dir, "index.md"))
            # Walk only exp_dir (books/), exclude .out/ directory
            for root, dirs, files in os.walk(exp_dir):
                # Skip .out directory if it exists under exp_dir
                if '.out' in dirs:
                    dirs.remove('.out')
                for f in files:
                    p = path.join(root, f)
                    if is_garbage(names, p):
                        rv.append(p)
            return rv

        if config.get("refresh_sources", False):
            cache_out_dir = None
        else:
            cache_out_dir = out_dir

        selection = parsed.test_cases

        if selection == "*":
            selection = config.get("default_tests", "test,book").split(",")

        cases = self.selected_names(selection, cache_out_dir)

        reports = CaseReports.of_dir(out_dir)
        done, todo = reports.cases_to_done_and_todo(cases, config)

        cmd = parsed.cmd

        if cmd == '--setup':
            from booktest.utils.setup import setup_booktest
            return setup_booktest()
        elif cmd == '--config':
            for key, value in config.items():
                print(f"{key}={value}")
            return 0
        elif cmd == '--garbage':
            for p in garbage():
                print(f"{p}")
            return 0
        elif cmd == '--print':
            for name in todo:
                file = path.join(exp_dir, f"{name}.md")
                if path.exists(file):
                    os.system(f"cat {file}")
            return 0
        elif cmd == '--path':
            for name in todo:
                file = path.join(exp_dir, f"{name}.md")
                print(file)
            return 0
        elif cmd == '--view':
            files = []
            for name in cases:
                file = path.join(exp_dir, f"{name}.md")
                if path.exists(file):
                    files.append(file)
            if len(files) > 0:
                return run_tool(config, "md_viewer", " ".join(files))
            else:
                return 0
        elif cmd == '--clean':
            for p in garbage():
                os.remove(p)
                print(f"removed {p}")
            return 0
        elif cmd == '-l':
            from booktest.reporting.colors import green, yellow, red, gray
            from booktest.reporting.reports import TestResult

            def format_duration(duration_ms):
                """Format duration in human-readable form."""
                if duration_ms >= 60000:
                    return f"{duration_ms / 60000:.1f} min"
                elif duration_ms >= 1000:
                    return f"{duration_ms / 1000:.1f} s"
                else:
                    return f"{int(duration_ms)} ms"

            # Build a lookup from test name to (result, duration_ms)
            result_lookup = {}
            for case_name, result, duration_ms in reports.cases:
                result_lookup[case_name] = (result, duration_ms)

            # Count stats
            ok_count = diff_count = fail_count = todo_count = 0

            for s in todo:
                if s in result_lookup:
                    result, duration_ms = result_lookup[s]
                    duration_str = format_duration(duration_ms)
                    if result == TestResult.OK:
                        status = green("ok") + f" {duration_str}"
                        ok_count += 1
                    elif result == TestResult.DIFF:
                        status = yellow("DIFF") + f" {duration_str}"
                        diff_count += 1
                    else:  # FAIL
                        status = red("FAIL") + f" {duration_str}"
                        fail_count += 1
                    print(f"  {s} - {status}")
                else:
                    # Not run yet
                    print(f"  {s}")
                    todo_count += 1

            return 0
        elif cmd == '--review':
            return review(exp_dir,
                          out_dir,
                          config,
                          None,
                          cases)
        elif cmd == '--forget':
            reports = CaseReports.of_dir(out_dir).cases
            reports = [i for i in reports if i[0] not in cases]
            CaseReports(reports).to_dir(out_dir)
        else:
            def run():
                parallel = config.get("parallel", False)
                if parallel:
                    return parallel_run_tests(exp_dir,
                                              out_dir,
                                              self,
                                              cases,
                                              config,
                                              setup)
                else:
                    return run_tests(exp_dir,
                                     out_dir,
                                     self,
                                     cases,
                                     config,
                                     cache,
                                     setup)

            coverage = config.get("coverage", False)

            if coverage:
                # remove old main coverage and process coverage files
                if os.path.exists(".coverage"):
                    os.remove(".coverage")
                for i in os.listdir("."):
                    if i.startswith(".coverage."):
                        os.remove(i)

                cov = Coverage()
                cov.start()

                try:
                    rv = run()
                finally:
                    cov.stop()
                    cov.save()
                    cov.combine()

                    cov.xml_report(outfile="coverage.xml")

                cov.report()

                # Print failure report if needed
                self._print_failure_report_if_needed(rv, exp_dir, out_dir, config, cases)

                return rv
            else:
                rv = run()

                # Print failure report if needed
                self._print_failure_report_if_needed(rv, exp_dir, out_dir, config, cases)

                return rv

    def exec(self,
             root_dir,
             args,
             cache=None,
             extra_default_config: dict = {},
             setup = None) -> int:
        """
        :param root_dir: the directory containing books and .out directory
        :param args: a string containing command line arguments
        :param cache: in-memory cache. Can be e.g. dictionary {},
                      LruCache or NoCache.
        :return: returns an exit value. 0 for success, 1 for error
        """
        # Custom formatter to add workflow examples
        class WorkflowHelpFormatter(argparse.RawDescriptionHelpFormatter):
            def format_help(self):
                help_text = super().format_help()
                # Insert workflow examples after description
                workflow_examples = """
Common workflows:
  booktest                       Run tests (auto-report shows failures)
  booktest -v                    Run with verbose output
  booktest -v -i                 Interactive development (pause on failures)
  booktest -w                    Review failures from previous run
  booktest -p8                   Parallel testing (recommended for CI)
  booktest -u -c                 Auto-accept changes, continue on failure

"""
                # Insert after the description line
                parts = help_text.split('\n\n', 1)
                if len(parts) == 2:
                    return parts[0] + '\n\n' + workflow_examples + parts[1]
                return help_text

        parser = argparse.ArgumentParser(
            description='booktest - review-driven testing for data science',
            formatter_class=WorkflowHelpFormatter)
        self.setup_parser(parser)

        parsed = parser.parse_args(args)

        return self.exec_parsed(root_dir, parsed, cache, extra_default_config, setup)
