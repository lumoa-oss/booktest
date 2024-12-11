import os
import sys

import booktest as bt

import subprocess

import re


class BooktestProcess:

    def __init__(self, args, context = None, out_file = None, err_file = None):
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

        self.process = subprocess.Popen(["/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/bin/booktest"] + self.args,
                                        cwd=self.context,
                                        env={},
                                        stdout=self.out,
                                        stderr=self.err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.wait()
        self.out.close()
        self.err.close()


def t_cli(t: bt.TestCaseRun, args, context=None):
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


def test_help(t: bt.TestCaseRun):
    t_cli(t, ["-h"])


def test_list(t: bt.TestCaseRun):
    t_cli(t, ["-l"])


def test_run(t: bt.TestCaseRun):
    t_cli(t, [])


def test_parallel(t: bt.TestCaseRun):
    t_cli(t, ["-p"])


def test_context(t: bt.TestCaseRun):
    t_cli(t, ["--context", "examples/predictor"], context=".")


def test_configurations(t: bt.TestCaseRun):
    t_cli(t, ["-v"], context="examples/configurations")
