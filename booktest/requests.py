import contextlib
import functools
import hashlib
import os
import types
import booktest as bt
import requests
from requests import adapters
import json
import threading
import sys
import six
import copy
import base64


def json_to_sha1(json_object):
    h = hashlib.sha1()
    h.update(json.dumps(json_object, sort_keys=True).encode())
    hash_code = str(h.hexdigest())
    return hash_code


def default_encode_body(body, _url, _method):
    if body is not None:
        if isinstance(body, str):
            body = body.encode("utf-8")
        if isinstance(body, bytes):
            return base64.b64encode(body).decode("ascii")
        else:
            raise ValueError(f"unexpected body {body} of type {type(body)}")


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
        return RequestKey(json_object, ignore_headers=ignore_headers, json_to_hash=json_to_hash)

    @staticmethod
    def from_request(request: requests.PreparedRequest,
                     ignore_headers=True,
                     json_to_hash=None,
                     encode_body=None):
        return RequestKey.from_properties(request.url,
                                          request.method,
                                          request.headers,
                                          request.body,
                                          ignore_headers=ignore_headers,
                                          json_to_hash=json_to_hash,
                                          encode_body=encode_body)

    def __eq__(self, other):
        return type(other) == RequestKey and self.hash == other.hash


class RequestSnapshot:

    def __init__(self,
                 request: RequestKey,
                 response: requests.Response):
        self.request = request
        self.response = response

    def match(self, request: RequestKey):
        return self.request == request

    @staticmethod
    def from_json_object(json_object, ignore_headers=True, json_to_hash=None):
        response_json = json_object["response"]

        response = requests.Response()
        response.headers = response_json["headers"]
        response.status_code = response_json["statusCode"]
        response.encoding = response_json["encoding"]
        response._content = response_json["content"].encode()

        return RequestSnapshot(RequestKey(json_object["request"], ignore_headers, json_to_hash),
                               response)

    def json_object(self, hide_details):
        rv = {
            "request": self.request.to_json_object(hide_details),
            "response": {
                "headers": dict(self.response.headers),
                "statusCode": self.response.status_code,
                "encoding": self.response.encoding,
                "content": self.response.content.decode()
            }
        }

        return rv

    def hash(self):
        return self.request.hash

    def __eq__(self, other):
        return isinstance(other, RequestSnapshot) and self.hash() == other.hash()


class SnapshotAdapter(adapters.BaseAdapter):
    """A fake adapter than can return predefined responses."""

    def __init__(self,
                 snapshots,
                 capture_snapshots,
                 ignore_headers,
                 json_to_hash=None,
                 encode_body=None):
        self.snapshots = snapshots
        self.capture_snapshots = capture_snapshots
        self.ignore_headers = ignore_headers
        self.json_to_hash = json_to_hash
        self.encode_body = encode_body
        self.requests = []

    def send(self, request, **kwargs):
        key = RequestKey.from_request(request,
                                      self.ignore_headers,
                                      self.json_to_hash,
                                      self.encode_body)

        for snapshot in reversed(self.snapshots):
            if snapshot.match(key):
                if snapshot not in self.requests:
                    self.requests.append(snapshot)
                return snapshot.response

        if not self.capture_snapshots:
            raise ValueError(f"missing snapshot for request {request.url} - {key.hash}. "
                             f"try running booktest with '-s' flag to capture the missing snapshot")

        rv = adapters.HTTPAdapter().send(request)

        # remove old version, it may have been timeout
        self.requests = list([i for i in self.requests if not i.request == key])
        self.requests.append(RequestSnapshot(key, rv))

        return rv


_original_send = requests.Session.send

# NOTE(phodge): we need to use an RLock (reentrant lock) here because
# requests.Session.send() is reentrant. See further comments where we
# monkeypatch get_adapter()
_send_lock = threading.RLock()


@contextlib.contextmanager
def threading_rlock(timeout):
    kwargs = {}
    if sys.version_info.major >= 3:
        # python2 doesn't support the timeout argument
        kwargs['timeout'] = timeout

    if not _send_lock.acquire(**kwargs):
        m = "Could not acquire threading lock - possible deadlock scenario"
        raise Exception(m)

    try:
        yield
    finally:
        _send_lock.release()


def _is_bound_method(method):
    """
    bound_method 's self is a obj
    unbound_method 's self is None
    """
    if isinstance(method, types.MethodType) and six.get_method_self(method):
        return True
    return False


