# test environment variable:


test raised exception 'TEST_ENV_VARIABLE':
Traceback (most recent call last):
  File "/home/arau/lumoa/src/booktest/booktest/testrun.py", line 105, in run_case
    rv = await maybe_async_call(case, [t], {})
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/env.py", line 128, in wrapper
    return await maybe_async_call(func, args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 8, in maybe_async_call
    return func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/examples/snapshots_book.py", line 157, in test_env
    t.keyvalueln(" * TEST_ENV_VARIABLE:", os.environ["TEST_ENV_VARIABLE"])
                                          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "<frozen os>", line 679, in __getitem__
KeyError: 'TEST_ENV_VARIABLE'

