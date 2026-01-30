# command:

booktest 

# configuration:

 * context: examples/failures

# output:


# test results:

  book/failing_book.py::test_assert - FAIL <number> ms
  book/failing_book.py::test_decorated_async_exception - FAIL <number> ms
  book/failing_book.py::test_decorated_exception - FAIL <number> ms
  book/failing_book.py::test_exception - FAIL <number> ms
  book/failing_book.py::test_fail - FAIL <number> ms
  book/failing_book.py::test_memory_monitor_exception - FAIL <number> ms
  book/failing_book.py::test_success - DIFF <number> ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# test results:

test book/failing_book.py::test_assert

  # fail with assert() method:
  
! is 1 == 2? FAILED                                            ≠ EOF

book/failing_book.py::test_assert FAILED in <number> ms

test book/failing_book.py::test_decorated_async_exception

  # fail with exception:
  
  
! test raised exception this is an exception:                  ≠ EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/core/testrun.py", line 105, in run_case
      rv = await maybe_async_call(case, [t], {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/utils/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/snapshots/env.py", line 248, in wrapper
      return await maybe_async_call(func , args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/utils/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 35, in test_decorated_async_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing_book.py::test_decorated_async_exception FAILED in <number> ms

test book/failing_book.py::test_decorated_exception

  # fail with exception:
  
  
! test raised exception this is an exception:                  ≠ EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/core/testrun.py", line 105, in run_case
      rv = await maybe_async_call(case, [t], {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/utils/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/snapshots/env.py", line 248, in wrapper
      return await maybe_async_call(func , args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/utils/coroutines.py", line 8, in maybe_async_call
      return func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 29, in test_decorated_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing_book.py::test_decorated_exception FAILED in <number> ms

test book/failing_book.py::test_exception

  # fail with exception:
  
  
! test raised exception this is an exception:                  ≠ EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/core/testrun.py", line 105, in run_case
      rv = await maybe_async_call(case, [t], {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/utils/coroutines.py", line 8, in maybe_async_call
      return func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 23, in test_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing_book.py::test_exception FAILED in <number> ms

test book/failing_book.py::test_fail

  # fail with fail() method:
  
! failed!                                                      ≠ EOF

book/failing_book.py::test_fail FAILED in <number> ms

test book/failing_book.py::test_memory_monitor_exception

  # fail with exception:
  
  
! test raised exception this is an exception:                  ≠ EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/core/testrun.py", line 105, in run_case
      rv = await maybe_async_call(case, [t], {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/utils/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/dependencies/memory.py", line 66, in wrapper
      rv = await maybe_async_call(func , args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/utils/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 41, in test_memory_monitor_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing_book.py::test_memory_monitor_exception FAILED in <number> ms

test book/failing_book.py::test_success

  # succeeding test for control:
  
  ok.

book/failing_book.py::test_success DIFFERED in <number> ms


7/7 test 1 differed and 6 failed in <number> ms:

  book/failing_book.py::test_assert - FAIL
  book/failing_book.py::test_decorated_async_exception - FAIL
  book/failing_book.py::test_decorated_exception - FAIL
  book/failing_book.py::test_exception - FAIL
  book/failing_book.py::test_fail - FAIL
  book/failing_book.py::test_memory_monitor_exception - FAIL
  book/failing_book.py::test_success - DIFF


💡 To review (-w) failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -w -c -v -i
💡 To rerun failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -c -v -i
💡 To update failed tests's (-c) missing snapshots (-s), run: booktest -c -s


