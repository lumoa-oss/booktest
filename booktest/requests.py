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


class Snapshot:

    def __init__(self,
                 request: requests.PreparedRequest,
                 response: requests.Response):
        self.request = request
        self.response = response

    def match(self, request: requests.PreparedRequest):
        return (self.request.url == request.url and
                self.request.method == request.method and
                self.request.body == request.body)

    @staticmethod
    def from_json_object(json_object):
        i = json_object["request"]
        request = requests.PreparedRequest()
        request.url = i["url"]
        request.method = i["method"]
        request.headers = i["headers"]
        request.body = i["body"]
        o = json_object["response"]
        response = requests.Response()
        response.headers = o["headers"]
        response.status_code = o["statusCode"]
        response.encoding = o["encoding"]
        response._content = o["content"].encode()

        return Snapshot(request,
                        response)

    def json_object(self):
        rv = {
            "request": {
                "url": self.request.url,
                "method": self.request.method,
                "headers": dict(self.request.headers),
                "body": self.request.body
            },
            "response": {
                "headers": dict(self.response.headers),
                "statusCode": self.response.status_code,
                "encoding": self.response.encoding,
                "content": self.response.content.decode()
            }
        }

        return rv

    def hash(self):
        h = hashlib.sha1()
        h.update(self.request.url.encode())
        h.update(json.dumps(self.json_object()["request"]).encode())
        return h.hexdigest()

    def name(self):
        return self.hash()


class SnapshotAdapter(adapters.BaseAdapter):
    """A fake adapter than can return predefined responses."""

    def __init__(self, snapshots):
        self.snapshots = snapshots
        self.requests = []

    def send(self, request, **kwargs):
        for snapshot in reversed(self.snapshots):
            if snapshot.match(request):
                if snapshot not in self.requests:
                    self.requests.append(snapshot)
                return snapshot.response

        rv = adapters.HTTPAdapter().send(request)
        self.requests.append(Snapshot(request, rv))

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

    def __init__(self, t: bt.TestCaseRun):
        self.t = t
        self.mock_path = os.path.join(t.exp_dir_name, ".requests")
        self.mock_out_path = t.file(".requests")
        self._mock_target = requests.Session
        self._last_send = None
        self._last_get_adapter = None
        # load snapshots
        snapshots = []
        if os.path.exists(self.mock_path):
            for mock_file in os.listdir(self.mock_path):
                with open(os.path.join(self.mock_path, mock_file), "r") as f:
                    snapshots.append(Snapshot.from_json_object(json.load(f)))

        self._adapter = SnapshotAdapter(snapshots)

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

        os.makedirs(self.mock_out_path, exist_ok=True)

        for snapshot in self._adapter.requests:
            name = snapshot.name()

            with open(os.path.join(self.mock_out_path, f"{name}.json"), "w") as f:
                json.dump(snapshot.json_object(), f, indent=4)

    def t_snapshots(self):
        self.t.h1("snaphots:")
        for i in self._adapter.requests:
            self.t.tln(f" * {i.request.url} - {i.name()}")

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.t_snapshots()


def snapshot_requests():
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with SnapshotRequests(t):
                return func(*args, **kwargs)
        wrapper._original_function = func
        return wrapper
    return decorator_depends

