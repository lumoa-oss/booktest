import booktest as bt


def test_hello(t: bt.TestCaseRun):
    t.h1("This test prints hello world")
    t.tln("hello world")
