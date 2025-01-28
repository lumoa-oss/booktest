import functools
import os
import re

import booktest as bt
import httpx
import json
import copy
import base64

from booktest.coroutines import maybe_async_call
from booktest.requests import json_to_sha1, default_encode_body
from booktest.snapshots import frozen_snapshot_path, out_snapshot_path, have_snapshots_dir
from booktest.utils import file_or_resource_exists, open_file_or_resource, accept_all


class RequestKey:

    def __init__(self,
                 json_object,
                 ignore_headers=True,
                 json_to_hash=None):
        if json_to_hash is None:
            json_to_hash = json_to_sha1

        json_object = copy.deepcopy(json_object)

        # headers contain often passwords, timestamps or other
        # information that must not be stored and cannot be used in CI
        if ignore_headers and "headers" in json_object:
            if ignore_headers is True:
                del json_object["headers"]
            else:
                headers = json_object["headers"]
                lower_ignore_headers = set([i.lower() for i in ignore_headers])
                removed = []
                for header in headers:
                    if header.lower() in lower_ignore_headers:
                        removed.append(header)
                for i in removed:
                    del headers[i]

        hash_code = json_object.get("hash")

        if hash_code is None:
            hash_code = json_to_hash(json_object)
            json_object["hash"] = hash_code

        self.json_object = json_object
        self.hash = hash_code

    def increase_order(self):
        prev_order = self.json_object.get("order", 0)
        json_object = copy.copy(self.json_object)
        json_object["order"] = prev_order + 1
        del json_object["hash"]
        return RequestKey(json_object, False)

    def url(self):
        return self.json_object.get("url")

    def to_json_object(self, hide_details):
        rv = copy.copy(self.json_object)
        rv["hash"] = self.hash

        if hide_details:
            if "headers" in rv:
                del rv["headers"]
            if "body" in rv:
                del rv["body"]

        return rv

    @staticmethod
    def from_properties(url,
                        method,
                        headers,
                        body,
                        ignore_headers,
                        json_to_hash=None,
                        encode_body=None):
        if encode_body is None:
            encode_body = default_encode_body

        json_object = {
            "url": str(url),
            "method": str(method),
            "headers": dict(headers)
        }
        if body is not None:
            json_object["body"] = encode_body(body, url, method)

        return RequestKey(json_object,
                          ignore_headers=ignore_headers,
                          json_to_hash=json_to_hash)

    @staticmethod
    def from_request(request: httpx.Request,
                     ignore_headers=True,
                     json_to_hash=None,
                     encode_body=None):
        return RequestKey.from_properties(request.url,
                                          request.method,
                                          request.headers,
                                          request.read(),
                                          ignore_headers=ignore_headers,
                                          json_to_hash=json_to_hash,
                                          encode_body=encode_body)

    def __eq__(self, other):
        return type(other) == RequestKey and self.hash == other.hash


class RequestSnapshot:

    def __init__(self,
                 request: RequestKey,
                 response: httpx.Response):
        self.request = request
        self.response = response

    def match(self, request: RequestKey):
        return self.request == request

    @staticmethod
    def from_json_object(json_object,
                         ignore_headers=True,
                         json_to_hash=None):
        response_json = json_object["response"]

        content = base64.b64decode(response_json["content"].encode("ascii")).decode("utf-8")

        response = httpx.Response(response_json["statusCode"],
                                  headers=response_json["headers"],
                                  content=content)

        return RequestSnapshot(RequestKey(json_object["request"], ignore_headers, json_to_hash),
                               response)

    def json_object(self, hide_details):
        payload = self.response.content

        # remove possible compression
        headers = dict(self.response.headers)
        if "content-encoding" in headers:
            del headers["content-encoding"]

        rv = {
            "request": self.request.to_json_object(hide_details),
            "response": {
                "headers": headers,
                "statusCode": self.response.status_code,
                "content": base64.b64encode(payload).decode("ascii")
            }
        }

        return rv

    def hash(self):
        return self.request.hash

    def __eq__(self, other):
        return isinstance(other, RequestSnapshot) and self.hash() == other.hash()


