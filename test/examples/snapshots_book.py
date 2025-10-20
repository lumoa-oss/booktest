import asyncio
import copy
import os
import random
from datetime import datetime

import booktest as bt
import requests
import json
import time
import httpx

from booktest.snapshots.functions import SnapshotFunctions, MockFunctions
from booktest.snapshots.requests import json_to_sha1, default_encode_body


@bt.snapshot_requests()
def test_requests(t: bt.TestCaseRun):
    response = requests.get("https://postman-echo.com/get")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))

@bt.snapshot_requests(url="https://postman-echo.com/get")
def test_requests_filter(t: bt.TestCaseRun):
    response = requests.get("https://postman-echo.com/get")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))

@bt.snapshot_httpx()
def test_httpx(t: bt.TestCaseRun):
    response = httpx.get("https://postman-echo.com/get")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))


@bt.snapshot_httpx(url="https://postman-echo.com/get")
def test_httpx_filter(t: bt.TestCaseRun):
    response = httpx.get("https://postman-echo.com/get")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))


@bt.snapshot_requests()
def test_requests_sequence(t: bt.TestCaseRun):
    t.h1("description:")
    t.tln("sometimes apis are stateful and we want to keep track of response sequence")
    t.tln("following requests should provide different answer")

    t.h1("first response:")
    response = requests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam")
    t.tln(json.dumps(response.json()["dateTime"], indent=4))

    time.sleep(0.1)

    t.h1("second response:")
    response = requests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam")
    t.tln(json.dumps(response.json()["dateTime"], indent=4))


@bt.snapshot_httpx()
def test_httpx_sequence(t: bt.TestCaseRun):
    t.h1("description:")
    t.tln("sometimes apis are stateful and we want to keep track of response sequence")
    t.tln("following requests should provide different answer")

    t.h1("first response:")
    response = httpx.get("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam")
    t.tln(json.dumps(response.json()["dateTime"], indent=4))

    time.sleep(0.1)

    t.h1("second response:")
    response = httpx.get("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam")
    t.tln(json.dumps(response.json()["dateTime"], indent=4))


def drop_random_parameter_json(json_object):
    json_object = copy.deepcopy(json_object)

    url = str(json_object["url"])
    if url.startswith("https://httpbin.org/anything/"):
        # remove random url component
        json_object["url"] = "https://httpbin.org/anything/"

    return json_to_sha1(json_object)

def drop_date_encode_body(body, request, url):
    json_object = json.loads(body.decode("utf-8"))

    del json_object["date"]

    return default_encode_body(json.dumps(json_object).encode("utf-8"), request, url)

@bt.snapshot_requests(json_to_hash=drop_random_parameter_json, encode_body=drop_date_encode_body)
def test_requests_deterministic_hashes(t: bt.TestCaseRun):
    t.h1("request:")

    random_id = random.randint(0, 10000000)
    t.i(f" * random url component is: {random_id}").tln()

    host_name = f"https://httpbin.org/anything/{random_id}"
    response = (
        t.i(f" * making post request to {host_name} in ").imsln(
            lambda:
            requests.post(
                host_name,
                json={
                    "message": "hello",
                    "date": datetime.now().isoformat()
                })))

    t.h1("response:")
    t.tln(json.dumps(response.json()["json"], indent=4))

@bt.snapshot_httpx(json_to_hash=drop_random_parameter_json, encode_body=drop_date_encode_body)
def test_requests_deterministic_hashes(t: bt.TestCaseRun):
    t.h1("request:")

    random_id = random.randint(0, 10000000)
    t.i(f" * random url component is: {random_id}").tln()

    host_name = f"https://httpbin.org/anything/{random_id}"
    response = (
        t.i(f" * making post request to {host_name} in ").imsln(
            lambda:
            httpx.post(
                host_name,
                json={
                    "message": "hello",
                    "date": datetime.now().isoformat()
                })))

    t.h1("response:")
    t.tln(json.dumps(response.json()["json"], indent=4))

@bt.snapshot_requests(lose_request_details=False,
                      ignore_headers=["User-Agent"])
