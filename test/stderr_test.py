import booktest as bt
import logging


class StdErrBook(bt.TestBook):

    def test_stderr(self, t: bt.TestCaseRun):
        t.tln("using logging on background.")

        logging.warning("this is a warning")

        t.err.flush()

        t.h1("err file content:")
        with open(t.err_file_name, "r") as f:
            for i in f.readlines():
                t.tln(f" * {i}")
