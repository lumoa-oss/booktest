import copy
import functools
import hashlib
import os
import pickle
import json
import sys
from collections import defaultdict

from booktest import TestCaseRun
from booktest.utils.coroutines import maybe_async_call
from booktest.snapshots.snapshots import frozen_snapshot_path, out_snapshot_path, have_snapshots_dir
from booktest.utils.utils import open_file_or_resource, file_or_resource_exists


class FunctionCall:

    def __init__(self, json_object):
        self.json_object = json_object

        hash_code = self.json_object.get("hash")

        if hash_code is None:
            h = hashlib.sha1()
            h.update(json.dumps(self.json_object).encode())
            hash_code = str(h.hexdigest())
            self.json_object["hash"] = hash_code

        self.hash = hash_code

    def func(self):
        return self.json_object["func"]

    def args(self):
        # tuple is used by default in python
        return self.json_object["args"]

    def kwargs(self):
        return self.json_object["kwargs"]

    def to_json_object(self, hide_details):
        rv = copy.copy(self.json_object)
        rv["hash"] = self.hash
        return rv

    @staticmethod
    def from_properties(func, args, kwargs):
        json_object = {
            "func": str(func.__qualname__),
            "args": list(args),
            "kwargs": dict(kwargs)
        }
        return FunctionCall(json_object)

    def __eq__(self, other):
        return isinstance(other, FunctionCall) and self.hash == other.hash


class FunctionCallSnapshot:

    def __init__(self,
                 call,
                 result):
        self.call = call
        self.result = result

    def match(self, call: FunctionCall):
        return self.call == call

    @staticmethod
    def from_json_object(json_object):
        return FunctionCallSnapshot(FunctionCall(json_object["call"]),
                                    json_object["result"])

    def json_object(self):
        rv = {
            "call": self.call.json_object,
            "result": self.result
        }
        return rv

    def func(self):
        return self.call.func()

    def hash(self):
        return self.call.hash

    def __eq__(self, other):
        return isinstance(other, FunctionCallSnapshot) and self.hash() == other.hash()


class FunctionSnapshotter:

    def __init__(self, t: TestCaseRun, func):
        self.t = t
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.t.snapshot(self.func, *args, **kwargs)

    def __repr__(self):
        return str(self.func)


def set_function(func, value):
    target = None
    if hasattr(func, "__self__"):
        target = func.__self__
    elif hasattr(func, "__module__"):
        target = sys.modules[func.__module__]
    name = func.__name__
    setattr(target, name, value)


