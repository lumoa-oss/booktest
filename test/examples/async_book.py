import asyncio
import time

import booktest as bt


async def test_wait(t: bt.TestCaseRun):
    t.h1("async test:")

    t.t(" * waiting on async io..")
    before = time.time()
    await asyncio.sleep(0.1)
    after = time.time()
    t.ifloatln(after-before, "s")

    t.tln(" * done")


