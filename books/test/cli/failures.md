# command:

booktest -v

# configuration:

 * context: examples/failures

# output:


# test results:

test book/failing/assert...

  # fail with assert() method:
  
! is 1 == 2? FAILED                                            | EOF

book/failing/assert FAILED in <number> ms

test book/failing/decorated_async_exception...

  # fail with exception:
  
  
! test raised exception this is an exception:                  | EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/testrun.py", line 94, in run_case
      rv = await case(t)
           ^^^^^^^^^^^^^
    File "<workdir>/booktest/env.py", line 202, in wrapper
      return await maybe_async_call(func , args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 35, in test_decorated_async_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing/decorated_async_exception FAILED in <number> ms

test book/failing/decorated_exception...

  # fail with exception:
  
  
! test raised exception this is an exception:                  | EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/testrun.py", line 94, in run_case
      rv = await case(t)
           ^^^^^^^^^^^^^
    File "<workdir>/booktest/env.py", line 202, in wrapper
      return await maybe_async_call(func , args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 8, in maybe_async_call
      return func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 29, in test_decorated_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing/decorated_exception FAILED in <number> ms

test book/failing/exception...

  # fail with exception:
  
  
! test raised exception this is an exception:                  | EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/testrun.py", line 96, in run_case
      rv = case(t)
           ^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 23, in test_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing/exception FAILED in <number> ms

test book/failing/fail...

  # fail with fail() method:
  
! failed!                                                      | EOF

book/failing/fail FAILED in <number> ms

test book/failing/memory_monitor_exception...

  # fail with exception:
  
  
! test raised exception this is an exception:                  | EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/testrun.py", line 94, in run_case
      rv = await case(t)
           ^^^^^^^^^^^^^
    File "<workdir>/booktest/memory.py", line 66, in wrapper
      rv = await maybe_async_call(func , args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/failures/book/failing_book.py", line 41, in test_memory_monitor_exception
      raise Exception("this is an exception")
  Exception: this is an exception
  

book/failing/memory_monitor_exception FAILED in <number> ms

test book/failing/success...

  # succeeding test for control:
  
  ok.

book/failing/success ok in <number> ms.


6/7 test failed in <number> ms:

  book/failing/assert
  book/failing/decorated_async_exception
  book/failing/decorated_exception
  book/failing/exception
  book/failing/fail
  book/failing/memory_monitor_exception