class SnapshotFunctions:

    def __init__(self, t: TestCaseRun, snapshot_funcs: list = None):
        self.t = t
        self.storage = t.get_storage()

        if snapshot_funcs is None:
            snapshot_funcs = []

        self.snapshot_funcs = snapshot_funcs

        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)

        self.capture_snapshots = self.refresh_snapshots or self.complete_snapshots
        self.stored_hash = None  # Store hash from storage layer

        self.snapshots = None
        self.calls = None
        self.snapshotters = None

    def snapshot(self, func, *args, **kwargs):
        call = FunctionCall.from_properties(func, args, kwargs)
        function_calls = self.calls[call.func()]

        snapshot = self.snapshots[call.func()].get(call.hash)
        if snapshot is not None:
            if snapshot.hash() not in function_calls:
                function_calls[call.hash] = snapshot
            return snapshot.result

        if not self.capture_snapshots:
            raise AssertionError(f"missing snapshot for function call {call.func()} - {call.hash}. "
                                 f"try running booktest with '-s' flag to capture the missing snapshot")

        # assume determinism and use past calls as cache
        snapshot = function_calls.get(call.hash)
        if snapshot is not None:
            return snapshot.result

        rv = func(*args, **kwargs)
        function_calls[call.hash] = FunctionCallSnapshot(call, rv)

        return rv

    def start(self):
        if self.snapshots is not None:
            raise RuntimeError('FunctionSnapshots has already been started')

        snapshots = defaultdict(dict)

        # Load from storage if not refreshing
        if not self.refresh_snapshots:
            try:
                content = self.storage.fetch(self.t.test_id, "func")
                if content:
                    for value in json.loads(content.decode('utf-8')):
                        snapshot = FunctionCallSnapshot.from_json_object(value)
                        snapshots[snapshot.func()][snapshot.hash()] = snapshot
            except Exception as e:
                raise AssertionError(f"test {self.t.name} snapshot file corrupted with {e}. "
                                     f"Use -S to refresh snapshots")

        snapshotters = []

        for func in self.snapshot_funcs:
            snapshotter = FunctionSnapshotter(self, func)
            set_function(func, snapshotter)
            snapshotters.append(snapshotter)

        self.snapshots = snapshots
        self.calls = defaultdict(dict)
        self.snapshotters = snapshotters

    def stop(self):
        for snapshotter in self.snapshotters:
            func = snapshotter.func
            set_function(func, func)

        # Get old hash before storing new content
        old_content = self.storage.fetch(self.t.test_id, "func")
        old_hash = None
        if old_content:
            import hashlib
            old_hash = f"sha256:{hashlib.sha256(old_content).hexdigest()}"

        stored = []
        for _, function_snapshots in sorted(list(self.calls.items()), key=lambda x: x[0]):
            for hash, snapshot in sorted(list(function_snapshots.items()), key=lambda x: x[0]):
                stored.append(snapshot.json_object())

        # Store via storage layer
        content = json.dumps(stored, indent=4).encode('utf-8')
        # storage.store() returns hash of normalized content
        self.stored_hash = self.storage.store(self.t.test_id, "func", content)

        # Store old hash for comparison in t_snapshots
        self.old_hash = old_hash

        # Keep snapshots and calls for t_snapshots() reporting, only clear snapshotters
        self.snapshotters = None

    def t_snapshots(self):
        """Report snapshot usage to the system instead of printing to test results."""
        from booktest.reporting.reports import SnapshotState

        # Determine snapshot state by comparing hashes
        if self.old_hash is None or self.old_hash != self.stored_hash:
            state = SnapshotState.UPDATED
        else:
            state = SnapshotState.INTACT

        # Build function summaries for details
        function_summaries = {}
        for function, function_snapshots in sorted(list(self.calls.items()), key=lambda x: x[0]):
            hashes = sorted(list(function_snapshots.keys()))
            stored = self.snapshots[function]
            h = hashlib.sha1()
            for i in hashes:
                if i not in stored:
                    # force snapshot creation, if a snapshot is missing
                    self.t.diff()
                h.update(i.encode())
            aggregate_hash = str(h.hexdigest())

            function_summaries[function] = {
                'aggregate_hash': aggregate_hash,
                'count': len(hashes),
                'unique_calls': len(set(hashes)),
                'hashes': hashes[:10]  # Store first 10 hashes for reference
            }

        # Use hash from storage layer
        if function_summaries:
            # Report to system using hash from storage
            self.t.report_snapshot_usage(
                snapshot_type="func",
                hash_value=self.stored_hash,
                state=state,
                details={
                    'functions': function_summaries
                }
            )

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.t_snapshots()


def snapshot_functions(*snapshot_funcs):
    """
    @param lose_request_details Saves no request details to avoid leaking keys
    @param ignore_headers Ignores all headers (True) or specific header list
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with SnapshotFunctions(t, snapshot_funcs):
                return await maybe_async_call(func, args, kwargs)
        wrapper._original_function = func
        return wrapper

    return decorator


class MockFunctions:

    def __init__(self, mock_funcs: dict = None):
        if mock_funcs is None:
            mock_funcs = {}

        self.mock_funcs = mock_funcs
        self._original_funcs = None

    def start(self):
        if self._original_funcs is not None:
            raise RuntimeError('FunctionSnapshots has already been started')

        original_funcs = []

        for func, mock in self.mock_funcs.items():
            set_function(func, mock)
            original_funcs.append(func)

        self._original_funcs = original_funcs

    def stop(self):
        for func in self._original_funcs:
            set_function(func, func)

        self._original_funcs = None

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def mock_functions(mock_funcs):
    """
    @param lose_request_details Saves no request details to avoid leaking keys
    @param ignore_headers Ignores all headers (True) or specific header list
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with MockFunctions(mock_funcs):
                return await maybe_async_call(func, args, kwargs)
        wrapper._original_function = func
        return wrapper

    return decorator
