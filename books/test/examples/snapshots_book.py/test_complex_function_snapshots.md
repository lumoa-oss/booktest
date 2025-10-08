# running 20 snapshots in random order to 2 different methods:


test raised exception missing snapshot for function call plus_one - 50a89c548410f5be533462ca83734b64459c7c82. try running booktest with '-s' flag to capture the missing snapshot:
Traceback (most recent call last):
  File "/home/arau/lumoa/src/booktest/booktest/testrun.py", line 105, in run_case
    rv = await maybe_async_call(case, [t], {})
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/functions.py", line 282, in wrapper
    return await maybe_async_call(func, args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/examples/snapshots_book.py", line 344, in test_complex_function_snapshots
    results[value] = plus_one(value)
                     ^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/functions.py", line 99, in __call__
    return self.t.snapshot(self.func, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/functions.py", line 147, in snapshot
    raise ValueError(f"missing snapshot for function call {call.func()} - {call.hash}. "
ValueError: missing snapshot for function call plus_one - 50a89c548410f5be533462ca83734b64459c7c82. try running booktest with '-s' flag to capture the missing snapshot

