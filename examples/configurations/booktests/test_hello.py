import booktest as bt

import hello


def test_hello(t: bt.TestCaseRun):
    t.tln(f"the message is {hello.hello()}")