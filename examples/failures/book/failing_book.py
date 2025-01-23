import booktest as bt
import time


def test_success(t: bt.TestCaseRun):
    t.h1("succeeding test for control:")
    t.tln("ok.")


def test_fail(t: bt.TestCaseRun):
    t.h1("fail with fail() method:")
    t.fail().tln("failed!")


def test_assert(t: bt.TestCaseRun):
    t.h1("fail with assert() method:")
    t.t("is 1 == 2? ").assertln(1 == 2)


def test_exception(t: bt.TestCaseRun):
    t.h1("fail with exception:")

    raise Exception("this is an exception")

@bt.mock_env({"ENV_VAR":"VALUE"})
def test_decorated_exception(t: bt.TestCaseRun):
    t.h1("fail with exception:")

    raise Exception("this is an exception")

@bt.mock_env({"ENV_VAR":"VALUE"})
async def test_decorated_async_exception(t: bt.TestCaseRun):
    t.h1("fail with exception:")

    raise Exception("this is an exception")

@bt.monitor_memory()
async def test_memory_monitor_exception(t: bt.TestCaseRun):
    t.h1("fail with exception:")

    raise Exception("this is an exception")

