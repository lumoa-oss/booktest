import booktest as bt
import requests
import json


class MockingTestBook(bt.TestBook):

    @bt.snapshot_requests()
    def test_requests(self, t: bt.TestCaseRun):
        response = requests.get("https://api.weather.gov/")

        t.h1("response:")
        t.tln(json.dumps(response.json(), indent=4))


