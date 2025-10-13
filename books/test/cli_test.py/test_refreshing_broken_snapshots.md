# description:

this test verifies that:

 1) snapshots can be recreated
 2) and tool requires user to accept & store recreated snapshot even if their hashes are the same

# command:

booktest -S -v

# configuration:

 * context: examples/broken_snapshots

# output:


# test results:

test book/broken_snapshots_book.py::test_function_snapshot

  # snapshot:
  
   * hello: hello world

book/broken_snapshots_book.py::test_function_snapshot DIFF <number> ms (snapshots updated)

test book/broken_snapshots_book.py::test_httpx

  # response url parameter:
  
  "https://postman-echo.com/get"

book/broken_snapshots_book.py::test_httpx DIFF <number> ms (snapshots updated)

test book/broken_snapshots_book.py::test_requests

  # response url parameter:
  
  "https://postman-echo.com/get"

book/broken_snapshots_book.py::test_requests DIFF <number> ms (snapshots updated)


3/3 test 3 differed in <number> ms:

  book/broken_snapshots_book.py::test_function_snapshot - DIFF
  book/broken_snapshots_book.py::test_httpx - DIFF
  book/broken_snapshots_book.py::test_requests - DIFF


