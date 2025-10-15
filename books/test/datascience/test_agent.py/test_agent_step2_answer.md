
test raised exception case test_agent_step2_answer dependency test/datascience/test_agent.py::test_agent_step1_plan missing in 'books/.out/test/datascience/test_agent.py/test_agent_step1_plan.bin':
Traceback (most recent call last):
  File "/home/arau/lumoa/src/booktest/booktest/testrun.py", line 105, in run_case
    rv = await maybe_async_call(case, [t], {})
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/dependencies.py", line 338, in wrapper
    return await call_function_test(dependencies, func, args[0], kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/dependencies.py", line 315, in call_function_test
    return await call_test(function_method_caller, dependencies, func, case, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/dependencies.py", line 252, in call_test
    resolved.append(method_caller(dependency))
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/dependencies.py", line 306, in function_method_caller
    case.run.get_test_result(
  File "/home/arau/lumoa/src/booktest/booktest/testrun.py", line 82, in get_test_result
    raise Exception(
Exception: case test_agent_step2_answer dependency test/datascience/test_agent.py::test_agent_step1_plan missing in 'books/.out/test/datascience/test_agent.py/test_agent_step1_plan.bin'

