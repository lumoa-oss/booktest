import random
import time

import booktest as bt


@bt.snapshot_functions(time.time_ns,
                       random._inst.random)
def test_auto_function_snapshots(t: bt.TestCaseRun):
    t.h1("snapshots:")

    t.keyvalueln(" * timestamp:", time.time_ns())
    t.keyvalueln(" * random:", random._inst.random())
