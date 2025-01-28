import time
import random

import requests
import json
import httpx

import booktest as bt


@bt.snapshot_requests()
def test_requests(t: bt.TestCaseRun):
    response = requests.get("https://api.weather.gov/")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))


@bt.snapshot_httpx()
def test_httpx(t: bt.TestCaseRun):
    response = httpx.get("https://api.weather.gov/")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))


def hello_world():
    return "hello world"

@bt.snapshot_functions(time.time_ns,
                       random._inst.random,
                       hello_world)
def test_function_snapshot(t: bt.TestCaseRun):
    t.h1("snapshot:")

    t.keyvalueln(" * hello:", hello_world())
