# description:

this test verifies that the slow test will fail with 1s timeout

# command:

booktest -p --timeout 2

# configuration:

 * context: examples/timeout

# output:


# test results:

  book/timeout_book.py::test_slow..FAILED in <number> ms
  book/timeout_book.py::test_fast..FAILED in <number> ms

2/2 test failed in <number> ms:

  book/timeout_book.py::test_slow
  book/timeout_book.py::test_fast


