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

7/7 test 1 differed and 6 failed in <number> ms:

  book/failing_book.py::test_assert - FAIL
  book/failing_book.py::test_decorated_async_exception - FAIL
  book/failing_book.py::test_decorated_exception - FAIL
  book/failing_book.py::test_exception - FAIL
  book/failing_book.py::test_fail - FAIL
  book/failing_book.py::test_memory_monitor_exception - FAIL
  book/failing_book.py::test_success - DIFF