def test_saved_request(t: bt.TestCaseRun):
    t.h1("description:")
    t.tln("in this test, the headers are stored within the expectation files.")

    response = requests.post("https://httpbin.org/anything", json={
        "message": "hello"
    })

    t.h1("response:")
    t.tln(json.dumps(response.json()["json"], indent=4))


@bt.snapshot_env("TEST_ENV_VARIABLE")
def test_env(t: bt.TestCaseRun):
    t.h1("test environment variable:")
    t.keyvalueln(" * TEST_ENV_VARIABLE:", os.environ["TEST_ENV_VARIABLE"])


@bt.mock_env({
    "TEST_ENV_VARIABLE": "hello2"
})
def test_mock_env(t: bt.TestCaseRun):
    t.h1("test environment variable:")
    t.keyvalueln(" * TEST_ENV_VARIABLE:", os.environ["TEST_ENV_VARIABLE"])


@bt.mock_env({
    "TEST_ENV_VARIABLE": "hello2"
})
def test_mock_env(t: bt.TestCaseRun):
    t.h1("test environment variable:")
    t.keyvalueln(" * TEST_ENV_VARIABLE:", os.environ["TEST_ENV_VARIABLE"])


@bt.mock_env({
    "SHELL": None,
    "HOME": None,
    "LANG": None,
    "USERNAME": None
})
def test_mock_env_deletions(t: bt.TestCaseRun):
    t.h1("deleted variables:")
    t.keyvalueln(" * SHELL:", os.environ.get("SHELL"))
    t.keyvalueln(" * HOME:", os.environ.get("HOME"))
    t.keyvalueln(" * LANG:", os.environ.get("LANG"))
    t.keyvalueln(" * USERNAME:", os.environ.get("USERNAME"))


@bt.snapshot_env("HOST_NAME")  # should be "https://httpbin.org/anything"
@bt.mock_missing_env({"API_KEY": "mock"})
@bt.snapshot_requests()
def test_requests_and_env(t: bt.TestCaseRun):
    t.h1("request:")

    host_name = os.environ["HOST_NAME"]
    response = (
        t.t(f"making post request to {host_name} in ").imsln(
            lambda:
            requests.post(
                host_name,
                json={
                    "message": "hello"
                },
                headers={
                    "X-Api-Key": os.environ["API_KEY"]
                })))

    t.h1("response:")
    t.tln(json.dumps(response.json()["json"], indent=4))


@bt.snapshot_env("HOST_NAME")  # should be "https://httpbin.org/anything"
@bt.mock_missing_env({"API_KEY": "mock"})
@bt.snapshot_requests(lose_request_details=False,
                      ignore_headers=["X-Api-Key", "X-Timestamp", "User-Agent"])
def test_requests_with_headers(t: bt.TestCaseRun):

    t.h1("description:")

    t.tln("in this description, it's assumed that user id is significant. ")
    t.tln("this test should create 2 snapshots, one for each user")
    t.tln()
    t.tln("note: you may need to freeze this twice, because on first run 2 different calls")
    t.tln("are made for user 1, but only snapshot is stored. recalling first run is necesssary,")
    t.tln("because otherwise the system may get stuck on timeouts. this will cause the result to")
    t.tln("be different on second run, as in first run 2 calls are done, while on second run")
    t.tln("one snapshot is used twice.")

    response = requests.post(os.environ["HOST_NAME"], json={
        "message": "hello"
    }, headers={
        "X-Api-Key": os.environ["API_KEY"],
        "X-Timestamp": str(time.time()),
        "X-User-Id": "1"
    })

    t.h1("response for user 1:")
    t.tln(json.dumps(response.json(), indent=4))

    response = requests.post(os.environ["HOST_NAME"], json={
        "message": "hello"
    }, headers={
        "X-Api-Key": os.environ["API_KEY"],
        "X-Timestamp": str(time.time()),
        "X-User-Id": "1"
    })

    t.h1("2nd response for user 1:")
    t.tln(json.dumps(response.json(), indent=4))

    response = requests.post(os.environ["HOST_NAME"], json={
        "message": "hello"
    }, headers={
        "X-Api-Key": os.environ["API_KEY"],
        "X-Timestamp": str(time.time()),
        "X-User-Id": "2"
    })

    t.h1("response for user 2:")
    t.tln(json.dumps(response.json(), indent=4))


