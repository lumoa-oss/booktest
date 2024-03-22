import functools
import os
import booktest as bt
import json


class SnapshotEnv:

    def __init__(self,
                 t: bt.TestCaseRun,
                 names: list):
        self.t = t
        self.names = names

        self.snaphot_path = os.path.join(t.exp_dir_name, ".env.json")
        self.snapshot_out_path = t.file(".env.json")

        self.snaphots = {}
        self._old_env = {}
        self.capture = {}

        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)

        # load snapshots
        if os.path.exists(self.snaphot_path) and not self.refresh_snapshots:
            with open(self.snaphot_path, "r") as f:
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
                del os.environ[name]
            else:
                os.environ[name] = self._old_env[name]

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
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with SnapshotEnv(t, names):
                return func(*args, **kwargs)
        wrapper._original_function = func
        return wrapper
    return decorator_depends


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
                    del os.environ[name]
                else:
                    os.environ[name] = value

    def stop(self):
        for name, value in self._old_env.items():
            if value is None:
                del os.environ[name]
            else:
                os.environ[name] = self._old_env[name]

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def mock_missing_env(env):
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with MockMissingEnv(t, env):
                return func(*args, **kwargs)
        wrapper._original_function = func
        return wrapper
    return decorator_depends


class MockEnv:

    def __init__(self, t: bt.TestCaseRun, env: dict):
        self.t = t
        self.env = env

        self._old_env = {}

    def start(self):
        if self._old_env is None:
            raise ValueError("already started")

        self._old_env = {}
        for name, value in self.env.items():
            old_value = os.environ.get(name)
            self._old_env[name] = old_value

            if value is None:
                del os.environ[name]
            else:
                os.environ[name] = value

    def stop(self):
        for name, value in self._old_env.items():
            if value is None:
                del os.environ[name]
            else:
                os.environ[name] = self._old_env[name]

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def mock_env(env):
    def decorator_depends(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with MockEnv(t, env):
                return func(*args, **kwargs)
        wrapper._original_function = func
        return wrapper
    return decorator_depends
