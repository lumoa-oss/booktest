import os

import booktest as bt
import requests
import json
import time
import httpx


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


@bt.snapshot_requests(lose_request_details=False,
                      ignore_headers=False)
def test_saved_request(t: bt.TestCaseRun):
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


@bt.snapshot_env("HOST_NAME")
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


@bt.snapshot_env("HOST_NAME")
@bt.mock_missing_env({"API_KEY": "mock"})
@bt.snapshot_requests(lose_request_details=False,
                      ignore_headers=["X-Api-Key", "X-Timestamp"])
def test_requests_with_headers(t: bt.TestCaseRun):

    t.h1("description:")

    t.tln("in this description, it's assumed that user id is significant. ")
    t.tln("this test should create 2 snapshots, one for each user")

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
    t.tln(json.dumps(response.json()["json"], indent=4))

