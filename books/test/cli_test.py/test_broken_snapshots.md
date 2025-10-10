# description:

this test verifies that broken snapshots will gracefully fail

# command:

booktest 

# configuration:

 * context: examples/broken_snapshots

# output:


# test results:

  book/broken_snapshots_book.py::test_function_snapshot - FAIL <number> ms (snapshots updated)
  book/broken_snapshots_book.py::test_httpx - FAIL <number> ms
  book/broken_snapshots_book.py::test_requests - FAIL <number> ms

3/3 test failed in <number> ms:

  book/broken_snapshots_book.py::test_function_snapshot
  book/broken_snapshots_book.py::test_httpx
  book/broken_snapshots_book.py::test_requests


