"""
Snapshot module for caching arbitrary callable results.

This module provides the `t.snapshot()` method for TestCaseRun that caches
results based on a user-provided name and arguments. Results are stored in
the test's snapshot file and reused when arguments match.

Overview
--------
The snapshot mechanism allows you to cache expensive computations (API calls,
database queries, complex calculations) and replay them in subsequent test runs.
This is useful for:

- Deterministic testing of code that depends on external services
- Faster test runs by avoiding repeated expensive operations
- Capturing specific responses for regression testing

Usage
-----
The snapshot args are automatically passed to the callable::

    def test_api_integration(t: bt.TestCaseRun):
        # Cache the API response based on user_id
        # api.fetch_user is called with (user_id,)
        response = t.snapshot("user-data", user_id)(api.fetch_user)
        t.tln(f"User: {response['name']}")

With keyword arguments::

    # db.query is called with ("users", limit=10)
    result = t.snapshot("query", "users", limit=10)(db.query)

Async support::

    async def test_async_api(t: bt.TestCaseRun):
        # async_client.get is called with (url,)
        data = await t.snapshot("async-fetch", url)(async_client.get)

Lambda for complex cases::

    # Use lambda when you need to transform args or add extra parameters
    result = t.snapshot("query", table)(
        lambda t: db.query(t, limit=100, order_by="id")
    )

How It Works
------------
1. On first run with `-s` flag, the callable is executed and result stored
2. On subsequent runs, if (name, args, kwargs) hash matches, cached result is returned
3. If arguments change, the snapshot is considered missing (requires `-s` to capture)
4. Use `-S` flag to refresh all snapshots (re-execute all callables)

Storage
-------
Snapshots are stored in the test's `.snapshots.json` file under the "snapshot" type.
The storage format is::

    [
        {
            "name": "user-data",
            "args": [123],
            "kwargs": {},
            "hash": "abc123...",
            "result": {"id": 123, "name": "John"}
        }
    ]

Flags
-----
- `-s` / `--complete-snapshots`: Capture missing snapshots (keeps existing)
- `-S` / `--refresh-snapshots`: Refresh all snapshots (re-executes everything)

Comparison with Other Snapshot Types
------------------------------------
- `@snapshot_functions`: Patches functions globally, automatic capture
- `@snapshot_requests`: Captures HTTP requests via requests library
- `@snapshot_httpx`: Captures HTTP requests via httpx library
- `t.snapshot()`: Manual, explicit caching with custom keys

Use `t.snapshot()` when you need fine-grained control over what gets cached
and how it's keyed.
"""

import hashlib
import json
import inspect
from typing import Any, Callable, Optional, Tuple, Dict

from booktest.reporting.reports import SnapshotState


class SnapshotCall:
    """Represents a snapshot call with name and arguments."""

    def __init__(self, name: str, args: tuple, kwargs: dict):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        h = hashlib.sha1()
        h.update(json.dumps({
            "name": self.name,
            "args": list(self.args),
            "kwargs": self.kwargs
        }, sort_keys=True).encode())
        return str(h.hexdigest())

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "args": list(self.args),
            "kwargs": self.kwargs,
            "hash": self.hash
        }

    @staticmethod
    def from_json(data: dict) -> 'SnapshotCall':
        call = SnapshotCall(
            data["name"],
            tuple(data.get("args", [])),
            data.get("kwargs", {})
        )
        # Use stored hash if available (for consistency)
        if "hash" in data:
            call.hash = data["hash"]
        return call


class SnapshotEntry:
    """A snapshot entry containing the call and its result."""

    def __init__(self, call: SnapshotCall, result: Any):
        self.call = call
        self.result = result

    def to_json(self) -> dict:
        return {
            **self.call.to_json(),
            "result": self.result
        }

    @staticmethod
    def from_json(data: dict) -> 'SnapshotEntry':
        call = SnapshotCall.from_json(data)
        return SnapshotEntry(call, data.get("result"))


