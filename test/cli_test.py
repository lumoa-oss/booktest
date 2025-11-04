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
FAILURES_CONTEXT = bt.Resource("examples/failures")
BROKEN_SNAPSHOT_CONTEXT = bt.Resource("examples/broken_snapshots")



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

        # Use minimal environment - preserve PATH for finding Python/executables
        clean_env = {
            'PATH': os.environ.get('PATH', ''),
            'PYTHONPATH': os.environ.get('PYTHONPATH', ''),
            'HOME': os.environ.get('HOME', ''),
        }
        self.process = subprocess.Popen([booktest_exec_path()] + self.args,
                                        cwd=self.context,
                                        env=clean_env,
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

    workdir = os.getcwd()
    homedir = os.path.expanduser("~")

    def replace_wd(text: str):
        return text.replace(workdir, "<workdir>")

    def replace_hd(text: str):
        return text.replace(homedir, "<homedir>")

    def replace_ms(text):
        return re.sub(number, "<number> ms", text)

    def do_diff(text):
        return "<homedir>" not in text

    def mask(text):
        return replace_ms(replace_hd(replace_wd(text)))

    with open(out_file) as f:
        content = mask(f.read())
        if do_diff(content):
            t.tln(content)
        else:
            t.iln(content)

    with open(err_file) as f:
        err = mask(f.read())

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


@bt.depends_on(PREDICTOR_CONTEXT)
def test_narrow_detection(t: bt.TestCaseRun, context: str):
    t.h1("description:")

    t.tln("narrow detection only run detection in related modules/test suites. ")
    t.tln("this test merely verifies that nothing breaks, when invoking the code")

    t_cli(t, ["--narrow-detection", "book/predictor_book.py"], context)


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


@bt.depends_on(FAILURES_CONTEXT)
def test_failures(t: bt.TestCaseRun, context: str):
    # let's not have -v parallel flag here, because python produces different
    # exception stack traces depending of the python version
    #
    # the key thing to test here is that tests fail and they don't get stuck
    t_cli(t, [], context)


def break_snapshots(t: bt.TestCaseRun, context:dir, title="breaking snapshots"):
    path = "books/book/broken_snapshots"
    files = [
        "function_snapshot.snapshots.json",
        "function_snapshot/_snapshots/functions.json",
        "httpx/_snapshots/httpx.json",
        "requests/_snapshots/requests.json"
    ]

    t.h1(title)
    for file in files:
        snapshot_file = os.path.join(context, path, file)

        with open(snapshot_file, "w") as f:
            f.write("\n# broken snapshot line\n")
        t.tln(f" * broke snapshot file: {snapshot_file}")

@bt.depends_on(BROKEN_SNAPSHOT_CONTEXT)
def test_broken_snapshots(t: bt.TestCaseRun, context: str):
    t.h1("description:")
    t.tln("this test verifies that:")
    t.tln()
    t.tln(" 1) malformed snasphots (e.g. because git merge) break the test")
    t.tln(" 2) and informs user about need to recapture them with -s")
    break_snapshots(t, context)
    t_cli(t, [], context)
    break_snapshots(t, context, "rebreak snapshots to keep git status clean:")


@bt.depends_on(BROKEN_SNAPSHOT_CONTEXT)
def test_refreshing_broken_snapshots(t: bt.TestCaseRun, context: str):
    t.h1("description:")
    t.tln("this test verifies that:")
    t.tln()
    t.tln(" 1) snapshots can be recreated")
    t.tln(" 2) and tool requires user to accept & store recreated snapshot even if their hashes are the same")
    break_snapshots(t, context)
    t_cli(t, ["-S", "-v"], context)
    break_snapshots(t, context, "rebreak snapshots to keep git status clean:")


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
