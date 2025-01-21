import os
import sys

import booktest as bt

import subprocess

import re


EXEC_PATH = None


# create resources for each test to avoid race conditions, when running
# multiple tests on a single project

PREDICTOR_CONTEXT = bt.Resource("examples/predictor")
CONFIGURATIONS_CONTEXT = bt.Resource("examples/configurations")
PYTEST_CONTEXT = bt.Resource("examples/pytest")
TIMEOUT_CONTEXT = bt.Resource("examples/timeout")



def booktest_exec_path():
    if EXEC_PATH is None:
        EXEC_PAT = subprocess.check_output(["which", "booktest"]).decode("utf-8").strip()
    return EXEC_PAT


class BooktestProcess:

    def __init__(self, args, context, out_file = None, err_file = None):
        self.args = args
        if context is None:
            context = os.getcwd()

        self.context = context
        self.out_file = out_file
        self.err_file = err_file


    def __enter__(self):
        if self.out_file is None:
            self.out = sys.stdout
        else:
            self.out = open(self.out_file, "w")

        if self.err_file is None:
            self.err = sys.stderr
        else:
            self.err = open(self.err_file, "w")

        self.process = subprocess.Popen([booktest_exec_path()] + self.args,
                                        cwd=self.context,
                                        env={},
                                        stdout=self.out,
                                        stderr=self.err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.wait()
        self.out.close()
        self.err.close()


def t_cli(t: bt.TestCaseRun, args, context):
    out_file = t.tmp_file("out.txt")
    err_file = t.tmp_file("err.txt")
    if context is None:
        # let's use our example project by default
        context = "examples/predictor"

    t.h1("command:")

    t.tln(f"booktest {' '.join(args)}")

    t.h1("configuration:")

    t.keyvalueln(" * context:", context)

    with BooktestProcess(args, context, out_file, err_file) as p:
        pass

    t.h1("output:")
    number = re.compile(r"\d+ ms")

    def replace_ms(text):
        return re.sub(number, "<number> ms", text)

    with open(out_file) as f:
        t.tln(replace_ms(f.read()))

    with open(err_file) as f:
        err = replace_ms(f.read())

    if err:
        t.h1("error:")
        t.tln(err)


@bt.depends_on(PREDICTOR_CONTEXT)
def test_help(t: bt.TestCaseRun, context: str):
    t_cli(t, ["-h"], context)


@bt.depends_on(PREDICTOR_CONTEXT)
def test_list(t: bt.TestCaseRun, context: str):
    t_cli(t, ["-l"], context)


@bt.depends_on(PREDICTOR_CONTEXT)
def test_run(t: bt.TestCaseRun, context: str):
    t_cli(t, [], context)


@bt.depends_on(PREDICTOR_CONTEXT)
def test_parallel(t: bt.TestCaseRun, context: str):
    t_cli(t, ["-p"], context)


@bt.depends_on(TIMEOUT_CONTEXT)
def test_timeout(t: bt.TestCaseRun, context: str):
    t.h1("description:")
    t.tln("this test verifies that the slow test will fail with 1s timeout")
    t_cli(t, ["-p", "--timeout", "2"], context)


@bt.depends_on(PREDICTOR_CONTEXT)
def test_context(t: bt.TestCaseRun, context: str):
    t_cli(t, ["--context", context], ".")


@bt.depends_on(CONFIGURATIONS_CONTEXT)
def test_configurations(t: bt.TestCaseRun, context: str):
    t_cli(t, ["-v"], context)


@bt.depends_on(PYTEST_CONTEXT)
def test_pytest(t: bt.TestCaseRun, context: str):
    t.h1("testing pytest project with booktest")
    t_cli(t, ["-v"], context)

    t.h1("testing pytest project with pytest")

    result = subprocess.run(["pytest", "--verbose"], cwd="examples/pytest", capture_output=True, text=True)

    number = re.compile(r"\d+(.\d+?)s")
    def replace_s(text):
        return re.sub(number, "<number>s", text)

    lines = result.stdout.split("\n")

    for i in lines:
        if i.startswith("test/"):
            t.tln(replace_s(i))
    t.tln()
    t.t(f"return code is {result.returncode}..").assertln(result.returncode==0)