class SnapshotManager:
    """
    Manages snapshot storage for a test case.

    Handles loading, caching, and saving of snapshot entries.
    """

    def __init__(self, t):
        """
        Initialize snapshot manager.

        Args:
            t: TestCaseRun instance
        """
        self.t = t
        self.storage = t.get_storage()
        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)
        self.capture_snapshots = self.refresh_snapshots or self.complete_snapshots

        # Snapshot storage
        self.snapshots: Dict[str, SnapshotEntry] = {}  # hash -> entry (loaded from storage)
        self.calls: Dict[str, SnapshotEntry] = {}  # hash -> entry (current run)
        self._loaded = False

        # Hash tracking for state detection
        self.old_hash: Optional[str] = None
        self.stored_hash: Optional[str] = None

    def _load(self):
        """Load existing snapshots from storage (lazy loading)."""
        if self._loaded:
            return
        self._loaded = True

        if self.refresh_snapshots:
            # Skip loading when refreshing all snapshots
            return

        try:
            content = self.storage.fetch(self.t.test_id, "snapshot")
            if content:
                # Store old hash for comparison
                self.old_hash = f"sha256:{hashlib.sha256(content).hexdigest()}"

                data = json.loads(content.decode('utf-8'))
                for item in data:
                    entry = SnapshotEntry.from_json(item)
                    self.snapshots[entry.call.hash] = entry
        except Exception as e:
            raise AssertionError(
                f"test {self.t.name} snapshot file corrupted with {e}. "
                f"Use -S to refresh snapshots"
            )

    def get(self, name: str, args: tuple, kwargs: dict) -> Tuple[Optional[Any], SnapshotCall]:
        """
        Get a cached result if available.

        Args:
            name: Snapshot name
            args: Call arguments
            kwargs: Call keyword arguments

        Returns:
            Tuple of (result or None, SnapshotCall)
        """
        self._load()
        call = SnapshotCall(name, args, kwargs)

        # Check if we have this snapshot
        entry = self.snapshots.get(call.hash)
        if entry is not None:
            # Track this call
            self.calls[call.hash] = entry
            return entry.result, call

        # Check current run cache (for repeated calls)
        entry = self.calls.get(call.hash)
        if entry is not None:
            return entry.result, call

        return None, call

    def set(self, call: SnapshotCall, result: Any):
        """
        Store a result for a call.

        Args:
            call: The snapshot call
            result: The result to store
        """
        entry = SnapshotEntry(call, result)
        self.calls[call.hash] = entry

    def save(self):
        """Save all calls to storage and report usage."""
        if not self.calls:
            return

        # Build sorted list for deterministic output
        stored = []
        for hash_key in sorted(self.calls.keys()):
            stored.append(self.calls[hash_key].to_json())

        # Store via storage layer
        content = json.dumps(stored, indent=2, sort_keys=True).encode('utf-8')
        self.stored_hash = self.storage.store(self.t.test_id, "snapshot", content)

        # Determine state
        if self.old_hash is None or self.old_hash != self.stored_hash:
            state = SnapshotState.UPDATED
        else:
            state = SnapshotState.INTACT

        # Report snapshot usage
        self.t.report_snapshot_usage(
            snapshot_type="snapshot",
            hash_value=self.stored_hash,
            state=state,
            details={
                'count': len(self.calls),
                'names': list(set(e.call.name for e in self.calls.values()))
            }
        )


class SnapshotCallWrapper:
    """
    Wrapper returned by t.snapshot() that captures a callable's result.

    Supports both sync and async callables.
    """

    def __init__(self, manager: SnapshotManager, name: str, args: tuple, kwargs: dict):
        self.manager = manager
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func: Callable) -> Any:
        """
        Execute the callable, using cached result if available.

        Args:
            func: Callable to execute (can be sync or async, or a lambda
                  returning a coroutine)

        Returns:
            The result (cached or freshly computed).
            For async callables or lambdas returning coroutines, returns a coroutine.
        """
        # Check cache first
        cached_result, call = self.manager.get(self.name, self.args, self.kwargs)

        # Determine if func is async or returns a coroutine
        is_async_func = inspect.iscoroutinefunction(func)

        if cached_result is not None:
            # We have a cached result. Need to match the async nature of func.
            if is_async_func:
                # func is async, return coroutine
                async def return_cached():
                    return cached_result
                return return_cached()

            # func is sync, but might return a coroutine (lambda *args: async_fn(*args))
            # We need to check by calling it, then close the coroutine
            test_result = func(*self.args, **self.kwargs)
            if inspect.iscoroutine(test_result):
                # Close the unused coroutine to avoid warnings
                test_result.close()
                # Return cached in a coroutine wrapper
                async def return_cached_async():
                    return cached_result
                return return_cached_async()

            # Truly sync - return directly
            return cached_result

        # Not in cache - need to capture
        if not self.manager.capture_snapshots:
            raise AssertionError(
                f"missing snapshot '{self.name}' with hash {call.hash}. "
                f"try running booktest with '-s' flag to capture the missing snapshot"
            )

        # Execute callable
        if is_async_func:
            return self._call_async(func, call)
        else:
            return self._call_sync(func, call)

    def _call_sync(self, func: Callable, call: SnapshotCall) -> Any:
        """Execute sync callable with snapshot args and store result."""
        result = func(*self.args, **self.kwargs)
        # Handle case where sync callable returns a coroutine
        # (e.g., lambda *args: async_func(*args))
        if inspect.iscoroutine(result):
            return self._call_returned_coroutine(result, call)
        self.manager.set(call, result)
        return result

    async def _call_returned_coroutine(self, coro, call: SnapshotCall) -> Any:
        """Await a coroutine returned by a sync callable and store result."""
        result = await coro
        self.manager.set(call, result)
        return result

    async def _call_async(self, func: Callable, call: SnapshotCall) -> Any:
        """Execute async callable with snapshot args and store result."""
        result = await func(*self.args, **self.kwargs)
        self.manager.set(call, result)
        return result