class SnapshotHttpx:

    def __init__(self,
                 t: bt.TestCaseRun,
                 lose_request_details=True,
                 ignore_headers=True,
                 json_to_hash=None,
                 encode_body=None,
                 match_request=accept_all):
        self.t = t

        self.legacy_mock_path = os.path.join(t.exp_dir_name, ".httpx")
        self.snapshot_file = frozen_snapshot_path(t, "httpx.json")
        self.snapshot_out_file = out_snapshot_path(t, "httpx.json")
        self.match_request = match_request

        self._lose_request_details = lose_request_details
        self._ignore_headers = ignore_headers
        self._json_to_hash = json_to_hash
        self._encode_body = encode_body

        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)
        self.capture_snapshots = self.refresh_snapshots or self.complete_snapshots

        # load snapshots
        snapshots = []

        # legacy support
        if os.path.exists(self.legacy_mock_path) and not self.refresh_snapshots:
            for mock_file in os.listdir(self.legacy_mock_path):
                with open(os.path.join(self.legacy_mock_path, mock_file), "r") as f:
                    snapshots.append(RequestSnapshot.from_json_object(json.load(f),
                                                                      ignore_headers=ignore_headers,
                                                                      json_to_hash=json_to_hash))

        if file_or_resource_exists(self.snapshot_file, t.resource_snapshots) and not self.refresh_snapshots:
            try:
                with open_file_or_resource(self.snapshot_file, t.resource_snapshots) as f:
                    for key, value in json.load(f).items():
                        snapshots.append(RequestSnapshot.from_json_object(value,
                                                                          ignore_headers=ignore_headers,
                                                                          json_to_hash=json_to_hash))
            except Exception as e:
                raise ValueError(f"test {self.t.name} snapshot file {self.snapshot_file} corrupted with {e}. "
                                 f"Use -S to refresh snapshots")

        self.snapshots = snapshots
        self.requests = []

        self._real_handle_request = None
        self._real_handle_async_request = None

    def mark_order(self, key: RequestKey):
        for i in self.requests:
            if key == i.request:
                key = key.increase_order()

        return key

    def get_snapshot(self, key):
        for snapshot in reversed(self.snapshots):
            if snapshot.match(key):
                if snapshot not in self.requests:
                    self.requests.append(snapshot)
                return snapshot
        return None

    def lookup_request_snapshot(self, request: httpx.Request):
        key = RequestKey.from_request(request,
                                      self._ignore_headers,
                                      self._json_to_hash,
                                      self._encode_body)

        key = self.mark_order(key)
        snapshot = self.get_snapshot(key)
        if snapshot:
            return key, snapshot.response

        if not self.capture_snapshots:
            raise ValueError(f"missing snapshot for request {request.url} - {key.hash}. "
                             f"try running booktest with '-s' flag to capture the missing snapshot")

        return key, None

    def snapshot_request(self, transport: httpx.HTTPTransport, request: httpx.Request):
        key, rv = self.lookup_request_snapshot(request)

        if rv is None:
            rv = self._real_handle_request(transport, request)
            self.requests.append(RequestSnapshot(key, rv))

        return rv

    def handle_request(self, transport: httpx.HTTPTransport, request: httpx.Request):
        if self.match_request(request):
            return self.snapshot_request(transport, request)
        else:
            return self._real_handle_request(transport, request)

    async def async_snapshot_request(self, transport: httpx.HTTPTransport, request: httpx.Request):
        key, rv = self.lookup_request_snapshot(request)

        if rv is None:
            rv = await self._real_handle_async_request(transport, request)
            self.requests.append(RequestSnapshot(key, rv))

        return rv

    async def handle_async_request(self, transport: httpx.AsyncHTTPTransport, request: httpx.Request):
        if self.match_request(request):
            return await self.async_snapshot_request(transport, request)
        else:
            return await self._real_handle_async_request(transport, request)

    def start(self):
        self._real_handle_request = httpx.HTTPTransport.handle_request
        self._real_handle_async_request = httpx.AsyncHTTPTransport.handle_async_request

        def mocked_handle_request(
                transport: httpx.HTTPTransport, request: httpx.Request
        ) -> httpx.Response:
            return self.handle_request(transport, request)

        setattr(
            httpx.HTTPTransport,
            "handle_request",
            mocked_handle_request)

        async def mocked_handle_async_request(
                transport: httpx.AsyncHTTPTransport, request: httpx.Request
        ) -> httpx.Response:
            return await self.handle_async_request(transport, request)

        setattr(
            httpx.AsyncHTTPTransport,
            "handle_async_request",
            mocked_handle_async_request)

        return self

    def stop(self):
        setattr(
            httpx.HTTPTransport,
            "handle_request",
            self._real_handle_request)
        setattr(
            httpx.AsyncHTTPTransport,
            "handle_async_request",
            self._real_handle_async_request)

        # let's store everything in one file to avoid spamming git
        stored = {}
        for snapshot in self.requests:
            name = snapshot.hash()
            stored[name] = snapshot.json_object(self._lose_request_details)

        have_snapshots_dir(self.t)
        with open(self.snapshot_out_file, "w") as f:
            json.dump(stored, f, indent=4)

    def t_snapshots(self):
        self.t.h1("httpx snaphots:")
        for i in sorted(self.requests, key=lambda i: (i.request.url(), i.hash())):
            if not self.get_snapshot(i.request):
                self.t.diff() # force test to fail if snapshot was missing
            self.t.tln(f" * {i.request.url()} - {i.hash()}")

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.t_snapshots()


def snapshot_httpx(lose_request_details=True,
                   ignore_headers=True,
                   json_to_hash=None,
                   encode_body=None,
                   match_request=None,
                   url=None):
    """
    @param lose_request_details Saves no request details to avoid leaking keys
    @param ignore_headers Ignores all headers (True) or specific header list
    @param json_to_hash allows adding your own json to hash for calculating hash code to request.
           can be used to print or prune e.g. http arguments in case they contain e.g. platform specific
           details or timestamps
    @param encode_body allows adding your own body encoding for removing e.g. platform or time details from
           request bodies. this needs to always return a string. encode body method receives body, url and method
    """
    matchers = []
    if match_request is not None:
        matchers.append(match_request)
    if url is not None:
        url_regex = re.compile(url)
        matchers.append(lambda x: url_regex.match(str(x.url)))

    if len(matchers) > 0:
        matcher = lambda x:any([i(x) for i in matchers])
    else:
        matcher = accept_all

    def decorator_depends(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with SnapshotHttpx(t, lose_request_details, ignore_headers, json_to_hash, encode_body, matcher):
                return await maybe_async_call(func , args, kwargs)
        wrapper._original_function = func
        return wrapper

    return decorator_depends
