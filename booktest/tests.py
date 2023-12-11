import os.path as path
import os
import argparse

from coverage import Coverage

from booktest.cache import LruCache
from booktest.review import run_tool, review
from booktest.runs import parallel_run_tests, run_tests
from booktest.config import get_default_config
import booktest.setup


class Tests:
    def __init__(self, cases):
        self.cases = cases

    def is_selected(self, test_name, selection):
        """
        checks whether the test name is selected
        based on the selection
        """
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

    def test_result_path(self, out_dir, case_path):
        return path.join(out_dir, case_path + ".bin")

    def test_result_exists(self, out_dir, case_path):
        return path.exists(self.test_result_path(out_dir, case_path))

    def get_case(self, case_name):
        for s in self.cases:
            if s[0] == case_name:
                return s[1]
        return None

    def case_by_method(self, method):
        for t in self.cases:
            # a bit hacky way for figuring out the dependencies
            if t[1] == method \
               or (hasattr(t[1], "__func__") and t[1].__func__ == method):
                return t[0]
        return None

    def method_dependencies(self,
                            method,
                            selection,
                            cache_out_dir=None):
        rv = []
        if hasattr(method, "_dependencies"):
            for dependency in method._dependencies:
                case = self.case_by_method(dependency)
                if case is not None:
                    if self.is_selected(case, selection) or \
                       cache_out_dir is None or \
                       not self.test_result_exists(cache_out_dir, case):
                        rv.append(case)

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
            if self.is_selected(c[0], selection):
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
            "-p",
            action='store_true',
            help="run test on parallel processes"
        )
        parser.add_argument(
            "--cov",
            action='store_true',
            help="store coverage information"
        )
        parser.add_argument(
            "-md-viewer",
            help="set the used mark down viewer"
        )
        parser.add_argument(
            "-diff-tool",
            help="set the used diff tool"
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

        test_choices = ["*"]
        for name in self.all_names():
            parts = name.split('/')
            prefix = ""
            for p in parts:
                if len(prefix) > 0:
                    prefix += "/"
                prefix += p
                if prefix not in test_choices:
                    test_choices.append(prefix)
                    test_choices.append("skip:" + prefix)

        parser.add_argument('test_cases',
                            nargs='*',
                            default='*',
                            choices=test_choices)

    def exec_parsed(self,
                    root_dir,
                    parsed,
                    cache=None,
                    extra_default_config: dict = {}) -> int:
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
        if parsed.p:
            config["parallel"] = True
        if parsed.cov:
            config["coverage"] = True
        if parsed.md_viewer:
            config["md_viewer"] = parsed.md_viewer
        if parsed.diff_tool:
            config["diff_tool"] = parsed.diff_tool

        def is_garbage(not_garbage, file):
            for ng in not_garbage:
                if ng == file:
                    return False
                if ng.endswith("/") and file.startswith(ng):
                    return False
            return True

        def garbage():
            rv = []
            names = set()
            for name in self.all_names():
                names.add(path.join(exp_dir, name + ".md"))
                names.add(path.join(exp_dir, name + "/"))
            names.add(path.join(exp_dir, "index.md"))
            for root, dirs, files in os.walk(root_dir):
                for f in files:
                    p = path.join(root, f)
                    if is_garbage(names, p):
                        rv.append(p)
            return rv

        if config.get("refresh_sources", False):
            cache_out_dir = None
        else:
            cache_out_dir = out_dir

        test_cases = parsed.test_cases

        if test_cases == "*":
            test_cases = config.get("default_tests", "test,book").split(",")

        cases = self.selected_names(test_cases, cache_out_dir)

        cmd = parsed.cmd

        if cmd == '--setup':
            return booktest.setup.setup_booktest()
        elif cmd == '--config':
            for key, value in config.items():
                print(f"{key}={value}")
            return 0
        elif cmd == '--garbage':
            for p in garbage():
                print(f"{p}")
            return 0
        elif cmd == '--print':
            for name in cases:
                file = path.join(exp_dir, f"{name}.md")
                if path.exists(file):
                    os.system(f"cat {file}")
            return 0
        elif cmd == '--path':
            for name in cases:
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
            for s in cases:
                print(f"  {s}")
            return 0
        elif cmd == '--review':
            return review(exp_dir,
                          out_dir,
                          config,
                          None,
                          cases)
        else:
            def run():
                parallel = config.get("parallel", False)
                if parallel:
                    return parallel_run_tests(exp_dir,
                                              out_dir,
                                              self,
                                              cases,
                                              config,
                                              cache)
                else:
                    return run_tests(exp_dir,
                                     out_dir,
                                     self,
                                     cases,
                                     config,
                                     cache)

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

                return rv
            else:
                return run()

    def exec(self, root_dir, args, cache=None) -> int:
        """
        :param root_dir: the directory containing books and .out directory
        :param args: a string containing command line arguments
        :param cache: in-memory cache. Can be e.g. dictionary {},
                      LruCache or NoCache.
        :return: returns an exit value. 0 for success, 1 for error
        """
        parser = argparse.ArgumentParser(
            description='run book test operations')
        self.setup_parser(parser)

        parsed = parser.parse_args(args)

        return self.exec_parsed(root_dir, parsed, cache)

