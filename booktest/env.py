import functools
import os
import booktest as bt
import json

from booktest.coroutines import maybe_async_call
from booktest.snapshots import out_snapshot_path, frozen_snapshot_path, have_snapshots_dir
from booktest.utils import file_or_resource_exists, open_file_or_resource


class SnapshotEnv:

    def __init__(self,
                 t: bt.TestCaseRun,
                 names: list):
        self.t = t
        self.names = names

        self.snaphot_path = frozen_snapshot_path(t, "env.json")
        self.snapshot_out_path = out_snapshot_path(t, "env.json")

        self.snaphots = {}
        self._old_env = {}
        self.capture = {}

        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)

        # load snapshots
        if file_or_resource_exists(self.snaphot_path, t.resource_snapshots) and not self.refresh_snapshots:
            with open_file_or_resource(self.snaphot_path, t.resource_snapshots) as f:
                self.snaphots = json.load(f)

    def start(self):
        if self._old_env is None:
            raise ValueError("already started")

        self._old_env = {}
        for name in self.names:
            old_value = os.environ.get(name)
            self._old_env[name] = old_value
            if name in self.snaphots:
                value = self.snaphots[name]
                if value is None:
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

        have_snapshots_dir(self.t)
        with open(self.snapshot_out_path, "w") as f:
            json.dump(self.capture, f, indent=4)

    def t_snapshots(self):
        self.t.h1("env snaphots:")
        for name, value in self.capture.items():
            self.t.tln(f" * {name}={value}")

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
            raise ValueError("already started")

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
            raise ValueError("already started")

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
