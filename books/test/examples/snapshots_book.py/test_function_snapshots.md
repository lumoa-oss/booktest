# snapshots:


test raised exception missing snapshot for function call time_ns - bc2e0043f8879f6f886da0f550eb552d0a839f8f. try running booktest with '-s' flag to capture the missing snapshot:
Traceback (most recent call last):
  File "/home/arau/lumoa/src/booktest/booktest/testrun.py", line 105, in run_case
    rv = await maybe_async_call(case, [t], {})
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 8, in maybe_async_call
    return func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/examples/snapshots_book.py", line 284, in test_function_snapshots
    t.keyvalueln(" * timestamp:", s.snapshot(time.time_ns))
                                  ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/functions.py", line 147, in snapshot
    raise ValueError(f"missing snapshot for function call {call.func()} - {call.hash}. "
ValueError: missing snapshot for function call time_ns - bc2e0043f8879f6f886da0f550eb552d0a839f8f. try running booktest with '-s' flag to capture the missing snapshot

