import os.path as path
import os
import inspect
from enum import Enum
import time
import pickle
import functools
import shutil

import traceback
import sys
import json
import argparse

from collections import OrderedDict
from coverage import Coverage

from booktest.cache import LruCache
from booktest.review import report_case_begin, case_review, report_case_result
from booktest.tokenizer import TestTokenizer, BufferIterator
from booktest.reports import TestResult, CaseReports

from enum import Enum


import pickle



class TestCaseRun:
    """
    Runs an individual test case.

    few concerns:

    1. behavior testing
    2. maintaining state
    3. workflow
    4. integration with unittesting
    """
    def __init__(self,
                 run,
                 test_path,
                 config,
                 output):
        relative_dir, name = path.split(test_path)

        # name & context
        self.run = run
        self.name = name
        self.test_path = test_path

        # configuration
        self.always_interactive = config.get("always_interactive", False)
        self.interactive = config.get("interactive", self.always_interactive)
        self.verbose = config.get("verbose", False)
        self.point_error_pos = config.get("point_error_pos", False)
        self.config = config

        if output is None:
            output = sys.stdout
        self.output = output

        # expectation file
        self.exp_base_dir = path.join(run.exp_dir, relative_dir)
        os.system(f"mkdir -p {self.exp_base_dir}")
        self.exp_file_name = path.join(self.exp_base_dir, name + ".md")
        self.exp_dir_name = path.join(self.exp_base_dir, name)
        self.exp_file_exists = path.exists(self.exp_file_name)
        self.exp = None
        self.exp_line = None
        self.exp_line_number = None
        self.exp_tokens = None

        # prepare output
        self.out_base_dir = path.join(run.out_dir, relative_dir)
        os.system(f"mkdir -p {self.out_base_dir}")
        self.out_file_name = path.join(self.out_base_dir, name + ".md")
        self.out_dir_name = path.join(self.out_base_dir, name)
        self.out_tmp_dir_name = path.join(self.out_base_dir, name + ".tmp")
        self.out = open(self.out_file_name, "w")
        self.out_line = ""

        # prepare reporting
        self.rep_file_name = path.join(self.out_base_dir, name + ".txt")
        self.rep = open(self.rep_file_name, "w")

        # error management
        #
        # let's separate diff from proper failure
        #
        self.line_diff = None
        self.line_error = None
        self.line_number = 0
        self.diffs = 0
        self.errors = 0
        # this is needed for sensible default behavior, when sections end
        self.last_checked = False

        # reporting
        self.took_ms = None
        self.result = None

        # purge old output files
        if path.exists(self.out_dir_name):
            shutil.rmtree(self.out_dir_name)

        if path.exists(self.out_tmp_dir_name):
            shutil.rmtree(self.out_tmp_dir_name)

        self.reset_exp_reader()

    def print(self, *args, sep=' ', end='\n'):
        print(*args, sep=sep, end=end, file=self.output)

    def report(self, *args, sep=' ', end='\n'):
        print(*args, sep=sep, end=end, file=self.rep)
        if self.verbose:
            self.print(*args, sep=sep, end=end)

    def reset_exp_reader(self):
        self.close_exp_reader()
        if self.exp_file_exists:
            self.exp = open(self.exp_file_name, "r")
        else:
            self.exp = None
        self.exp_line = None
        self.exp_line_number = 0
        self.exp_tokens = None
        self.next_exp_line()

    def tmp_file(self, filename):
        if not path.exists(self.out_tmp_dir_name):
            os.mkdir(self.out_tmp_dir_name)
        return path.join(self.out_tmp_dir_name, filename)

    def file(self, filename):
        # prepare new output files
        if not path.exists(self.out_dir_name):
            os.mkdir(self.out_dir_name)
        return path.join(self.out_dir_name, filename)

    def start(self, title=None):
        self.started = time.time()
        report_case_begin(self.print,
                          self.test_path,
                          title,
                          self.verbose)

    def review(self, result):
        return case_review(
            self.exp_base_dir,
            self.out_base_dir,
            self.name,
            result,
            self.config)

    def end(self):
        self.ended = time.time()
        self.took_ms = 1000*(self.ended - self.started)

        self.close()

        if self.errors != 0:
            rv = TestResult.FAIL
        elif self.diffs != 0 or not path.exists(self.exp_file_name):
            rv = TestResult.DIFF
        else:
            rv = TestResult.OK

        report_case_result(
            self.print,
            self.test_path,
            rv,
            self.took_ms,
            self.verbose)

        rv, interaction = self.review(rv)

        if self.verbose:
            self.print("")

        self.result = rv

        return rv, interaction

    def close_exp_reader(self):
        if self.exp is not None:
            self.exp.close()
            self.exp = None

    def close(self):
        self.close_exp_reader()
        self.out.close()
        self.out = None
        self.rep.close()
        self.rep = None

    def next_exp_line(self):
        if self.exp_file_exists:
            if self.exp:
                line = self.exp.readline()
                if len(line) == 0:
                    self.close_exp_reader()
                    self.exp_line = None
                    self.exp_tokens = None
                    self.exp_line_number += 1
                else:
                    self.exp_line_number += 1
                    self.exp_line = line[0:len(line)-1]
                    self.exp_tokens =\
                        BufferIterator(TestTokenizer(self.exp_line))
            elif self.last_checked:
                self.exp_line = None
                self.exp_tokens = None

    def jump(self, line_number):
        if self.exp_file_exists:

            if line_number < self.exp_line_number:
                self.reset_exp_reader()

            while (self.exp_line is not None
                   and self.exp_line_number < line_number):
                self.next_exp_line()

    def seek(self, is_line_ok, begin=0, end=sys.maxsize):
        """
        Seeks an expectation file line that matches the is_line_ok()
        lambda. The seeking is started on 'begin' line and
        it ends on the 'end' line.

        NOTE: The seeks starts from the cursor position,
        but it may restart seeking from the beginning of the file,
        if the sought line is not found.

        NOTE: this is really an O(N) scanning operation.
              it may restart at the beginning of file and
              it typically reads the the entire file
              on seek failures.
        """
        if self.exp_file_exists:
            at_line_number = self.exp_line_number

            # scan, until the anchor is found
            while (self.exp_line is not None
                   and not is_line_ok(self.exp_line)
                   and self.exp_line_number < end):
                self.next_exp_line()
            if self.exp_line is None:
                # if anchor was not found, let's look for previous location
                # or alternatively: let's return to the original location
                self.jump(begin)
                while (self.exp_line is not None
                       and not is_line_ok(self.exp_line)
                       and self.exp_line_number < at_line_number):
                    self.next_exp_line()

    def seek_line(self, anchor, begin=0, end=sys.maxsize):
        return self.seek(lambda x: x == anchor, begin, end)

    def seek_prefix(self, prefix):
        return self.seek(lambda x: x.startswith(prefix))

    def write_line(self):
        self.out.write(self.out_line)
        self.out.write('\n')
        self.out_line = ""
        self.next_exp_line()
        self.line_number = self.line_number + 1

    def commit_line(self):
        if self.line_error is not None or self.line_diff is not None:
            symbol = "?"
            pos = None
            if self.line_diff is not None:
                self.diffs += 1
                pos = self.line_diff
            if self.line_error is not None:
                symbol = "!"
                self.errors += 1
                pos = self.line_error
            if self.exp_line is not None:
                self.report(f"{symbol} {self.out_line:60s} | "
                            f"{self.exp_line}")
            else:
                self.report(f"{symbol} {self.out_line:60s} | EOF")
            if self.point_error_pos:
                self.report("  " + (" " * pos) + "^")

            self.write_line()
            self.line_error = None
            self.line_diff = None
        else:
            self.report(f"  {self.out_line}")
            self.write_line()

    def head_exp_token(self):
        if self.exp_tokens is not None:
            if self.exp_tokens.has_next():
                return self.exp_tokens.head
            else:
                return '\n'
        else:
            return None

    def next_exp_token(self):
        if self.exp_tokens is not None:
            if self.exp_tokens.has_next():
                return next(self.exp_tokens)
            else:
                return '\n'
        else:
            return None

    def feed_token(self, token, check=False):
        exp_token = self.next_exp_token()
        self.last_checked = check
        if self.exp_file_exists \
           and token != exp_token \
           and check:
            self.diff()
        if token == '\n':
            self.commit_line()
        else:
            self.out_line = self.out_line + token
        return self

    def test_feed_token(self, token):
        self.feed_token(token, check=True)
        return self

    def test_feed(self, text):
        tokens = TestTokenizer(str(text))
        for t in tokens:
            self.test_feed_token(t)
        return self

    def feed(self, text):
        tokens = TestTokenizer(text)
        for t in tokens:
            self.feed_token(t)
        return self

    def diff(self):
        """ an unexpected difference encountered"""
        if self.line_diff is None:
            self.line_diff = len(self.out_line)
        return self

    def fail(self):
        """ a proper failure encountered """
        if self.line_error is None:
            self.line_error = len(self.out_line)
        return self

    def anchor(self, anchor):
        self.seek_prefix(anchor)
        self.t(anchor)
        return self

    def anchorln(self, anchor):
        self.seek_line(anchor)
        self.tln(anchor)
        return self

    def header(self, header):
        if self.line_number > 0:
            check = self.last_checked and self.exp_line is not None
            self.feed_token("\n", check=check)
        self.anchorln(header)
        self.tln("")
        return self

    def tmsln(self, f, max_ms):
        before = time.time()
        rv = f()
        after = time.time()
        ms = (after-before)*1000
        if ms > max_ms:
            self.fail().tln(f"{(after - before) * 1000:.2f} ms > "
                            f"max {max_ms:.2f} ms! (failed)")
        else:
            old = self.head_exp_token()
            try:
                if old is not None:
                    old = float(old)
            except ValueError:
                old = None

            self.i(f"{(after-before)*1000:.2f} ms")
            if old is not None:
                self.iln(f" (was {old:.2f} ms)")
            else:
                self.iln()

        return rv

    def imsln(self, f):
        return self.tmsln(f, sys.maxsize)

    def h(self, level, title):
        self.header(f"{'#' * level} {title}")
        return self

    def h1(self, title):
        self.header("# " + title)
        return self

    def h2(self, title):
        self.header("## " + title)
        return self

    def h3(self, title):
        self.header("### " + title)
        return self

    def timage(self, file, alt_text=None):
        if alt_text is None:
            alt_text = os.path.splitext(os.path.basename(file))[0]
        self.tln(f"![{alt_text}]({file[len(self.out_base_dir)+1:]})")
        return self

    def ttable(self, table: dict):
        import pandas as pd
        self.tdf(pd.DataFrame(table))
        return self

    def tdf(self, df):
        """
        df should be of pd.DataFrame or compatible type
        """
        pads = []
        for column in df.columns:
            max_len = len(column)
            for i in df.index:
                max_len = max(max_len, len(str(df[column][i])))
            pads.append(max_len)

        buf = ""
        buf += "|"
        for i, column in enumerate(df.columns):
            buf += column.ljust(pads[i])
            buf += "|"
        self.iln(buf)
        buf = "|"
        for i in pads:
            buf += "-" * i
            buf += "|"
        self.tln(buf)
        for i in df.index:
            self.t("|")
            for j, column in enumerate(df.columns):
                buf = str(df[column][i])\
                          .replace("\r", " ")\
                          .replace("\n", " ")\
                          .strip()

                self.t(buf)
                self.i(" " * (pads[j]-len(buf)))

                self.t("|")
            self.tln()
        return self

    def tlist(self, list, prefix=" * "):
        for i in list:
            self.tln(f"{prefix}{i}")

    def tset(self, items, prefix=" * "):
        """
        This method used to print and compare a set of items to expected set
        in out of order fashion. It will first scan the next elements
        based on prefix. After this step, it will check whether the items
        were in the list.

        NOTE: this method may be slow, if the set order is unstable.
        """
        compare = None

        if self.exp_line is not None:
            begin = self.exp_line_number
            compare = set()
            while (self.exp_line is not None
                   and self.exp_line.startswith(prefix)):
                compare.add(self.exp_line[len(prefix):])
                self.next_exp_line()
            end = self.exp_line_number

        for i in items:
            i_str = str(i)
            line = f"{prefix}{i_str}"
            if compare is not None:
                if i_str in compare:
                    self.seek_line(line, begin, end)
                    compare.remove(i_str)
                else:
                    self.diff()
            self.iln(line)

        if compare is not None:
            if len(compare) > 0:
                self.diff()
            self.jump(end)

    def assertln(self, cond, error_message=None):
        if cond:
            self.iln("ok")
        else:
            self.fail()
            if error_message:
                self.iln(error_message)
            else:
                self.iln("FAILED")

    def must_apply(self, it, title, cond, error_message=None):
        prefix = f" * MUST {title}..."
        self.i(prefix).assertln(cond(it), error_message)

    def must_contain(self, it, member):
        self.must_apply(it, f"have {member}", lambda x: member in x)

    def must_equal(self, it, value):
        self.must_apply(it, f"equal {value}", lambda x: x == value)

    def must_be_a(self, it, typ):
        self.must_apply(it,
                        f"be a {typ}",
                        lambda x: type(x) == typ,
                        f"was {type(it)}")

    def it(self, name, it):
        return TestIt(self, name, it)

    def t(self, text):
        self.test_feed(text)
        return self

    def tformat(self, value):
        self.tln(json.dumps(value_format(value), indent=2))
        return self

    def tln(self):
        self.test_feed("\n")
        return self

    def keyvalueln(self, key, value):
        self.anchor(key)
        self.tln(f" {value}")
        return self

    def tln(self, text=""):
        self.test_feed(text)
        self.test_feed("\n")
        return self

    def i(self, text):
        self.feed(text)
        return self

    def iln(self, text=""):
        self.feed(text)
        self.feed("\n")
        return self


def value_format(value):
    value_type = type(value)
    if value_type is list:
        rv = []
        for item in value:
            rv.append(value_format(item))
    elif value_type is dict:
        rv = {}
        for key in value:
            rv[key] = value_format(value[key])
    else:
        rv = value_type.__name__
    return rv


class TestIt:
    """ utility for making assertions related to a specific object """

    def __init__(self, run: TestCaseRun, title: str, it):
        self.run = run
        self.title = title
        self.it = it
        run.h2(title + "..")

    def must_contain(self, member):
        self.run.must_contain(self.it, member)
        return self

    def must_equal(self, member):
        self.run.must_equal(self.it, member)
        return self

    def must_be_a(self, typ):
        self.run.must_be_a(self.it, typ)
        return self

    def must_apply(self, title, cond):
        self.run.must_apply(self.it, title, cond)
        return self

    def member(self, title, select):
        return TestIt(self.run, self.title + "." + title, select(self.it))

