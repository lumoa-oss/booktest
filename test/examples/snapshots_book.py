import booktest as bt
import requests
import json


class SnapshotsTestBook(bt.TestBook):

    @bt.snapshot_requests()
    def test_requests(self, t: bt.TestCaseRun):
        response = requests.get("https://api.weather.gov/")

        t.h1("response:")
        t.tln(json.dumps(response.json(), indent=4))

    @bt.snapshot_env("TEST_ENV_VARIABLE")
    def test_env(self, t: bt.TestCaseRun):
        response = requests.get("https://api.weather.gov/")

        t.h1("response:")
        t.tln(json.dumps(response.json(), indent=4))



