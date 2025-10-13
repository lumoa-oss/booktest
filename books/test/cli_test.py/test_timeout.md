# description:

this test verifies that the slow test will fail with 1s timeout

# command:

booktest -p --timeout 2

# configuration:

 * context: examples/timeout

# output:


# test results:

  book/timeout_book.py::test_fast - <number> ms
  book/timeout_book.py::test_slow - FAILED in <number> ms

1/2 test 1 failed in <number> ms:

  book/timeout_book.py::test_slow - FAIL


