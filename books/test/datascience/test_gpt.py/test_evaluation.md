
test raised exception Must provide either the `api_version` argument or the `OPENAI_API_VERSION` environment variable:
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
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/env.py", line 190, in wrapper
    return await maybe_async_call(func, args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/httpx.py", line 421, in wrapper
    return await maybe_async_call(func , args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 8, in maybe_async_call
    return func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/datascience/test_gpt.py", line 81, in test_evaluation
    detector = CatDetector()
               ^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/datascience/test_gpt.py", line 56, in __init__
    self.client = AzureOpenAI(
                  ^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/openai/lib/azure.py", line 207, in __init__
    raise ValueError(
ValueError: Must provide either the `api_version` argument or the `OPENAI_API_VERSION` environment variable

