import booktest as bt
import time


def test_fast(t: bt.TestCaseRun):
    t.tln("done.")

def test_slow(t: bt.TestCaseRun):
    t.tln("waiting 3s...")
    time.sleep(3)
    t.tln("done.")