def non_deterministic_and_slow_algorithm(input):
    rnd = random.Random(input)
    noise = random.Random(int(time.time()))

    rv = []
    for i in range(rnd.randint(0, 3) + 1 + noise.randint(0, 1)):
        rv.append(rnd.randint(0, 10000) + noise.randint(-1, 1))
        time.sleep(1)

    return rv


def multiargs(a, b, c, *args, **kwargs):
    return { "a": a, "b": b, "c": c, "args": list(args), "kwargs": kwargs }


def test_function_snapshots(t: bt.TestCaseRun):
    with SnapshotFunctions(t, []) as s:
        t.h1("snapshots:")

        t.keyvalueln(" * timestamp:", s.snapshot(time.time_ns))
        t.keyvalueln(" * random:", s.snapshot(random.random))

        t.h1("algorithm snapshot:")

        # NOTE: These results vary randomly
        result = (
            t.t(" * calculating result..").imsln(
                lambda: s.snapshot(non_deterministic_and_slow_algorithm, 124)))

        t.keyvalueln(" * result:", result)

        t.h1("args:")
        t.keyvalueln(" * args: 123:", s.snapshot(multiargs, 1, 2, 3))
        t.keyvalueln(" * args: 12345:", s.snapshot(multiargs, 1, 2,  3, 4, 5))
        t.keyvalueln(" * named args:", s.snapshot(multiargs, a=1, b=2, c=3, d=4, e=5))


@bt.snapshot_functions(time.time_ns,
                       random._inst.random,
                       non_deterministic_and_slow_algorithm,
                       multiargs)
def test_auto_function_snapshots(t: bt.TestCaseRun):
    t.h1("snapshots:")

    t.keyvalueln(" * timestamp:", time.time_ns())
    t.keyvalueln(" * random:", random._inst.random())

    t.h1("algorithm snapshot:")

    result = (
        t.t(" * calculating result..").imsln(
            lambda: non_deterministic_and_slow_algorithm(124)))

    t.keyvalueln(" * result:", result)

    t.h1("args:")
    t.keyvalueln(" * args: 123:", multiargs(1, 2, 3))
    t.keyvalueln(" * args: 12345:", multiargs(1, 2, 3, 4, 5))
    t.keyvalueln(" * named args:", multiargs(a=1, b=2, c=3, d=4, e=5))


def plus_one(value):
    return value + 1

def minus_one(value):
    return value - 1

@bt.snapshot_functions(plus_one, minus_one)
async def test_complex_function_snapshots(t: bt.TestCaseRun):
    t.h1("running 20 snapshots in random order to 2 different methods:")

    values = list(range(20))
    r = random.Random(time.time())
    r.shuffle(values) # use true randomization

    results = {}

    for value in values:
        if value % 2 == 0:
            results[value] = plus_one(value)
        else:
            results[value] = minus_one(value)

    t.tln("done.")
    t.tln()
    t.iln(f"randomized order is {', '.join(map(str, values))}")

    t.h1("results:")
    check_sum = 0
    for value, result in sorted(list(results.items())):
        t.keyvalueln(f" * {value}:", result)
        check_sum += result

    t.tln()
    t.keyvalueln("check sum:", check_sum)

def mock_time_ns():
    return 10000000000000


def mock_random():
    return 42


async def async_random():
    await asyncio.sleep(0.1)
    return random.randint(0, 10000000)


async def mock_async_random():
    return 23


@bt.mock_functions({
    time.time_ns: mock_time_ns,
    random._inst.random: mock_random,
    async_random: mock_async_random
})
async def test_mock_functions(t: bt.TestCaseRun):
    t.h1("mocks:")

    t.keyvalueln(" * timestamp:", time.time_ns())
    t.keyvalueln(" * random:", random._inst.random())
    t.keyvalueln(" * async random:", await async_random())
