import functools
import threading
import psutil
import time

from booktest.coroutines import maybe_async_call


class MemoryMonitor:

    def __init__(self):
        self._recordings = []
        self._continue = True
        self._thread = threading.Thread(target=self.run, args=())

    def __enter__(self):
        self._thread.start()
        return self

    def stop(self):
        if self._continue:
            self._continue = False
            self._thread.join(2000)
            self._thread = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def results(self):
        self.stop()
        return self._recordings

    def run(self):
        process = psutil.Process()
        self._recordings.append(process.memory_info().rss)
        while self._continue:
            time.sleep(0.1)
            self._recordings.append(process.memory_info().rss)


def t_memory(t, name, func):
    with MemoryMonitor() as mem:
        rv = t.t(f"{name}..").imsln(func)

        res = mem.results()
        mb = 1024*1024
        min_mem = min(res) / mb
        aver_mem = sum(res) / len(res) / mb
        max_mem = max(res) / mb
        t.t(f" * memory usage: ").iln(f"{min_mem:.1f} < {aver_mem:.1f} < {max_mem:.1f} MB (n={len(res)})")

        return rv


def monitor_memory():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            m = MemoryMonitor()
            with m:
                rv = await maybe_async_call(func , args, kwargs)

            t.h1("memory:")

            res = m.results()
            mb = 1024 * 1024
            min_mem = min(res) / mb
            aver_mem = sum(res) / len(res) / mb
            max_mem = max(res) / mb

            t.anchor(f" * min:  ").ifloatln(min_mem, "MB")
            t.anchor(f" * mean: ").ifloatln(aver_mem, "MB")
            t.anchor(f" * max:  ").ifloatln(max_mem, "MB")
            t.anchor(f" * n:    ").ivalueln(len(res), "samples")

            return rv

        wrapper._original_function = func
        return wrapper

    return decorator
