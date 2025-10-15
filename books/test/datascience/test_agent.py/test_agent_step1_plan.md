# Agent Step 1: Planning

Agent analyzes the question and creates an answering strategy


## Loading Context

Loaded 27793 characters of documentation


## Creating Plan


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
  File "/home/arau/lumoa/src/booktest/test/datascience/test_agent.py", line 42, in test_agent_step1_plan
    agent = BooktestAgent(context)
            ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/datascience/booktest_agent.py", line 43, in __init__
    self.llm = get_llm()
               ^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/llm.py", line 104, in get_llm
    _default_llm = GptLlm()
                   ^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/llm.py", line 59, in __init__
    self.client = AzureOpenAI(
                  ^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/openai/lib/azure.py", line 207, in __init__
    raise ValueError(
ValueError: Must provide either the `api_version` argument or the `OPENAI_API_VERSION` environment variable