def _set_method(target, name, method):
    """ Set a mocked method onto the target.

    Target may be either an instance of a Session object of the
    requests.Session class. First we Bind the method if it's an instance.

    If method is a bound_method, can direct setattr
    """
    if not isinstance(target, type) and not _is_bound_method(method):
        method = six.create_bound_method(method, target)

    setattr(target, name, method)


class SnapshotRequests:

    def __init__(self,
                 t: bt.TestCaseRun,
                 lose_request_details=True,
                 ignore_headers=True,
                 json_to_hash=None,
                 encode_body=None):
        self.t = t
        self.legacy_mock_path = os.path.join(t.exp_dir_name, ".requests")
        self.mock_file = os.path.join(t.exp_dir_name, ".requests.json")
        self.mock_out_file = t.file(".requests.json")
        self._mock_target = requests.Session
        self._last_send = None
        self._last_get_adapter = None
        self._lose_request_details = lose_request_details
        self._ignore_headers = ignore_headers
        self._encode_body = encode_body

        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)

        # load snapshots
        snapshots = []

        # legacy support
        if os.path.exists(self.legacy_mock_path) and not self.refresh_snapshots:
            for mock_file in os.listdir(self.legacy_mock_path):
                with open(os.path.join(self.legacy_mock_path, mock_file), "r") as f:
                    snapshots.append(RequestSnapshot.from_json_object(json.load(f),
                                                                      ignore_headers=ignore_headers,
                                                                      json_to_hash=json_to_hash))

        if os.path.exists(self.mock_file) and not self.refresh_snapshots:
            with open(self.mock_file, "r") as f:
                for key, value in json.load(f).items():
                    snapshots.append(RequestSnapshot.from_json_object(value,
                                                                      ignore_headers=ignore_headers,
                                                                      json_to_hash=json_to_hash))

        self._adapter = SnapshotAdapter(snapshots,
                                        self.refresh_snapshots or self.complete_snapshots,
                                        ignore_headers,
                                        json_to_hash,
                                        encode_body)

    def start(self):
        """Start mocking requests.
        """
        if self._last_send:
            raise RuntimeError('Mocker has already been started')

        # backup last `send` for restoration on `self.stop`
        self._last_send = self._mock_target.send
        self._last_get_adapter = self._mock_target.get_adapter

        def _fake_get_adapter(session, url):
            return self._adapter

        def _fake_send(session, request, **kwargs):
            with threading_rlock(timeout=10):
                _set_method(session, "get_adapter", _fake_get_adapter)

                try:
                    return _original_send(session, request, **kwargs)
                finally:
                    # restore get_adapter
                    _set_method(session, "get_adapter", self._last_get_adapter)

            if isinstance(self._mock_target, type):
                return self._last_send(session, request, **kwargs)
            else:
                return self._last_send(request, **kwargs)

        _set_method(self._mock_target, "send", _fake_send)

    def stop(self):
        """Stop mocking requests.

        This should have no impact if mocking has not been started.
        When nesting mockers, make sure to stop the innermost first.
        """
        if self._last_send:
            self._mock_target.send = self._last_send
            self._last_send = None

        # let's store everything in one file to avoid spamming git
        stored = {}
        for snapshot in self._adapter.requests:
            name = snapshot.hash()
            stored[name] = snapshot.json_object(self._lose_request_details)

        with open(self.mock_out_file, "w") as f:
            json.dump(stored, f, indent=4)

    def t_snapshots(self):
        self.t.h1("request snaphots:")
        for i in self._adapter.requests:
            self.t.tln(f" * {i.request.url()} - {i.hash()}")

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.t_snapshots()


def snapshot_requests(lose_request_details=True,
                      ignore_headers=True,
                      json_to_hash=None,
                      encode_body=None):
    """
    @param lose_request_details Saves no request details to avoid leaking keys
    @param ignore_headers Ignores all headers (True) or specific header list
    @param json_to_hash allows adding your own json to hash for calculating hash code to request.
           can be used to print or prune e.g. http arguments in case they contain e.g. platform specific
           details or timestamps
    @param encode_body allows adding your own body encoding for removing e.g. platform or time details from
           request bodies. this needs to always return a string. encode body method receives body, url and method
    """
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with SnapshotRequests(t, lose_request_details, ignore_headers, json_to_hash, encode_body):
                return func(*args, **kwargs)
        wrapper._original_function = func
        return wrapper
    return decorator_depends
