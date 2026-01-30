import functools
import os
import booktest as bt
import json

from booktest.utils.coroutines import maybe_async_call
from booktest.snapshots.snapshots import out_snapshot_path, frozen_snapshot_path, have_snapshots_dir
from booktest.utils.utils import file_or_resource_exists, open_file_or_resource


class SnapshotEnv:

    def __init__(self,
                 t: bt.TestCaseRun,
                 names: list):
        self.t = t
        self.storage = t.get_storage()
        self.names = names

        self.snaphots = {}
        self._old_env = {}
        self.capture = {}

        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)
        self.stored_hash = None  # Store hash from storage layer

        # Legacy support - single file format (.env.json)
        legacy_file_path = os.path.join(t.exp_dir_name, ".env.json")
        if file_or_resource_exists(legacy_file_path, t.resource_snapshots) and not self.refresh_snapshots:
            with open_file_or_resource(legacy_file_path, t.resource_snapshots) as f:
                self.snaphots = json.load(f)

        # Load snapshots from storage if not refreshing
        if not self.refresh_snapshots:
            content = self.storage.fetch(t.test_id, "env")
            if content:
                self.snaphots = json.loads(content.decode('utf-8'))

    def start(self):
        if self._old_env is None:
            raise AssertionError("already started")

        # Reset the global LLM cache so it will be recreated with restored env vars
        from booktest.llm.llm import set_llm
        set_llm(None)

        self._old_env = {}
        for name in self.names:
            old_value = os.environ.get(name)
            self._old_env[name] = old_value
            if name in self.snaphots:
                value = self.snaphots[name]
                if value is None:
                    if name in os.environ:
                        del os.environ[name]
                else:
                    os.environ[name] = self.snaphots[name]
                self.capture[name] = value
            elif self.complete_snapshots or self.refresh_snapshots:
                self.capture[name] = old_value
            else:
                raise Exception(
                    f"missing env snapshot '{name}'. "
                    "try running booktest with '-s' flag to capture the missing snapshot")

    def stop(self):
        for name, value in self._old_env.items():
            if value is None:
                if name in os.environ:
                    del os.environ[name]
            else:
                os.environ[name] = self._old_env[name]

        # Reset the global LLM cache so subsequent code uses restored env vars
        from booktest.llm.llm import set_llm
        set_llm(None)

        # Get old hash before storing new content
        old_content = self.storage.fetch(self.t.test_id, "env")
        old_hash = None
        if old_content:
            import hashlib
            old_hash = f"sha256:{hashlib.sha256(old_content).hexdigest()}"

        # Store via storage layer
        content = json.dumps(self.capture, indent=4).encode('utf-8')
        # storage.store() returns hash of normalized content
        self.stored_hash = self.storage.store(self.t.test_id, "env", content)

        # Store old hash for comparison in t_snapshots
        self.old_hash = old_hash

    def t_snapshots(self):
        """Report snapshot usage to the system instead of printing to test results."""
        from booktest.reporting.reports import SnapshotState

        # Determine snapshot state by comparing hashes
        if self.old_hash is None or self.old_hash != self.stored_hash:
            state = SnapshotState.UPDATED
        else:
            state = SnapshotState.INTACT

        # Use hash from storage layer
        if self.capture:
            # Report to system using hash from storage
            # Note: For security, we only include variable names, not values
            self.t.report_snapshot_usage(
                snapshot_type="env",
                hash_value=self.stored_hash,
                state=state,
                details={
                    'count': len(self.capture),
                    'variables': list(self.capture.keys())
                    # Intentionally not including values for security
                }
            )

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.t_snapshots()


def snapshot_env(*names):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with SnapshotEnv(t, names):
                return await maybe_async_call(func, args, kwargs)
        wrapper._original_function = func
        return wrapper

    return decorator


class MockMissingEnv:

    def __init__(self, t: bt.TestCaseRun, env: dict):
        self.t = t
        self.env = env

        self._old_env = {}

        refresh_snapshots = t.config.get("refresh_snapshots", False)
        complete_snapshots = t.config.get("complete_snapshots", False)

        # mocking is on only, when we are not updating snapshots
        self._do_mock = not (refresh_snapshots | complete_snapshots)

    def start(self):
        if self._old_env is None:
            raise AssertionError("already started")

        self._old_env = {}
        for name, value in self.env.items():
            old_value = os.environ.get(name)
            self._old_env[name] = old_value

            if old_value is None:
                if value is None:
                    if name in os.environ:
                        del os.environ[name]
                else:
                    os.environ[name] = value

    def stop(self):
        for name, value in self._old_env.items():
            if value is None:
                if name in os.environ:
                    del os.environ[name]
            else:
                os.environ[name] = self._old_env[name]

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def mock_missing_env(env):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with MockMissingEnv(t, env):
                return await maybe_async_call(func, args, kwargs)
        wrapper._original_function = func
        return wrapper
    return decorator


class MockEnv:

    def __init__(self, env: dict):
        self.env = env

        self._old_env = None

    def start(self):
        if self._old_env is not None:
            raise AssertionError("already started")

        self._old_env = {}
        for name, value in self.env.items():
            old_value = os.environ.get(name)
            self._old_env[name] = old_value

            if value is None:
                if name in os.environ:
                    del os.environ[name]
            else:
                os.environ[name] = value

    def stop(self):
        for name, value in self._old_env.items():
            if value is None:
                if name in os.environ:
                    del os.environ[name]
            else:
                os.environ[name] = self._old_env[name]
        self._old_env = None

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def mock_env(env):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            with MockEnv(env):
                return await maybe_async_call(func , args, kwargs)
        wrapper._original_function = func
        return wrapper

    return decorator
