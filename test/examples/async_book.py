import asyncio
import json
import time

import booktest as bt

import requests
import httpx


async def test_wait(t: bt.TestCaseRun):
    t.h1("async test:")

    t.t(" * waiting on async io..")
    before = time.time()
    await asyncio.sleep(0.1)
    after = time.time()
    t.ifloatln(after-before, "s")

    t.tln(" * done")

async def test_cache(t: bt.TestCaseRun):
    t.h1("async test:")

    t.t(" * calculating things..")
    before = time.time()
    await asyncio.sleep(0.1)
    rv = 42
    after = time.time()
    t.ifloatln(after-before, "s")

    t.tln(f" * result is {rv}")

    return rv


@bt.depends_on(test_cache)
async def test_cache_use(t: bt.TestCaseRun, value):
    t.tln(f" * value is {value} ")


@bt.snapshot_requests()
async def test_requests(t: bt.TestCaseRun):
    response = requests.get("https://api.weather.gov/")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))


@bt.snapshot_httpx()
async def test_httpx(t: bt.TestCaseRun):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.weather.gov/")

        t.h1("response:")
        t.tln(json.dumps(response.json(), indent=4))






